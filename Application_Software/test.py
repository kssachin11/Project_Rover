import spidev
import json
import time
from json.decoder import JSONDecodeError

class SPI:
    def __init__(self):
        
        self.spi_sleep = 0.2
        self.spi_bus = 0
        self.spi_device = 0
        self.max_speed = 500000
        self.mode =0
                
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

    def spiHandshake(self, input):
        '''Send 1 to begin spi communication, return bool'''
        handshakevalue = int(input)
        print(type(handshakevalue))
        self.spi.writebytes([handshakevalue])
        time.sleep(self.spi_sleep)
        reply = self.spi.readbytes(2)[0]
        print(reply)
        print(f'Value received: {reply:09b} : {reply:3}')

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


obj = SPI()

while True:
    # this is a test
    input_val = input("Enter your value: ")
    value = obj.spiHandshake(int(input_val))
    # Testing