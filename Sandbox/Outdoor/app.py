from audioop import avg
import json, time, os
from math import e
from datetime import datetime
from networkx import directed_combinatorial_laplacian_matrix
import numpy as np
from matplotlib import pyplot as plt
from helpers import *
from json.decoder import JSONDecodeError
from queue import Queue
from Layers.L2_Data.pub_data_handler import Pub_Handler
from Layers.L1_App.sensor.dgps.DGPS import connect_pksi_dgps
from Layers.L1_App.sensor.imu.gyroscpe import connect_pksi_INS
# import Layers.L1_App.driver.Rover as rover
from Layers.L1_App.navigation.create_map_network import MapHandler
#from Layers.L1_App.sensor.Laser.point_cloud import Laser as ls
#from Layers.L1_App.navigation.object_avoid_final import Object_avoid
from logger import Logger as log
class AppCommand:
    def __init__(self) -> None:
        """Init Roboclaw"""
        self.enableManual = 69
        #self.rover = rover()
        # check connection is working between Jetson and Roboclaw
    """ while True:
            if not self.spi.spiHandshake():
                print("SPI connection error, check wiring!")
                time.sleep(0.5)
            else:
                break """

    def worker(self, q1, q2):
        #print("Connected to mqtt")
        while True:
            try:
                command = q1.get()
                # convert string to  object
                json_object = json.loads(command)
                
                
                # print(json_object)
                # Check data type coming from APP
                if not (json_object.get("autoMode") is None):
                    print("autoMode received: {}".format(json_object["autoMode"]))
                    log().getLogger("AppCommand").info("autoMode received: {}".format(json_object["autoMode"]))
                    if not (json_object.get("tapPositon") is None):
                        print("targetLocation received: {}".format(json_object["tapPositon"]))
                        q2.put(json_object["tapPositon"])
                        log().getLogger("AppCommand").info("targetLocation received: {}".format(json_object["tapPositon"]))
                    else:
                        #print("No targetLocation received")
                        #log().getLogger("AppCommand").error("No targetLocation received")
                        pass
                    #
                elif not (json_object.get("manualMode") is None):
                    print("manualMode received: {}".format(json_object["manualMode"]))
                    log().getLogger("AppCommand").info("manualMode received: {}".format(json_object["manualMode"]))
                    
                    if not (json_object.get("botCommand") is None):
                        print("botCommand received: {}".format(json_object["botCommand"]))
                        log().getLogger("AppCommand").info("botCommand received: {}".format(json_object["botCommand"]))
                    
                        if json_object["botCommand"] == 17:
                            # rover.forward(33)
                            log().getLogger("AppCommand").info("Robot is moving forward")
                            print("Robot is moving forwardm1")
                        elif json_object["botCommand"] == 18:
                            # rover.backward(33)
                            log().getLogger("AppCommand").info("Robot is moving backward")
                            print("Robot is moving backward")
                        elif json_object["botCommand"] == 20:
                            # rover.right(90)
                            log().getLogger("AppCommand").info("Robot is moving right")
                            print("Robot is moving right")
                        elif json_object["botCommand"] == 24:
                            # rover.left(90)
                            log().getLogger("AppCommand").info("Robot is moving left")
                            print("Robot is moving left")
                        elif json_object["botCommand"] == 16:
                            # rover.stop()
                            print("Robot is stopped")
                            log().getLogger("AppCommand").info("Robot is stopped")
                        else:
                            print("Invalid command")
                            log().getLogger("AppCommand").error("Invalid command")
                    #print("no bot command")
                    else:
                        # print("No botCommand received")
                        log().getLogger("AppCommand").error("No botCommand received")
                    print("no bot command")
                elif not (json_object.get("targetLocation") is None):
                    print("targetLocation received: {}".format(json_object["targetLocation"]))
                    q2.put(json_object["targetLocation"])
                    log().getLogger("AppCommand").info("targetLocation received: {}".format(json_object["targetLocation"]))

                else:
                    print("not a valid Json format!")
                    log().getLogger("AppCommand").critical("not a valid Json format!")
                print("Queue 1: ", q1.queue)
            except KeyboardInterrupt or Exception as e:
                print("exiting")
                log().getLogger("AppCommand").error("MQTT connection error: {}".format(e))


class AppData:
    def __init__(self) -> None:
        #Init MQTT
        self.mqtt = Pub_Handler()
        
        self.datarefreshRate = 0
        self.coordinates = (0, 0)
        self.config_path = config_path()
        self.acceleration = (0, 0, 0)
        self.avg_acc = 0
        self.direction = 0
        try:
            self.gps = connect_pksi_dgps(self.config_path)
            self.imu = connect_pksi_INS()
        except Exception as e:
            print(e)
            log().getLogger("AppData").error("error connecting to piksi: {}".format(e))
        # Data Log for autonomous mode
        print(f'Getting Longitudenal and Latitude data: {self.gps.get_data(type="rover")}')
        print(f'Logging Longitudenal and Latitude data: {self.gps.log()}')

    def worker(self, q2):
        while True:
            try:
                """Establishing connection with GPS"""
                
                self.coordinates = self.gps.get_data(type="rover")
                print(f'Getting Longitudenal and Latitude data: {self.coordinates}')
                # print(f'Logging Longitudenal and Latitude data: {gps.log()}')
                acc = self.imu.get_acc_data()
                avg_acc = np.sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2)
                print(f'Getting Acceleration data: {avg_acc}')
                direction = self.imu.get_heading()

                if not q2.empty():
                    print(f'logging coordinates for map generation : {self.gps.log()}')

            except Exception or KeyboardInterrupt as e:
                print(e) 
                log().getLogger("AppData").error(e)
            
            # Dictionary
            msg_dict = {
                "topic": "/bot/data",
                "latitude": str(self.coordinates[0]),
                "longitude": str(self.coordinates[1]),
                "acceleration": str(self.avg_acc),
                "direction": str(self.direction)
            }
            print(msg_dict)
            # send msg to MQTT broaker
            time.sleep(self.datarefreshRate)
            self.mqtt.data_handler(msg_dict)
            log().getLogger("AppData").info(self.mqtt.status)
            
class Navigator:
    def __init__(self) -> None:
        #self.mqtt = Pub_Handler() # can not have 2 publishers handler instance as used in AppData
        #self.laser = ls()
        # 
        config_path = gps_path()
        try:
            if config_path is not None:
                with open(config_path, "r") as config_file:
                    data = json.load(config_file)
                    lat = data['lat']
                    lon = data['lon']
                    config_file.close()
            else:
                alt_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../.."))}/L2_Data/gps_data.json'
                with open(alt_path, "r") as config_file:
                    data = json.load(config_file)
                    lat = data['lat']
                    lon = data['lon']
                    config_file.close()
        
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)
            log().getLogger("Navigator").error("Failed to read JSON, return code %d\n", e) 

        self.coordinates = (lat, lon)

    def autonomousNavigator(self, q2):
        try:
            """Once set the target position, this function will receive
            the value and set it to algorithm to start."""
            tapPosition = q2.get()
            print(tapPosition)
            targetLocation= (tapPosition['latitude'], tapPosition['longitude'])
            #print(self.coordinates)
            map = MapHandler(type='all', destination=targetLocation, coordinates=self.coordinates)
            """Call Individual functions from create_map_network.py"""
            print(f'create area graph(): {map.create_area_graph()}')
            print(f'find shortest path between two points():{map.find_shortest_path_between_two_points()}')
            cartesian_coordinates = map.cartesian_coordinates() # coordinates for change in direction
            print(f'cartesian coordinates(): {cartesian_coordinates}')
            print(f'logging coordinates(): {map.log_coordinates()}')
            print(f'plot graph shortest route(): {map.plot_graph_shortest_route()}')
            """Get the shortest route for Global Navigation and publish to app"""
            # print(f'Get shortest route for Global Navigation: {map.get_map()}')
            # Publish the initial direction to app
            msg_dict = {
                "topic": '/navigation/data',
                "path": cartesian_coordinates,
                "coordinates": self.coordinates
            }

            #self.mqtt.data_handler(msg_dict)
        except Exception as e:
            print("error in navigator library!: {}".format(e))
            log().getLogger("Navigator").error("error in navigator library!: {}".format(e))

    def worker(self, q2):
        while True:
            try:
                if not q2.empty():
                    print("Autonomous Navigator is working")
                    #log().getLogger("Navigator").info("Autonomous Navigator is working")
                    self.autonomousNavigator(q2)
                    # print(f'Laser data: {self.laser.scan()}')
                    q2.queue.clear() # clear the queue hence this will only run once and provide the shortest path 
                else:
                    pass
                    #print("No target position received")
                    #log().getLogger("Navigator").error("No target position received")
            except KeyboardInterrupt or Exception as e:
                log().getLogger("Navigator").error("exiting navigator with error!: {}".format(e))
                print("exiting navigator with error!")

#Update the below code for point cloud from SICK laser sensor or camera object avoidance algorithm
class manoeuvre:
    def __init__(self) -> None:
        pass
        #self.laser = ls()
        #self.ob = Object_avoid(self.laser.laser, target_distance=40, target_angle=(60, 120))
    def worker(self):
        while True:
            try:    
                #print(f'Laser data: {self.laser.scan()}')
                #print(f'Object Avoidance: {self.ob.object_detect()}')
                time.sleep(0.1)
            except KeyboardInterrupt:
                print("exiting manoeuvre with error!")
