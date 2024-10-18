#!/usr/bin/python
from Layer_1.sensor.sick.sick import *


print("<<<< initing sick")
sick = SICK("/dev/ttyUSB1", debug = True)
while True:
    print(".")
    if sick.get_frame():
        print(sick.polar)
        #car = ObstacleAvoidance(port="/dev/ttyUSB1",threshold=200)
        '''sick.make_image()
        cv2.imshow("Real Time Image", sick.image)
        cv2.waitKey(5)'''




