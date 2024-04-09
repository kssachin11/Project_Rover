import json
from datetime import datetime
import time
import numpy as np

from matplotlib import pyplot as plt
#from Navigator.Navigator import Navigator
from Layers.L2_Data.pub_data_handler import Pub_Handler
from Layers.L3_protocols.spi import SPI
from helper import *


class AppCommand:
    def __init__(self) -> None:
        """Init SPI"""
        self.spi = SPI()
        self.enableManual = 69

        # check SPI connection is working between Pi and Arduino
        while True:
            if not self.spi.spiHandshake():
                print("SPI connection error, check wiring!")
                time.sleep(0.5)
            else:
                break

    def worker(self, q1, q2):
        while True:
            try:
                command = q1.get()
                # convert string to  object
                json_object = json.loads(command)

                # Check data type coming from APP
                if not (json_object.get("botCommand") is None):
                    print("botCommand received: {}".format(json_object["botCommand"]))
                    self.spi.txSpi(self.enableManual)
                    time.sleep(1)
                    self.spi.txSpi(int(json_object["botcommand"]))

                elif not (json_object.get("autoMode") is None):
                    print("autoMode received: {}".format(json_object["autoMode"]))
                    self.spi.txSpi(int(json_object["autoMode"]))

                elif not (json_object.get("manualMode") is None):
                    print("manualMode received: {}".format(json_object["manualMode"]))
                    self.spi.txSpi(int(json_object["manualMode"]))

                elif not (json_object.get("targetPosition") is None):
                    q2.put(json_object["targetPosition"])

                else:
                    print("not a valid Json format!")

            except KeyboardInterrupt:
                print("exiting")


class AppData:
    def __init__(self) -> None:
        """Init MQTT & SPI"""
        self.mqtt = Pub_Handler()
        self.spi = SPI()
        self.datarefreshRate = 30

    def worker(self):
        flag = False
        counter = 0
        dataList = []
        dummyList = []
        while True:
            try:
                # Read data from SPI

                val = self.spi.rxpi()
                #print("val is: ")
                #print(val)
                if flag == True:
                    #print("flag = true!")
                    dummyList.append(val)
                    if counter == 8:
                        #print("list full")
                        dataList = dummyList[2:8]
                        print(dataList)
                        int1 =  dataList[1]<<8
                        int1 |= dataList[0]
                        int2 =  dataList[3]<<8
                        int2 |= dataList[2]
                        int3 =  dataList[5]<<8
                        int3 |= dataList[4]
                        print(int1,int2,int3)
                        counter = 0
                        flag = False
                        dataList.clear()
                        dummyList.clear()
                    counter+=1

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
                navigator = Navigator(radarData = jsonData['data'], mapData=mapData, target=[int(targetPosition[0]), int(targetPosition[1])])
                startTime = datetime.now()
                path = navigator.run()
                stopTime = datetime.now()
                timeTaken = stopTime - startTime

                direction = navigator.botData.direction

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