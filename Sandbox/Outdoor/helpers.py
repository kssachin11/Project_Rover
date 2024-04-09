# ------------------------------------------------
# --- Author: Vasu Padsumbia
# ------------------------------------------------
''' Description: This file return paths and other helper actions'''

import os
import logging as setuptools_logging
from setuptools import errors


# setuptools_logging.configure()
# log = logging.getLogger()

#------------------------------------------------------------
# File/Folder path Configuration
#------------------------------------------------------------

def log_path():
    ''' It returns the log file path'''
    try:
        CWD = os.path.dirname(os.path.abspath(__file__)) #get directory of current file
        temp = os.path.join(CWD, "Logs")
        if not os.path.exists(temp):
            os.makedirs(temp)
        logs_path = os.path.join(temp, "application.log")
        if not os.path.exists(logs_path):
            with open(logs_path, 'w') as file:
                pass
        return logs_path
        
    except OSError as errors :
        print(errors)

def config_path():
    '''It return the config file path'''
    try:
        CWD = os.path.dirname(os.path.abspath(__file__)) #get directory of current file
        config_path = os.path.join(CWD, "Configure.json")
        return config_path
        
    except OSError as errors :
        print(errors)

def map_coordinate_path():
    '''It return the smallMap_path file path'''
    try:
        CWD = os.path.dirname(os.path.abspath(__file__)) #get directory of current file
        folder1 = os.path.join(CWD, "Layers")
        folder2 = os.path.join(folder1, "L2_Data")
        map_coordinate_path = os.path.join(folder2, "coordinates.json")
        return map_coordinate_path
        
    except OSError as errors :
        print(errors)
        return None

def gps_path():
    '''It return the polarMap_path file path'''
    try:
        CWD = os.path.dirname(os.path.abspath(__file__)) #get directory of current file
        #print(CWD)  
        folder1 = os.path.join(CWD, "Layers")
        folder2 = os.path.join(folder1, "L2_Data")
        gps_path = os.path.join(folder2, "gps_data.json")
        return gps_path
        
    except OSError as errors :
        print(errors)
        return None
    
def polarMap_path():
    '''It return the polarMap_path file path'''
    try:
        CWD = os.path.dirname(os.path.abspath(__file__)) #get directory of current file
        folder1 = os.path.join(CWD, "Layers")
        folder2 = os.path.join(folder1, "L2_Data")
        polarMap_path = os.path.join(folder2, "polarMap.json")
        return polarMap_path
        
    except OSError as errors :
        print(errors)
        return None