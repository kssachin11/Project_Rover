import itertools
from matplotlib import pyplot as plt
import numpy as np
from cmath import rect
from math import pi
from copy import copy
from typing import List

# from matplotlib import pyplot as plt
import numpy as np
from heapq import nsmallest
from pyoverload import overload
from Layer_3.navigation.map import Map

from Layer_3.navigation.metric_position import MetricPosition
from Layer_3.navigation.point import Point
from Layer_3.navigation.polar import Polar
from Layer_3.navigation.polar_calculator import PolarCalculator


class NoPathFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AStar():
    def __init__(self, start: MetricPosition, target: MetricPosition, map: Map) -> None:
        """A*-algorithm
        
        Args:
        ---
            start (MetricPosition): (22.5,29.70)
            target (MetricPosition): (28,50)
            map (Map): Map of environment.
            F
        Returns:
        ----------
            None
        """
        self.path = []
        self.coordinates_list = []
        self.start = Point(position=start, map=map)
        self.target = Point(position=target, map=map)
        self._start_direction = start.alpha
        self.start.calc_approx_distance(self.target)
        self.matrix = np.array(map._data, dtype=bool)
        self.visited = np.zeros(shape=map._data.shape)
        self.visited_bool = np.array(map._data)
        self.open_list = np.zeros(shape=map._data.shape)
        self.path_matrix = np.array(self.matrix, dtype=int)
        self.points = []
        self.meters_per_pixel = map._resolution
        self.distance = 0
        
  #  def get_coordinates_list(self) -> List[List[int]]:
        """Returns the list of coordinates.

        Returns:
        ---
            List[List[int]]: List of coordinates.
        """
   #     return self.coordinates_list
    # After running the A* algorithm

    def run(self) -> List[Polar]:
        """Executes A*-algorithm.

        Raises:
        ---
            NoPathFoundError: [description]

        Returns:
        ---
            list[Polar]: List of polar coordinates describing the path to travel relatively to initial or recent orientation.
        """
        pathFound = True
        self.points.append(self.start)
        while len(self.points) > 0: 
            point = nsmallest(1, self.points)[0]
            if point == self.target:
                pathFound = True
                break
            self._set_visited(point)

            for step in [Point(1, 0), Point(0, 1), Point(0, -1), Point(-1, 0), Point(1, 1), Point(1, -1), Point(-1, 1), Point(-1, -1)]:
                if self._check_matrices(point, step):
                    next_point = Point.create_new_point(point=point, step=step, target=self.target)
                    self.points.append(next_point)
                    self._set_open_list(next_point)
            self.points.remove(point)

        if pathFound:
            self._generate_path(point)
            polar_calculator = PolarCalculator()
            polar_path = polar_calculator._calc_polar_path(self.path, self._start_direction)
            
            #polar_calculator = PolarCalculator(self.path, self._start_direction)
            #polar_path = polar_calculator.generate_path()
    
            # Reverse the coordinates_list
            reversed_coordinates_list = self.coordinates_list[::-1]
                
            return reversed_coordinates_list

            self.path = [self.start, self.target]

            self._mark_waypoints()
            raise NoPathFoundError()    
    
    
    def _generate_path(self, point: Point) -> None:
        """Generates path of single waypoints from detected route. Path is generated backward from target to start point.

        Args:
        ---
            point (Point): Last waypoint of path.
            
        Returns:
        ----------
            None
        """
        last_point = point  # Initialize last_point here

        while point.parent:
            next_point = point.parent
            if (point - last_point).get_coords() != (next_point - point).get_coords():
                self.path.append(point)
            if self._get_number_of_surrounding_pixels(last_point) != self._get_number_of_surrounding_pixels(point):
                point.is_edge = True
                self.path.append(point)
            self._set_path(point)     
            last_point = point
            point = next_point
        self.path.append(self.start)

        # Reverse the path to have it from start to target
        self.path = self.path[::-1]

        # Update path_matrix in reverse order
        reversed_path = self.path[::-1]
        for i, point in enumerate(reversed_path[:-1]):
            self.path_matrix[point.x][point.y] = i + 2  # Update path_matrix in reverse order

        self._calc_distance()
        self._mark_waypoints()


    @overload
    def _shorten_path(self, path: List[Point] = None) -> List[Point]:
        """Removes unnecessary waypoints from path.

        Args:
        ---
            path (list[Point], optional): Path to be shortened. Defaults to None.

        Returns:
        ---
            list[Point]: Shortened path.
        """
        change = True
        if path: path = copy(path)
        else: path = copy(self.path)

        while change:
            change = False

            i = 1
            while i < len(path) - 1:
                while self._check_directly(path[i-1], path[i+1]):
                    if path[i].is_edge: 
                        path[i:] = self._shorten_path(path[i:])
                        path[i].is_edge = False
                    else:
                        del path[i]
                        change = True
                        if i >= len(path) - 1: break
                i += 1
        return path
    

    def _calc_distance(self):
        """Calculates length of determined path.
            
        Returns:
        ----------
            None
        """
        self.distance = 0
        for i in range(1, len(self.path)):
            self.distance += (self.path[i-1] - self.path[i]).abs()
            #print(self.distance)
        self.distance *= self.meters_per_pixel
        

    def _mark_waypoints(self) -> None:
        """Marks waypoints in path_matrix.
            
        Returns:
        ----------
            None
        """
        for point in self.path:
            self._mark_waypoint(point)

    def _mark_waypoint(self, point: Point) -> None:
        """Marks single waypoint in path_matrix.
            
        Returns:
        ----------
            None
        """
        for i, j in itertools.product(range(1), range(1)):
            self.path_matrix[point.x + i][point.y + j] = 4
        

    def _check_matrices(self, start: Point, step: Point) -> bool:
        """Checks that the POI has not been visited, is not in a forbidden area, and is not on the openList. If point is on openList but new path is shorter, old entry is deleted.

        Args:
        ---
            start (Point): Point from where to reach next point.
            step (Point): Step to next point.

        Returns:
        ---
            bool: Point is visitable or not.
        """
        point = Point.create_new_point(start, step, self.target)
        if self.visited[point.x][point.y]: return False                 # already visited                          -> False
        if self.matrix[point.x][point.y]: return False                  # not allowed area                          -> False
        if self.open_list[point.x][point.y] != 0:                       # on open list                              -> False
            if self.open_list[point.x][point.y] > point.approx_distance: # on open list but new path is shorter      -> True
                self.open_list[point.x][point.y] = 0                                                                # delete from open list
                self.points.remove([item for item in self.points if item.x == point.x and item.y == point.y][0])    # delete from points
                return True
            return False
        return True

    def _check_directly(self, start: Point, target: Point) -> bool:
        """Checks if target point is directly reachable from start point without passing forbidden areas or obstacles.

        Args:
        ---
            start (Point): Start point in gridded area.
            target (Point): Target point in gridded area.

        Returns:
        ---
            bool: Point is directly reachable or not.
        """
        position = copy(start)
        i = 1
        direction = (target - start).phase()
        while (position - target).abs() > 1:
            step = rect(i, direction)
            position = start + step
            if self.matrix[position.x][position.y]: return False
            i += 1
        return True

    counter = 0

    def _set_visited(self, point: Point) -> None:
        """Marks POI as visited.

        Args:
        ---
            point (Point): POI
            
        Returns:
        ----------
            None
        """
        self.visited[point.x][point.y] = point.approx_distance
        self.visited_bool[point.x][point.y] = True
        
        # if not self.counter % 1000:
        #     plt.imshow(self.visited_bool)
        #     plt.pause(0.1)
        # self.counter += 1

    def _set_open_list(self, point: Point) -> None:
        """Sets POI to openList.

        Args:
        ---
            point (Point): POI
            
        Returns:
        ----------
            None
        """
        self.open_list[point.x][point.y] = point.approx_distance

    def _set_path(self, point: Point) -> None:
        """Marks POI as belonging to path.

        Args:
        ---
            point (Point): POI
            
        Returns:
        ----------
            None
        """
        self.path_matrix[point.x][point.y] = 3 if point.is_edge else 2

        # Print the coordinates of the path point
        #self.coordinates_list.append([point.x, point.y])
        #print(f"[{point.x},{point.y}]")
        

    def _get_number_of_surrounding_pixels(self, point: Point) -> int:
        """Calculates number of not empty pixels around point.

        Returns:
        ---
            int: [description]
        """
        return int(np.sum(self.matrix[
            int(point.x - 1) : int(point.x + 2),
            int(point.y - 1) : int(point.y + 2)
        ]))


   