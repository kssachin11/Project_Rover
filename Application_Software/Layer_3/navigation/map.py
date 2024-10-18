import itertools
import json
from math import ceil, floor, log2
from PIL import Image
import numpy as np
from typing import Union



class Map():
    """Representation of gridded metric map
    
    Attributes:
    ---
    data : numpy.ndarray
        Data of gridded map.
    resolution : float
        Meters per pixel. Defaults to 0.1.

    Methods:
    ---
    resized(n: int):
        Generates and returns resized data array for faster computation.
    """
    def __init__(self, map: Union[str, list, np.ndarray], resolution: float=0.1) -> None:

        """Representation of gridded metric map

        Args:
        ---
            map (str|list|np.array): Data of gridded map as path to either a .json or a .png file or as list or np.array.
            resolution (float): Meters per pixel. Defaults to 0.1.

        Raises:
        ---
            TypeError: [description]
            TypeError: [description]
        """
        
        if isinstance(map, str):
            if map.endswith('.png'):
                image = Image.open(map)
                inputData = np.asarray(image)
                self._data = np.zeros(shape=[len(inputData), len(inputData[0])])


                for i in range(len(inputData)):
                    temp = np.zeros(shape=len(inputData[0]))
                    for j in range(len(inputData[0])):
                        if inputData[i][j][:3].mean() < 128: temp[j] = 1
                    self._data[i] = temp
                
            elif map.endswith('.json'):
                with open(map, "r") as f:
                    self._data = np.array(json.load(f)['data'])
            else: raise TypeError('map musst be .png or .json file!')
        elif isinstance(map, np.ndarray):
            self._data = map
        elif isinstance(map, list):
            self._data = np.array(map)
        else: raise TypeError('map musst .png, .json, list or numpy array!')
        
        
        self._resized_data = [self._data]
        
        self._resolution = float(resolution)
        
    @property
    def width(self) -> int:
        return self._data.shape[0]
        
    @property
    def height(self) -> int:
        return self._data.shape[1]
    
    @property
    def data(self) -> np.ndarray:
        return self._data
    
    @property
    def resolution(self) -> float:
        return self._resolution
    
    def resized(self, stage: int) -> np.ndarray:
        """Generates and returns resized data array for faster computation.
        All generated arrays will be stored and do not have to be generated again if needed multiple times.

        Args:
        ----
            s (int): Resize step: square width that gets summarized.

        Returns:
        ----
            np.ndarray: Resized array.
        """
        n = stage
        # n = floor(log2(s))
        
        while len(self._resized_data) <= n:
            l = len(self._resized_data)
            nn = 1 << l
            nn_squared = nn**2
            
            self._resized_data.append(np.zeros(shape=[ceil(self.width / nn), ceil(self.height / nn)]))
            for i, j in itertools.product(range(self._resized_data[-1].shape[0]), range(self._resized_data[-1].shape[1])):
                self._resized_data[-1][i][j] = (self._data[i << l:(i+1) << l, j << l:(j+1) << l] * nn_squared).mean()

        return self._resized_data[n]
