import heapq
import itertools
from math import ceil, floor, log2
from typing import overload
from matplotlib import pyplot as plt
from typing import List, Tuple

import numpy as np
from scipy.signal import convolve2d
from scipy.stats import norm
from Layer_3.navigation.map import Map
from Layer_3.navigation.metric_position import MetricPosition

from Layer_3.navigation.polar import Polar
from Layer_3.navigation.polar_to_cartesian import polar_to_cartesian
from debugTools import printDebug

DEBUG = False


class PointCloudCartesian():
    """Cartesian representation of point cloud."""    
    @overload
    def __init__(self, point_cloud_polar: List[List], blur_radius: int = 5) -> None:
        """Cartesian representation of point cloud.

        Args:
        ---
            point_cloud_polar (list[list]): Collected point cloud from Lidar.
            blur_radius (int, optional): Blur radius for convolution process. Defaults to 5.
        """
        self.__init__(point_cloud_polar=Polar.from_array(point_cloud_polar), blur_radius=blur_radius)
        
    def __init__(self, point_cloud_polar: List[Polar], blur_radius: int = 5) -> None:
        """Cartesian representation of point cloud.

        Args:
        ---
            point_cloud_polar (list[Polar]): Collected point cloud from Lidar.
            blur_radius (int, optional): Blur radius for convolution process. Defaults to 5.
        """
        self._blur_radius = blur_radius
        self._data, self._position, self._direction = polar_to_cartesian(Polar.from_array(point_cloud_polar), alignment_iterations=1)
        self._width, self._height = self._data.shape
        self._map_position = None
        X, Y = self._width, self._height
        x, y = self._position
        self._offset_matrix = [
            np.array([x, y]),
            np.array([Y - y, x]),
            np.array([X - x, Y - y]),
            np.array([y, X-x])
        ]
        
        self._blur()
        
    @property
    def width(self) -> int:
        return self._data.shape[0]
        Tuple
    @property
    def height(self) -> int:
        return self._data.shape[1]
        
    @property
    def direction(self):
        return self._direction
        
    @property
    def width(self):
        return self._width
        
    @property
    def height(self):
        return self._height
        
    @property
    def offset_matrix(self):
        return self._offset_matrix
    
    def get_data(self):
        return self._data
        
    def _blur(self) -> None:
        x = norm.pdf(np.linspace(-2, 2, 2*self._blur_radius+1))
        k = np.outer(x, x)
        self._blurred_data = [[convolve2d(self._data, k, 'same')], [], [], []]
        for r in range(1, 4): self._blurred_data[r].append(np.rot90(self._blurred_data[0][0], k=r))
    
    def processed(self, rotations90: int, stage: int) -> np.ndarray:
        """Generates and returns resized and rotated data array for faster computation.
        All generated arrays will be stored and do not have to be generated again if needed multiple times.

        Args:
        ----
            rotation90 (int): number of 90° rotations -> 0: 0°, 1: 90°, 2: 180°...
            s (int): Resize step: square width that gets summarized.

        Returns:
        ----
            np.ndarray: Resized and rotated array.
        """
        
        n = stage
        
        while len(self._blurred_data[0]) <= n:
            l = len(self._blurred_data[0])
            nn = 1 << l
            
            self._blurred_data[0].append(np.zeros(shape=[ceil(self.width / nn), ceil(self.height / nn)]))                               # appending new array
            for i, j in itertools.product(range(self._blurred_data[0][-1].shape[0]), range(self._blurred_data[0][-1].shape[1])):        # for each field in new array:
                self._blurred_data[0][-1][i][j] = (self._blurred_data[0][0][i << l:(i+1) << l, j << l:(j+1) << l] * nn**2).mean()       # merging squares with edge length 1**l
                
            for r in range(1, 4):
                self._blurred_data[r].append(np.rot90(self._blurred_data[0][-1], k=r))                                                  # adding rotated versions

        return self._blurred_data[rotations90][n]
    
    def get_map_position(self):
        return self._map_position
    
    def determine_map_position(self, map:Map, scan_radius: int = 6, stages: int = 4, threshold: float = 0.7) -> List[int]:
        """Determines position and orientation of point cloud in mapped environment.

        Args:
        ----
            map (Map): Map of environment.
            scan_radius (int, optional): Radius to be scanned around previously detected peaks. Defaults to 6.
            stages (int, optional): Number of processing operations at different resolutions. Defaults to 4.
            threshold (float, optional): Threshold for peaks to be scanned in next step. Defaults to 0.7. (Range: 0...1)
            
        Returns:
        ----
            list[int, int]: Determined coordinates
        """

        def calcConvolution(areas: List, point_cloud_s: np.ndarray, map_s: np.ndarray) -> Tuple[List, np.ndarray]:
            """Calculates convolution steps:

            Args:
            ---
                areas (list): List of areas to be scanned.
                point_cloud_s (np.ndarray): Resized and rotated point cloud for this particular calculation.
                map_s (np.ndarray): Resized and rotated map for this particular calculation.

            Returns:
            ---
                list[list, np.ndarray]:
                    1. List of all values with their related coordinates.
                    2. Convolution output.
            """
            maxima = []
            width, height = point_cloud_s.shape
            outShape = [map_s.shape[0] - width + 1, map_s.shape[1] - height + 1]
            output = np.zeros(shape=outShape)

            for area in areas:
                area[0][0] = max(area[0][0], 0)
                area[0][1] = max(area[0][1], 0)
                area[1][0] = min(area[1][0], outShape[0])
                area[1][1] = min(area[1][1], outShape[1])

                for i in range(area[0][0], area[1][0]):
                    for j in range(area[0][1], area[1][1]):
                        if output[i][j] == 0:
                            output[i][j] = np.sum(point_cloud_s * map_s[i:i+width, j:j+height])
                            maxima.append([output[i][j], i, j])
                        
            return maxima, output

        finals = []
        
        if DEBUG: fig = plt.figure(figsize=(4,5))

        for rotations90 in range(4):    # computation for each orientation
            if DEBUG: printDebug(str=f'rotations90 = {rotations90}', color='red')
            if rotations90 % 2: areas = [[[0,0], [map.width - self.height + 1, map.height - self.width + 1]]]
            else: areas = [[[0,0], [map.width - self.width + 1, map.height - self.height + 1]]]
            
            if DEBUG:
                fig.add_subplot(4, 5, 5*rotations90 + 1)
                plt.imshow(self.processed(rotations90=rotations90, stage=0))

            for stage in range(stages - 1, -1, -1):
                if DEBUG: printDebug(str=f'stage = {stage}', color='red')
                maxima, output = calcConvolution(areas=areas, point_cloud_s=self.processed(rotations90=rotations90, stage=stage), map_s=map.resized(stage))
                
                if DEBUG:
                    fig.add_subplot(4, 5, 5*rotations90 + 5 - stage)
                    plt.gca().set_title(f'{rotations90*90}° -> stage {stage}')
                    plt.imshow(output)
                
                areas = []
                thresh_intern = heapq.nlargest(1, maxima)[0][0] * threshold
                while len(maxima) > 0 and stage > 0:
                    maximum = heapq.nlargest(1, maxima)[0]
                    if maximum[0] < thresh_intern: break
                    maxima.remove(maximum)
                    step = 2**(stage + 1)
                    areas.append([
                        [maximum[1] * 2 - step * (scan_radius),  maximum[2] * 2 - step * (scan_radius)],
                        [maximum[1] * 2 + step * (scan_radius + 1),  maximum[2] * 2 + step * (scan_radius + 1)],
                        maximum
                    ])


            maxFinal = heapq.nlargest(1, maxima)[0]
            
            maxFinal[1:] += self.offset_matrix[rotations90]

            maxFinal.append(rotations90)

            finals.append(maxFinal)
            
        if DEBUG: plt.show()
            
        maxFinal = heapq.nlargest(1, finals)[0][1:]
        
        self._direction -= 90 * maxFinal[2]
        self._map_position = MetricPosition(x=maxFinal[0] * map.resolution, y=maxFinal[1] * map.resolution, z=0, alpha=self._direction)
        
        return self._map_position
