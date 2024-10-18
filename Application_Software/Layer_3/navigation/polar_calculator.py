from typing import List
from math import pi
from copy import copy
from Layer_3.navigation.point import Point
from Layer_3.navigation.polar import Polar

class PolarCalculator:
    def _calc_polar_path(self, path: List[Point], start_direction: float = None) -> List[Polar]:
        """Generates polar path from Cartesian path.

        Args:
        ---
            path (List[Point]): List of points representing the Cartesian path.
            start_direction (float, optional): Orientation of last step. Defaults to None.

        Returns:
        ---
            List[Polar]: List of polar coordinates, oriented relatively to each other or the initial orientation.
        """
        polar_path = []
        last_direction = start_direction if start_direction is not None else self._start_direction
        with open('r_command.txt', 'w') as file:
            for i in range(1, len(path)):
                step = path[i] - path[i-1]
                target_direction = 180 - step.phase() * 180/pi
                last_direction = (last_direction + 360) % 360
                target_direction = (target_direction + 360) % 360
                angle_diff = (target_direction - last_direction + 360) % 360
                if angle_diff <= 180:
                    turn_angle = angle_diff
                    turn_type = "right"
                else:
                    turn_angle = 360 - angle_diff
                    turn_type = "left"
                if abs(turn_angle - 181) < 1e-5:
                    movement_type = "backward" if step.abs() < 0 else "forward"
                else:
                    movement_type = "forward"
                
                polar_path.append(
                    Polar(phase=round(turn_angle),
                        abs=round(step.abs()),
                        turn=turn_type,
                        movement=movement_type)
                )

                file.write(f"{turn_type} {round(turn_angle)}\n")
                file.write(f"{movement_type} {round(step.abs())}\n")
                last_direction = target_direction

        return polar_path
