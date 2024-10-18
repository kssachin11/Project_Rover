from copy import copy
from math import atan, pi, sqrt
from typing import Any, TypeVar
import numpy as np
from pyoverload import overload
from Layer_3.navigation.map import Map
from typing import List


from Layer_3.navigation.metric_position import MetricPosition

TPoint = TypeVar('TPoint', bound='Point')

class Point():
    """Point in gridded environment.

    Attributes:
    ---
    x : int
        x-coordinate
    y : int
        y-coordinate
    traveled_distance : float
        Distance between start point and this point over each and every intermediate point.
    approx_distance : float
        Sum of traveled distance and direct distance between this point and target point.
    parent : Point
        Point from where to reach this point.
    is_edge : bool
        If point is located next the edge of a forbidden or blocked area.
    """
    
    @overload
    def __init__(self, x: int, y: int, traveled_distance: float=0, approx_distance: float=np.Infinity, parent: TPoint=None, is_edge: bool=False) -> None:
        """Point in gridded environment.

        Args:
        ----------
            x (int): x-coordinate
            y (int): y-coordinate
            traveled_distance (float): Distance between start point and this point over each and every intermediate point.
            approx_distance (float): Sum of traveled distance and direct distance between this point and target point.
            parent (Point): Point from where to reach this point.
            is_edge (bool): If point is located next the edge of a forbidden or blocked area.
            
        Returns:
        ----------
            None
        """
        self.x = x
        self.y = y
        self.traveled_distance = traveled_distance
        self.approx_distance = approx_distance
        self.parent = parent
        self.is_edge = is_edge
        
    @overload
    def __init__(self, x: Any, y: Any, traveled_distance: float=0, approx_distance: float=np.Infinity, parent: TPoint=None, is_edge: bool=False) -> None:
        """Point in gridded environment.

        Args:
        ----------
            x (Any): x-coordinate
            y (Any): y-coordinate
            traveled_distance (float): Distance between start point and this point over each and every intermediate point.
            approx_distance (float): Sum of traveled distance and direct distance between this point and target point.
            parent (Point): Point from where to reach this point.
            is_edge (bool): If point is located next the edge of a forbidden or blocked area.
            
        Returns:
        ----------
            None
        """
        self.x = int(x)
        self.y = int(y)
        self.traveled_distance = traveled_distance
        self.approx_distance = approx_distance
        self.parent = parent
        self.is_edge = is_edge

    @overload
    def __init__(self, position: MetricPosition, map: Map, traveled_distance: float=0, approx_distance: float=np.Infinity, parent: TPoint=None, is_edge: bool=False) -> None:
        """Point in gridded environment.

        Args:
        ----------
            position (MetricPosition): Coordinate in gridded map.
            map (Map): Map.
        OR
            x (int): x-coordinate
            y (int): y-coordinate
                
            traveled_distance (float): Distance between start point and this point over each and every intermediate point.
            approx_distance (float): Sum of traveled distance and direct distance between this point and target point.
            parent (Point): Point from where to reach this point.
            is_edge (bool): If point is located next the edge of a forbidden or blocked area.
            
        Returns:
        ----------
            None
        """
        self.x, self.y, _, _ = (position / map.resolution).getCoordinates()
        self.traveled_distance = traveled_distance
        self.approx_distance = approx_distance
        self.parent = parent
        self.is_edge = is_edge
    
    def __lt__(self, other: TPoint):
        return self.approx_distance < other.approx_distance

    def __gt__(self, other):
        return self.approx_distance > other.approx_distance

    def __add__(self, other):
        point = copy(self)
        if isinstance(other, Point):
            point.x += (other.x)
            point.y += (other.y)
        elif isinstance(other, List):
            point.x += (other[0])
            point.y += (other[1])
        elif isinstance(other, complex):
            point.x += (other.real)
            point.y += (other.imag)
        else:
            raise Exception()
        point.x = round(point.x)
        point.y = round(point.y)
        point.traveled_distance += (point - other).abs()
        return point

    def __sub__(self, other):
        point = copy(self)
        if isinstance(other, Point):
            point.x -= (other.x)
            point.y -= (other.y)
        elif isinstance(other, List):
            point.x -= (other[0])
            point.y -= (other[1])
        elif isinstance(other, complex):
            point.x -= (other.real)
            point.y -= (other.imag)
        else:
            raise Exception()
        point.x = round(point.x)
        point.y = round(point.y)
        return point

    def abs(self) -> float:
        """Absolut length of vector.

        Returns:
        ----------
            float: Absolut length of vector.
        """
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def phase(self) -> float:
        """Phase of vector.

        Returns:
        ----------
            float: Phase of vector.
        """
        if self.x > 0: 
            return atan(self.y / self.x) % (2 * pi)
        elif self.x == 0 and self.y > 0: 
            return pi / 2
        elif self.x == 0 and self.y < 0: 
            return 3 * pi / 2
        elif self.x == 0 and self.y == 0: 
            return 0
        else: 
            return atan(self.y / self.x) + pi

    @staticmethod
    def create_new_point(point: TPoint, step: TPoint, target: TPoint) -> TPoint:
        """Creates new point at position of point + step with traveled distance of point + length of step.

        Args:
        ----------
            point (Point): Actual point.
            step (Point): Step to next point.
            target (Point): Target to go to.

        Returns:
        ----------
            Point: New point.
        """
        newPoint = point + step
        newPoint.parent = point
        newPoint.traveled_distance = point.traveled_distance + step.abs()
        newPoint.calc_approx_distance(target)
        return newPoint
        
    def calc_approx_distance(self, target: TPoint) -> None:
        """Calculates approximated distance as traveled distance to this point plus direct distance to target.

        Args:
        ----------
            target (Point): Point to go to.
            
        Returns:
        ----------
            None
        """
        self.approx_distance = self.traveled_distance + sqrt(pow(self.x - target.x, 2) + pow(self.y - target.y, 2))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        """return f'Point - position: ({self.x:4}, {self.y:4}), traveled_distance: {self.traveled_distance:8.3f}, approx_distance {self.approx_distance:8.3f}'"""
        return f'Point: ({self.x:4}, {self.y:4})'

    def get_coords(self) -> List[int]:
        """Array of points coordinates.

        Returns:
        ----------
            list[int]: Array of points coordinates.
        """
        return [self.x, self.y]

    def coords_to_str(self) -> str:
        """Generates string representation of coordinates.

        Returns:
        ----------
            str: String representation of coordinates.
        """
        return f'({self.x:4}, {self.y:4})'

    def get_environment(self) -> List[List[int]]:
        """Keine Ahnung, was das Ding macht.

        Returns:
        ----------
            list[list[int]]: [description]
        """
        raise Exception('Nachgucken, was die Funktion macht!')
        return [[self.x, 0], [0, self.y]]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = int(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = int(value)
