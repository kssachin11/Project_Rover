import serial
import time
import json
from Layer_1.driver.roboclaw_3 import Roboclaw  # Assuming you have the 'roboclaw' module installed
roboclaw = Roboclaw(comport="/dev/ttyACM0",rate=115200)
roboclaw.Open()
class RobotMove:
    def __init__(self, port, baudrate, address):
        self.serial_port = serial.Serial(port, baudrate)
        self.address = address
        self.roboclaw = Roboclaw("/dev/ttyACM0", 115200)  # Update the port and baudrate accordingly

    def send_command(self, command):
        # Send command to RoboClaw
        full_command = f"{self.address}{command}\r"
        self.serial_port.write(full_command.encode())

    def read_response(self):
        # Read and return response from RoboClaw
        response = self.serial_port.readline().decode().strip()
        return response

    def set_motor_speed(self, motor_channel, speed):
        # Command to set motor speed
        command = f"M{motor_channel} {speed}"
        self.send_command(command)
        response = self.read_response()
        print(f"Set Motor {motor_channel} Speed: {speed}, Response: {response}")

    def forward(self,speed):
        # Drive both motors forward
        
        print("hello")
        # time.sleep(2)
        roboclaw.ForwardM1(0x80, val=speed)
        roboclaw.ForwardM2(0x80, val=speed)
        print("Robot is moving forwardm1")
        # time.sleep(5)

    def backward(self,speed):
        # Drive both motors in reverse
        
        roboclaw.BackwardM1(0x80, val=speed)
        roboclaw.BackwardM2(0x80, val=speed)
        print("moving back")
        # time.sleep(5)

    def right(self,speed):
        # Drive both motors in reverse
        
        roboclaw.ForwardM1(0x80, val=speed)
        roboclaw.BackwardM2(0x80, val=speed)
        print("moving right")

    def left(self,speed):
        # Drive both motors in reverse
        
        roboclaw.ForwardM2(0x80, val=speed)
        roboclaw.BackwardM1(0x80, val=speed)
        print("moving left")

    def stop(self):
        roboclaw.ForwardM1(0x80,val=0)
        roboclaw.ForwardM2(0x80,val=0)
        roboclaw.BackwardM1(0x80,val=0)
        roboclaw.BackwardM2(0x80,val=0)
        # time.sleep(5)

    def close_connection(self):
        # Close the serial connection
        self.serial_port.close()


if __name__ == "__main__":
    # Example usage
    roboclaw = RobotMove(port="/dev/ttyACM0", baudrate=115200, address="0x80")
    roboclaw.forward()
    # Add more method calls as needed
    roboclaw.close_connection()
