from Layer_1.driver.roboclaw_3 import Roboclaw
#import paho.mqtt.client as mqtt
from Layer_3.navigation.a_star import AStar
from Layer_3.navigation.obstacle import Obstacle
from Layer_1.sensor.sick import SICK
import time
import os

# Replace with your serial port and baud rate
roboclaw = Roboclaw("/dev/ttyACM0",115200)
#roboclaw = Roboclaw("/dev/ttyACM0",115200)

# Open the serial port
roboclaw.Open()

# Motor channel numbers
address = 0x80
#m2count = 0
#m1count = 0
fixed_value_90 = 5000
fixed_value_distance = 9700
sample_time = 0.1   
one_round_cm = 68     

def __init__(self, sick_instance):
    self.sick = sick_instance
    

def execute_movement_commands(commands,sick_instance):
    
    for action, value in commands:

        if action == 'right':
            right(int(value))
            Obstacle.update_clearance_flags()
            Obstacle.navigate_and_return()
            
        elif action == 'left':
            left(int(value))
            Obstacle.update_clearance_flags()
            Obstacle.navigate_and_return()

        elif action == 'forward':
            forward(int(value))
            obstacleavoid.update_clearance_flags()
            obstacleavoid.navigate_and_return()
        elif action == 'backward':
            backward(int(value))
            
        time.sleep(sample_time)

def right(Angle):
        #Angle= int(input(" At what angle do you want turn: "))
        m2count = int((Angle*fixed_value_90)/90)
        #print(m2count)
        roboclaw.ResetEncoders(0x80)
        roboclaw.ForwardM2(address,speed)
        roboclaw.BackwardM1(address,speed)
        
        while True :
            motor_2 = roboclaw.ReadEncM2(0x80)
            middle_value = int(motor_2[1]) #middle_value is the only encoder value other wise we got value (164,4700,0)
            #print(middle_value) 
            range1 =  m2count - plus
            range2 =  m2count + plus  
            if range1< middle_value < range2:
                roboclaw.ForwardM1(address,0)
                roboclaw.ForwardM2(address,0)
                break
        time.sleep(sample_time)

def left(Angle):
        m1count= int((Angle*fixed_value_90)/90)
        #print(m1count)
        roboclaw.ResetEncoders(0x80)
        roboclaw.ForwardM1(address,speed)
        roboclaw.BackwardM2(address,speed)
        while True :
                motor_1 = roboclaw.ReadEncM1(0x80)
                middle_value = int(motor_1[1])   
                range1 =  m1count - plus
                range2 =  m1count + plus   
                if range1< middle_value < range2:
                    roboclaw.ForwardM1(address,0)
                    roboclaw.ForwardM2(address,0)
                    break
        time.sleep(sample_time)

def forward(distance):
        #Drive both motors forward
        m1count= int(((distance*1.53)*fixed_value_distance)/one_round_cm)
        #print(m1count)
        roboclaw.ResetEncoders(0x80)
        roboclaw.ForwardM1(address,speed)
        roboclaw.ForwardM2(address,speed)
        while True :
                motor_1 = roboclaw.ReadEncM1(0x80)
                middle_value = int(motor_1[1])   
                range1 =  m1count - plus
                range2 =  m1count + plus   
                if range1< middle_value < range2:
                    roboclaw.ForwardM1(address,0)
                    roboclaw.ForwardM2(address,0)
                    break
        time.sleep(sample_time)

def backward(distance):
        #Drive both motors backward
        m1count= int(((distance*1.53)*fixed_value_distance)/one_round_cm)
        #print(m1count)
        roboclaw.ResetEncoders(0x80)
        roboclaw.BackwardM1(address,speed)
        roboclaw.BackwardM2(address,speed)
        while True :
                motor_1 = roboclaw.ReadEncM1(0x80)
                middle_value = int(motor_1[1])   
                range1 =  m1count - plus
                range2 =  m1count + plus   
                if range1< middle_value < range2:
                    roboclaw.ForwardM1(address,0)
                    roboclaw.ForwardM2(address,0)
                    break
        time.sleep(sample_time)

def stop():
        #Stop both motors
        roboclaw.ForwardM1(address,0)
        roboclaw.ForwardM2(address,0)

def rotate360():
        #for rotating 360 digree
        roboclaw.ResetEncoders(0x80)
        roboclaw.ForwardM1(address,speed)
        roboclaw.BackwardM2(address,speed)
        m1count= (fixed_value_90 * 4)
        
        while True :
                motor_1 = roboclaw.ReadEncM1(0x80)
                middle_value = int(motor_1[1])   
                range1 =  m1count - plus
                range2 =  m1count + plus   
                if range1< middle_value < range2:
                    roboclaw.ForwardM1(address,0)
                    roboclaw.ForwardM2(address,0)
                    break
        time.sleep(sample_time)
        
while True:
    #speed = int(input("Enter the speed: "))
    speed = 32 #constant speed
    if 0 < speed <= 100:
        plus = 10 if 0 < speed <= 32 else (40 if 33 <= speed <= 64 else (50 if 65 <= speed <= 100 else 0))
        break
    else:
        print("Invalid speed. Please enter a speed between 1 and 100.")
        
file_path = r'/home/indoor/Documents/Latest_1/rover/r_command.txt'
def main():
    with open(file_path, 'r') as file:
         for line in file:
            commands = [elem.split() for elem in line.strip().split('\n')]
            execute_movement_commands(commands)
            time.sleep(1)

if __name__ == "__main__":
        
    main()

'''with open(file_path, 'r') as file:
    for line in file:
        commands = line.strip().split()
        for i in range(0, len(commands), 4):
            command_group = commands[i:i+4]
            execute_movement_commands(command_group)
            time.sleep(1)


        
    
while True:
        userio = input("What's your option (forward,backword,right,left,stop,360): ")

        if userio in {"right","left"}:
                angle_input = int(input(" At what angle do you want turn: "))
                if userio == "right":
                        right(angle_input)
                elif userio == "left":
                        left(angle_input)
        
        elif userio in {"forward","backward"}:
                distance_input = int(input(" enter the distance: "))
                if userio == "forward":
                        forward(distance_input)
                elif userio == "backward":
                        backward(distance_input)
                        
        match userio:

                        case "stop":
                                stop()

                        case "360":
                                rotate360()
                        
'''''
