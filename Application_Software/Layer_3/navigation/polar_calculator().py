from typing import List
from math import pi
from copy import copy
from Layer_3.navigation.metric_position import MetricPosition
from Layer_3.navigation.point import Point
from Layer_3.navigation.polar import *

class PolarCalculator:
    def __init__(self, path: List[Point], start_direction: float) -> None:
        self.path = path
        self.start_direction = start_direction
        self.polar_path = []

    def generate_path(self) -> List[Polar]:
        last_direction = self.start_direction
        with open('r_command.txt', 'w') as file:
            smoothed_path = self._smooth_path(self.path)  # Smooth the path
            for i in range(1, len(smoothed_path)):
                step = smoothed_path[i] - smoothed_path[i-1]
                target_direction = (step.phase() * 180/pi) % 360
                last_direction = (last_direction + 360) % 360
                target_direction = (target_direction + 360) % 360
                angle_diff = (target_direction - last_direction + 360) % 360
                if angle_diff <= 180:
                    turn_angle = angle_diff
                    turn_type = "right"
                else:
                    turn_angle = 360 - angle_diff
                    turn_type = "left"
                if abs(turn_angle - 180) < 1e-5:
                    movement_type = "backward" if step.abs() < 0 else "forward"
                else:
                    movement_type = "forward"
                self.polar_path.append(
                    Polar(phase=round(turn_angle),
                        abs=round(step.abs()),
                        turn=turn_type,
                        movement=movement_type)
                )
                file.write(f"{turn_type} {round(turn_angle)}\n")
                file.write(f"{movement_type} {round(step.abs())}\n")
                last_direction = target_direction
        return self.polar_path

    def _smooth_path(self, path: List[Point], epsilon: float = 1.0) -> List[Point]:
        """Applies Douglas-Peucker algorithm to smooth the path."""
        if len(path) < 3:
            return path
        dmax = 0
        index = 0
        end = len(path) - 1
        for i in range(1, end):
            d = self._perpendicular_distance(path[i], path[0], path[end])
            if d > dmax:
                index = i
                dmax = d
        if dmax > epsilon:
            results1 = self._smooth_path(path[:index + 1], epsilon)
            results2 = self._smooth_path(path[index:], epsilon)
            results1.pop()  # Remove duplicate point
            return results1 + results2
        else:
            return [path[0], path[end]]

    def _perpendicular_distance(self, point: Point, start: Point, end: Point) -> float:
        """Calculates perpendicular distance from point to line segment."""
        if start == end:
            return (point - start).abs()
        return abs(((end.y - start.y) * point.x - (end.x - start.x) * point.y + end.x * start.y - end.y * start.x) / ((end - start).abs()))