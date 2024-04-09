# ------------------------------------------------
# --- Author: Farogh Iftekhar
# ------------------------------------------------
''' Description: SPI driver for raspberry Pi'''

import time
import spidev
import json
import helper

from json.decoder import JSONDecodeError

class SPI:
    def __init__(self):
        self.config_path = helper.config_path()
        self.spi_sleep = 0.2
        try:
            with open(self.config_path, "r") as config_file:
                data = json.load(config_file)
                self.spi_bus = data['spi']['bus']
                self.spi_device = data['spi']['device']
                self.max_speed = data['spi']['freq']
                self.mode = data['spi']['mode']
                config_file.close()
                
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)
        
        # Start new SPI connection
        self.spiInit()

    def spiInit(self):
        #SPI activating
        self.spi = spidev.SpiDev()
        self.spi.open(self.spi_bus,self.spi_device)
        self.spi.max_speed_hz= self.max_speed
        self.spi.mode = self.mode
        

    def spiReset(self):
        self.spi.close()
        self.spiInit()

    def spiHandshake(self):
        '''Send 1 to begin spi communication, return bool'''
        handshakevalue = 170
        self.spi.writebytes([handshakevalue])
        reply = self.spi.readbytes(1)[0]
        
        if reply == 170:
            print("SPI connected!")
            return True
        else:
            return False

    def txSpi(self, spiPacket):
        '''Transmit SPI packets'''
        self.spi.writebytes([spiPacket])
        time.sleep(self.spi_sleep)

    def rxSpi(self, retries):
        '''Receive data from the SPI and return a list'''
        reply = []
        counter = 0
        while sum(int(reply)) == 0 and counter < int(retries):
            reply = self.spi.readbytes(1)[0]
            counter += 1
        return reply
    
    def rxpi(self):
        '''Receive data from the SPI and return a list'''
        reply = self.spi.readbytes(1)[0]
        return reply