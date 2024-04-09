"This code updates location based on acceleration and heading data. It also sends the data"
# ------------------------------------------------
from Layers.L1_App.sensor.imu.gyroscpe import connect_pksi_INS as imu
from Layers.L1_App.sensor.dgps.DGPS import connect_pksi_dgps as dgps
import time, json, math
from helpers import * 

class INS:
    def __init__(self) -> None:
        self.config_path = config_path()
        self.ins = imu()
        self.gps = dgps(self.config_path)
        self.gps_type = "rover"
        self.mag_x, self.mag_y, self.mag_z = self.ins.get_mag_data()
        self.acc_x, self.acc_y, self.acc_z = self.ins.get_acc_data()
        self.heading_deg = self.ins.get_heading()
        self.data = {
            "mag_x": self.mag_x,
            "mag_y": self.mag_y,
            "mag_z": self.mag_z,
            "acc_x": self.acc_x,
            "acc_y": self.acc_y,
            "acc_z": self.acc_z,
            "heading_deg": self.heading_deg
        }
        # self.data = json.dumps(self.data)
        # self.mqtt = MQTT_Publish()
        # self.mqtt.publish_mqtt(self.data)
        # self.ins.log()
        # self.ins.close()
        self.velocity_x = 0
        self.velocity_y = 0
        self.latitude = 0
        self.longitude = 0
        self.heading_deg = 0
        self.dt = 0.01

    def get_data(self, type):
        coordinates = self.gps.get_data(type=type)
        if coordinates == [0, 0, 0]:
            return self.update_location()
        else:
            self.latitude = coordinates[0]
            self.longitude = coordinates[1]
            self.height = coordinates[2]
            return self.latitude, self.longitude, self.height

    def update_location(self):
        start_time = time.time()
        # Get acceleration and heading data
        acc_x, acc_y, acc_z = self.ins.get_acc_data()

        # Update coordinates based on acceleration, velocity, and heading
        # Update velocity
        self.velocity_x += acc_x * self.dt
        self.velocity_y += acc_y * self.dt

        # Assuming constant acceleration, velocity, and small time interval
        delta_x = self.velocity_x * self.dt + acc_x * self.dt**2 / 2
        delta_y = self.velocity_y * self.dt + acc_y * self.dt**2 / 2

        # Update location
        self.latitude += delta_x
        self.longitude += delta_y

        end_time = time.time()
        print(f"Time taken to update location: {end_time - start_time} seconds")
        self.dt = end_time - start_time
        return self.latitude, self.longitude, self.height
    
    def get_heading(self):
        return self.ins.get_heading()
    
    def calculate_target_heading(self, start, end):
        """ Calculate the heading from the start to the end point """
        start_lat, start_lon = start
        end_lat, end_lon = end
        dlon = math.radians(end_lon) - math.radians(start_lon)
        y = math.sin(dlon) * math.cos(end_lat)
        x = math.cos(start_lat) * math.sin(end_lat) - math.sin(start_lat) * math.cos(end_lat) * math.cos(dlon)
        angle = math.atan2(y, x)

        # Convert the angle to degrees
        angle = math.degrees(angle)

        # Normalize the bearing to a value between 0 and 360
        compass_bearing = (angle + 360) % 360

        return compass_bearing
    
    def cal_turn_angle(self, start_point, target_point):
        ''' Calculate the turn angle to the target point '''
        # Calculate the angle between the current heading and the target point
        target_heading = self.calculate_target_heading(start_point, target_point)
        tolerance = 5 # adjust as needed
        if abs(self.heading_deg - target_heading) < tolerance:
            return 0
        else:
            """ if the angle is negative, turn left, if positive, turn right """
            return target_heading - self.ins.get_heading() 
