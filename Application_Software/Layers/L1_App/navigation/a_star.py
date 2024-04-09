import itertools
from matplotlib import pyplot as plt
import numpy as np
from cmath import rect
from math import pi
from copy import copy
# from matplotlib import pyplot as plt
import numpy as np
from heapq import nsmallest
from pyoverload import overload
from Layers.L1_App.navigation.map import Map

from Layers.L1_App.navigation.metric_position import MetricPosition
from Layers.L1_App.navigation.point import Point
from Layers.L1_App.navigation.polar import Polar


class NoPathFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AStar():
    def __init__(self, start: MetricPosition, target: MetricPosition, map: Map) -> None:
        """A*-algorithm
        
        Args:
        ---
            start (MetricPosition): Start coordinate.
            target (MetricPosition): Target coordinate.
            map (Map): Map of environment.
            
        Returns:
        ----------
            None
        """
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

    def run(self) -> list[Polar]:
        """Executes A*-algorithm.

        Raises:
        ---
            NoPathFoundError: [description]

        Returns:
        ---
            list[Polar]: List of polar coordinates describing the path to travel relatively to initial or recent orientation.
        """
        pathFound = False
        self.points.append(self.start)
        while len(self.points) > 0: 
            point = nsmallest(1, self.points)[0]            # get point with smallest distance to target
            if point == self.target:            # break if point is target -> path found
                pathFound = True
                break                                   
            self._set_visited(point)                         # mark coordinate as visited

            # check surrounding coordinates
            for step in [Point(1, 0), Point(0, 1), Point(0, -1), Point(-1, 0), Point(1, 1), Point(1, -1), Point(-1, 1), Point(-1, -1)]:
                    if self._check_matrices(point, step):    # check if point is reachable
                        next_point = Point.create_new_point(point=point, step=step, target=self.target)    # create new point from actual point and step
                        self.points.append(next_point)       # add new point to reachable points list
                        self._set_open_list(next_point)        # add new point to open list
            self.points.remove(point)                       # remove actual point from reachable points list

        if pathFound:
            self._generate_path(point)
            return self._calc_polar_path()
        self.path = [self.start, self.target]
        self._mark_waypoints()
        raise NoPathFoundError()
    
    def _generate_path(self, point: Point) -> None:
        """Generates path of single waypoints from detected route. Path is generated backwards from target to start point.

        Args:
        ---
            point (Point): Last waypoint of path.
            
        Returns:
        ----------
            None
        """
        self.path = [point]
        last_point = point
        point = point.parent
        while point.parent:
            next_point = point.parent
            if (point - last_point).get_coords() != (next_point - point).get_coords():  # pick out points between start and end
                self.path.append(point)                                             # point of single-direction sequence            # .
            if self._get_number_of_surrounding_pixels(last_point) != self._get_number_of_surrounding_pixels(point):
                point.is_edge = True
                self.path.append(point)
            self._set_path(point)     
            last_point = point
            point = next_point
        self.path.append(self.start)

        self.path = self.path[::-1]

        self._shorten_path()
        self._calc_distance()
        self._mark_waypoints()

    @overload
    def _shorten_path(self, path: list[Point] = None) -> list[Point]:
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

    @overload
    def _calc_polar_path(self, direction: float) -> list[Polar]:
        """Generates polar path from Cartesian path.

        Args:
        ---
            direction (float): Orientation of last step.

        Returns:
        ---
            list[Polar]: List of polar coordinates, oriented relatively to each other or the initial orientation.
        """
        self.polar_path = []
        last_direction = direction
        for i in range(1, len(self.path)):
            step = self.path[i] - self.path[i-1]
            direction = 180 - step.phase() * 180/pi
            self.polar_path.append(
                Polar(phase=round((direction - last_direction) % 360),
                      abs=round(step.abs()))
                )
            last_direction = direction
        return self.polar_path

    @overload
    def _calc_polar_path(self) -> list[Polar]:
        """Generates polar path from Cartesian path.

        Returns:
        ---
            list[Polar]: List of polar coordinates, oriented relatively to each other or the initial orientation.
        """
        self.polar_path = []
        return self._calc_polar_path(self._start_direction)