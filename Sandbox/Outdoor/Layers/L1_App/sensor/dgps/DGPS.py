import os
import re
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.navigation import *
from json.decoder import JSONDecodeError
import json
from matplotlib import pyplot as plt
import helpers as helper


    
class connect_pksi_dgps():

    def __init__(self, config_path) -> None:

        """_summary_

        This code opens piksi multi at IP address mentioned in Config.json file in workspace
        and generats coordinates of the rover and saves it into maps/gps_data.json.

        """
        self.flag = 0.0
        self.n, self.e, self.d = 0.0, 0.0, 0.0
        self.lat, self.lon, self.height, self.h = 0.0 , 0.0, 0.0, 0.0
        self.v_n, self.v_e, self.v_d = 0.0, 0.0, 0.0
        self.wn, self.tow = 0, 0
        self.mag_x, self.mag_y, self.mag_z = 0.0, 0.0, 0.0
        self.acc_x, self.acc_y, self.acc_z = 0.0, 0.0, 0.0
        self.coordinates = []
        
        self.config_path = config_path
        # self.config_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../.."))}/Configure.json'
        # as required [SBP_MSG_BASELINE_NED, SBP_MSG_POS_LLH, SBP_MSG_VEL_NED, SBP_MSG_GPS_TIME]
        self.msg_list = [SBP_MSG_POS_LLH]

        try:
            with open(self.config_path, "r") as config_file:
                data = json.load(config_file)
                self.IP_add = data['dgps']['IP_add']
                self.port = data['dgps']['port']
                self.base = data['base']['IP_add']
                config_file.close()
        except FileNotFoundError:
            print("File not found")
            
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)

    def get_data(self, type, msg_list = None):
        if msg_list is None:
            msg_list = self.msg_list # default message list
        if type == "rover":
            ''' Creates Piksi connection'''
            with TCPDriver(self.IP_add, self.port) as driver:
                with Handler(Framer(driver.read, None, verbose=True)) as source:
                    # print(f'Connection Eshtablished for piksi at IP {self.IP_add}')

                    ''' Getting data'''
                    try:
                        
                        #msg_list = [SBP_MSG_POS_LLH]
                        """  This position solution message reports the absolute geodetic coordinates and" 
                            the status (single point vs pseudo-absolute RTK) of the position solution."
                            If the rover receiver knows the surveyed position of the base station and"
                            has an RTK solution, this reports a pseudo-absolute position solution using"
                            the base station position and the rover's RTK baseline vector. The full GPS"
                            time is given by the preceding MSG_GPS_TIME with the matching time-of-week(tow)"""
                        coordinates = []
                        for msg_type in msg_list:
                            msg, metadata = next(source.filter([msg_type]),(None,None))
                            if msg is not None:
                                # print(f'Data Receiving from Piksi at IP {msg.sender}')
                                # LLH position in deg-deg-m
                                if msg.msg_type == 522:
                                    # print("Getting LLH position in deg-deg-m")
                                    self.lat = msg.lat
                                    self.lon = msg.lon
                                    self.h = msg.height
                                    return self.lat, self.lon, self.h
                                # RTK position in mm (from base to rover)
                                elif msg.msg_type == 524:
                                    self.n = msg.n
                                    self.e = msg.e
                                    self.d = msg.d
                                # RTK velocity in mm/s
                                elif msg.msg_type == 526:
                                    self.v_n = msg.n
                                    self.v_e = msg.e
                                    self.v_d = msg.d
                                # GPS time
                                elif msg.msg_type == 258:
                                    self.wn = msg.wn
                                    self.tow = msg.tow  # in milli
                                # Magnetometer data
                                elif msg.msg_type == 2306:
                                    print("Getting Magnetometer data")
                                    self.mag_x = msg.mag_x
                                    self.mag_y = msg.mag_y
                                    self.mag_z = msg.mag_z
                                    return self.mag_x, self.mag_y, self.mag_z
                                # Accelerometer data
                                elif msg.msg_type == 2304:
                                    print("Getting Accelerometer data")
                                    self.acc_x = msg.acc_x * 8 /32768
                                    self.acc_y = msg.acc_y * 8 /32768
                                    self.acc_z = msg.acc_z * 8 /32768
                                    return self.acc_x, self.acc_y, self.acc_z
                                else:
                                    pass
                            #self.log()
                            #print(self.whole_string())
                        
                    except KeyboardInterrupt:
                        print("Error getting data!")
        elif type == "base":
            ''' Creates Piksi connection for base station'''
            with TCPDriver(self.base, self.port) as driver:
                with Handler(Framer(driver.read, None, verbose=True)) as source:
                    # print(f'Connection Eshtablished for piksi at IP {self.base}')

                    ''' Getting data'''
                    try:
                        msg_list = [SBP_MSG_BASELINE_NED, SBP_MSG_POS_LLH,
                                         SBP_MSG_VEL_NED, SBP_MSG_GPS_TIME]
                        coordinates = []
                        #for i in range(10):
                        for msg_type in msg_list:
                            msg, metadata = next(source.filter([msg_type]),(None,None))
                            #print("Latitude: %.4f, Longitude: %.4f" % (msg.lat , msg.lon )
                            if msg is not None:
                                # print(f'Data Receiving from Piksi at IP {msg.sender}')
                                # LLH position in deg-deg-m
                                if msg.msg_type == 522:
                                    self.lat = msg.lat
                                    self.lon = msg.lon
                                    self.h = msg.height
                                    return self.lat, self.lon, self.h
                                # RTK position in mm (from base to rover)
                                elif msg.msg_type == 524:
                                    self.n = msg.n
                                    self.e = msg.e
                                    self.d = msg.d

                                # RTK velocity in mm/s
                                elif msg.msg_type == 526:
                                    self.v_n = msg.n
                                    self.v_e = msg.e
                                    self.v_d = msg.d
                                # GPS time
                                elif msg.msg_type == 258:
                                    self.wn = msg.wn
                                    self.tow = msg.tow  # in milli
                                else:
                                    pass
                            #coordinates.append([self.lat, self.lon])
                            #self.log()
                            #print(self.whole
                    except KeyboardInterrupt:
                        print("Error getting data!")

        
    
    def whole_string(self):
        '''
        Returns all the data as a string
        '''

        return('wn: %.0f\ttow: %.0f\tlat: %.4f\tlon: %.4f\th: %4.6f\tn: %6.0f\te: %6.0f\td: %6.0f\t'
               'v_n: %6.0f\tv_e: %6.0f\tv_d: %6.0f\t' %
               (self.wn, self.tow, self.lat, self.lon, self.h, self.n, self.e,
                self.d, self.v_n, self.v_e, self.v_d))
    
    def log(self):
        data_JSON =  {
	        "tow": self.tow,
	        "lat": self.lat,
	        "lon": self.lon,
	        "height": self.height,
            "flag": self.flag,
            "North": self.n,
            "East": self.e,             
            "Down": self.d,             
            "Height_base": self.h,
            "velocity_north": self.v_n,
            "velocity_east": self.v_e,             
            "velocity_down": self.v_d,         
        }
        with open(f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../.."))}/L2_Data/gps_data.json', "w") as write_file:
            json.dump(data_JSON, write_file)

    def average(self, data):
        ''' Returns the average of the data '''
        return sum(data)/len(data)