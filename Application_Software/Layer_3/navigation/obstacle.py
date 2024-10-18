from Layer_1.sensor.sick import*
from Layer_1.driver.robot_move import *
from Layer_1.driver.different_speed import *
import math
import time
speed=32
class Obstacle():
    def __init__(self, sick_instance):
        self.sick = sick_instance
        self.obstacle_distance_threshold = 60
        self.safe_turn_distance = 60 
        self.safe_turn_left_range = (120, 180)  
        self.safe_turn_right_range = (0, 60)  

    def update_clearance_flags(self):
        """Update clearance flags based on current sensor readings."""
        polar_coords = self.sick.polar
        self.straight_clear = all(distance > self.obstacle_distance_threshold for distance, angle in polar_coords if 60 <= angle <= 120)
        self.left_clear = all(distance > self.safe_turn_distance for distance, angle in polar_coords if angle in self.safe_turn_left_range)
        self.right_clear = all(distance > self.safe_turn_distance for distance, angle in polar_coords if angle in self.safe_turn_right_range)

    def navigate_and_return(self):
        """Main navigation loop with trajectory correction to return to original path."""
        self.update_clearance_flags()  # Initial clearance check

        while True:  # Main loop 
            if self.straight_clear:
                print('No obstacles detected, moving towards target.')
                break
                
                
            elif self.left_clear or self.right_clear:
                if self.right_clear:
                    self.avoid_obstacle_and_return(direction="right")
                elif self.left_clear:
                    self.avoid_obstacle_and_return(direction="left")
            else:
                print("Obstacles detected on all sides. Stopping and reassessing.")
                RobotMove.backward(speed)
                time.sleep(0.5)
                if self.left_clear or self.right_clear:
                    if self.right_clear:
                        self.avoid_obstacle_and_return(direction="right")
                    elif self.left_clear:
                        self.avoid_obstacle_and_return(direction="left")  
                self.update_clearance_flags()
                  
            self.sick.get_frame()
            self.sick.calc_distances()
            self.update_clearance_flags()

    def avoid_obstacle_and_return(self, direction):
        """Avoids obstacle with continuous sensor checks and an intention to return to the original path."""
        print(f"Moving {direction} to avoid obstacle.")
        angle_to_turn = 90

        # Turn 1
        self.perform_turn(direction, angle_to_turn)
        start_time = time.time()
        self.move_forward_with_checks()
        move_time = time.time() - start_time
        
        # Turn 2
        opposite_direction = "left" if direction == "right" else "right"
        self.perform_turn(opposite_direction, angle_to_turn)
        RobotMove.forward(speed)
        time.sleep(4)
        self.move_forward_with_checks()

        # Turn 3
        self.perform_turn(opposite_direction, angle_to_turn)
        RobotMove.forward(speed)
        time.sleep(move_time)

        # Turn 4
        self.perform_turn(direction, angle_to_turn)
        print("Returned to original trajectory after avoiding obstacle.")

    def perform_turn(self, direction, angle):
        if direction == "right":
            RoboAngle.right(Angle=angle)
        elif direction == "left":
            RoboAngle.left(Angle=angle)
        
        self.sick.get_frame()
        self.sick.calc_distances()
        self.update_clearance_flags()
        
    def move_forward_with_checks(self):
        while True:
            self.sick.get_frame()
            self.sick.calc_distances()
            self.update_clearance_flags()
            if not self.left_clear and self.right_clear:
                RobotMove.forward(speed)
            else:
                RobotMove.forward(speed)
                time.sleep(1.5)
                break

if __name__ == "__main__":
    sick_instance = SICK(port="/dev/ttyUSB1", debug=True)
    rover_controller = Obstacle(sick_instance)

    while True:
        sick_instance.get_frame()
        sick_instance.calc_distances()
        rover_controller.navigate_and_return()
