
import json
from datetime import datetime
import time
import numpy as np
import serial
import math
from Layer_1.driver.roboclaw_3 import Roboclaw
from Layer_1.driver.robot_move import *
from Layer_3.navigation.obstacle import *
from Layer_1.sensor.sick import SICK
from runnable_example1 import NavigationSystem
from matplotlib import pyplot as plt
import subprocess
#from Navigator.Navigator import Navigator
#from Layers.L2_Data.pub_data_handler import Pub_Handler

#from Layers.L3_protocols.spi import SPI
#from helper import *
#from Layer_1.driver.different_speed import RoboAngle

#roboclaw = Roboclaw(comport="/dev/ttyACM0",rate=115200)

class AppCommand:

    '''def __init__(self,port,baudrate,address):
        self.serial_port = serial.Serial(port, baudrate)
        self.address = address

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

270
275
270
270
270
275
275ort.close()'''


    def worker(self, q1, q2):
        #q1 - que mqtt q2-app command
        #roboclaw.Open()
        sick_instance= SICK(port="/dev/ttyUSB1", debug=True)
        obstacle_avoider = Obstacle(sick_instance) 
    
        #self.appCommand = AppCommand(port, baudrate, address)

        #roboclaw = Roboclaw(comport="/dev/ttyACM0",rate=115200)
        while True:
            try:
                command = q1.get()
                print(command)
                # convert string to  object
                json_object = json.loads(command)

                obstacle_avoider.update_clearance_flags()

                if not obstacle_avoider.straight_clear:
                    print("Obstacle detected, initiating avoidance maneuver.")
                    obstacle_avoider.navigate_and_return()
                else:    

                # Check data type coming from APP
                    if not (json_object.get("botCommand") is None):
                        print("botCommand received: {}".format(json_object["botCommand"]))
                        speed=json_object.get("botCommand")

                        if (json_object.get("botCommand")%16)==1:
                            #forward
                            RobotMove.forward(0x80,speed)
                            print("moving fwd")

                        elif json_object.get("botCommand")%16==2:
                            RobotMove.backward(0x80,speed)
                            # Drive both motors in reverse
                            print("moving back")

                        elif json_object.get("botCommand")%16==8:
                            RobotMove.right(0x80,speed)
                            # Drive both motors in reverse
                            print("moving right")

                        elif json_object.get("botCommand")%16==4:
                            RobotMove.left(0x80,speed)
                            # Drive both motors in reverse
                    
                            print("moving left")

                        elif (json_object.get("botCommand")% 16)==0:
                            RobotMove.stop(0x80)
                            
                            #time.sleep(5)



                    elif not (json_object.get("autoMode") is None):
                        print("autoMode received: {}".format(json_object["autoMode"]))
                        # self.spi.txSpi(int(json_object["autoMode"]))
                        # Assuming autoMode initiates navigation
                        # Configure your map and point cloud paths and target here
                        if (json_object.get("autoMode"))==253:
                            map_file = 'maps/map6_small.json'
                            point_cloud_file = 'maps/map6_small_225_297_0.json'
                            target_x, target_y = 26, 50.9  # Example target
                            navigation_system = NavigationSystem(
                                map_file=map_file,
                                point_cloud_file=point_cloud_file,
                                target_x=target_x,
                                target_y=target_y
                            )
                            #path = navigation_system.get_path()
                            #navigation_system.visualize_path()
                            subprocess.Popen(['python3','runnable_example1.py'])
                            subprocess.Popen(['python3','different_speed.py'])

                            #navigation_system.run_different_speed_script()
                        else:
                            print("NO auto command")   
                    
                        #autorobo =RoboAngle(port="/dev/ttyACM0",baud_rate=115200)
                        #file_path = r'C:\Users\dpvas\Desktop\Application_Software\r_command.txt'
                        #autorobo.main(file_path)
                        
                
                    elif not (json_object.get("manualMode") is None):
                        print("manualMode received: {}".format(json_object["manualMode"]))
                        #self.spi.txSpi(int(json_object["manualMode"]))

                    elif not (json_object.get("targetPosition") is None):
                        q2.put(json_object["targetPosition"])
                        

                    else:
                        print("not a valid Json format!")##
 
            except KeyboardInterrupt:
                print("exiting")


class AppData:
    def __init__(self) -> None:port,baudrate,address
        # self.datarefreshRate = 30

    def uploader(self, dataList):
        print(dataList)

        if dataList[0] < 400:
            Ultrasonic1 = dataList[0]
        elif dataList[1] < 400:
            Ultrasonic2 = dataList[1]
        elif dataList[2] < 360:
            heading = dataList[2]

        '''
        # Dictionary
        msg_dict = {
            "topic": "/bot/data",
            "distance": Ultrasonic1,
            "direction": heading,
        }
        print(msg_dict)'''

        # send msg to MQTT broaker
        # time.sleep(self.datarefreshRate)
        # self.mqtt.data_handler(msg_dict)

    def worker(self):
        flag = False
        counter = 0
        dataList = []
        while True:
            try:
                # Read data from SPI
                val = self.spi.rxpi()
                #print("val is: ")
                #print(val)
                if flag == True:
                    #print("flag = true!")
                    dataList.append(val)
                    if counter == 8:
                        #print("list full")
                        print(dataList)
                        int1 =  dataList[3]<<8
                        int1 |= dataList[2]
                        int2 =  dataList[5]<<8
                        int2 |= dataList[4]
                        int3 =  dataList[7]<<8
                        int3 |= dataList[6]
                        print(int1,int2,int3)
                        dataList = [int1,int2,int3]
                        self.uploader(dataList)
                        counter = 0
                        flag = False
                        dataList.clear()
                    counter+=1
                json_object = json.loads(command)

                if val == 89:
                    #print("89 detected")
                    flag = True

                time.sleep(0.1)

            except Exception as e:
                print(e)


class Navigator:
    def __init__(self) -> None:
        self.mqtt = Pub_Handler()

    def autonomousNavigator(self, q2):
        try:
            """Once set the target position, this function will receive
            the value and set it to algorithm to start."""
            targetPosition = q2.get()
            print(targetPosition)

            """with open(smallMap_path(), "r") as f:
                mapData = json.load(f)['data']

            with open(polarMap_path(), "r") as f:
                jsonData = json.load(f)
                navigator = Navigator(point_cloud_polar, position_map, path_map, target) ->                 json_object = json.loads(command)
None:
                startTime = datetime.now()
                path = navigator.generate_path()
                stopTime = datetime.now()
                timeTaken = stopTime - startTime

                direction = navigator.get_orientation()

                # Publish the initial direction to app
                msg_dict = {
                    "topic": '/bot/data',
                    "direction": direction
                }

                self.mqtt.data_handler(msg_dict)"""

        except Exception as e:
            print("error in navigator library!: {}".format(e))

    def worker(self, q2):
        while True:
            try:
                self.autonomousNavigator(q2)

            except KeyboardInterrupt:
                print("exiting navigator with error!")
