from Layer_3.navigation.a_star import AStar
from Layer_3.navigation.map import Map
from Layer_3.navigation.metric_position import MetricPosition
from Layer_3.navigation.point_cloud_cartesian import PointCloudCartesian
from Layer_3.navigation.polar import Polar
from typing import List, Union


class Navigator():
    def __init__(self, point_cloud_polar: List[Union[Polar, List]], position_map: Map, path_map: Map, target: MetricPosition, stages: int = 4, threshold: float = 0.7) -> None:
        """_summary_

        Args:
            point_cloud_polar (list[any): Point Cloud.
            position_map (Map): Map of environment without forbidden areas.
            path_map (Map): Map of environment with forbidden areas.
            target (MetricPosition): Target position.
            stages (int, optional): Convolution stages. Defaults to 4.
            threshold (float, optional): Threshold for convolution. Defaults to 0.7.
        """
        self._point_cloud_cartesian = PointCloudCartesian(point_cloud_polar=point_cloud_polar)
        self._position_map = position_map
        self._path_map = path_map
        self._target = target
        self._stages = stages
        self._threshold = threshold
        self._aStar = None
        self._path = None
        self._position = None
        
    def determine_position(self) -> MetricPosition:
        """Determines position based on detected point cloud.

        Returns:
            MetricPosition: Position of point cloud origin.
        """
        self._position = self._point_cloud_cartesian.determine_map_position(self._position_map, threshold=self._threshold)
        return self._position

    def generate_path(self) -> List[Polar]:
        """Generates Path.

        Returns:
            list[Polar]: List of polar coordinates describing the path to the target position.
        """
        self._astar = AStar(start=self.get_position(), target=self._target, map=self._path_map)
        self._path = self._astar.run()
        return self._path
    
    def get_position(self) -> MetricPosition:
        """Returns position. Calls determine_position() if necessary.

        Returns:
            MetricPosition: Position of point cloud origin.
        """
        return self._position if self._position else self.determine_position()
    
    def get_path(self):
        """Returns path. Calls generate_path() if necessary.

        Returns:
            list[Polar]: List of polar coordinates describing the path to the target position.
        """
        return self._path if self._path else self.generate_path()
    
    def get_orientation(self) -> float:
        """Returns detected orientation. Calls determine_position() if necessary.

        Returns:
            float: Angle of orientation in deg.
        """
        return self._position.alpha if self._position else self.determine_position().alpha
