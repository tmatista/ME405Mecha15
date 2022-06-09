from pyb import Timer, SPI
#import
import pyb
from pyb import Timer, SPI
from math import pi


class TMC4210_driver:
    
    def __init__(self): 
        self.spi = SPI(2,SPI.CONTROLLER,baudrate=1000000,polarity=1, phase=1) #changed from 100k to 1M (6/4/2022)
        self.buf = bytearray(4)
        #check baudrate
        pass
    
    ## put in bytearray use 0b prefix
    def sanity_check(self,byte_array):
        # Sanity Check. 
        self.spi.send_recv(byte_array,self.buf,timeout=5000)

        for idx,byte in enumerate(self.buf):
            print(f"b{3-idx}: {byte:#010b} {byte:#04x} {byte:#03}")
        pass
        
    ## A Motor Driver 1 Send/Receive function
    def send_recv(self, address):
        # Send datagrams via SPI bus and recieve a message from the TMC back
        self.spi.send_recv(address,self.buf,timeout=5000)
        return self.decoder(self.buf)
#         print(self.buf)
#         for idx,byte in enumerate(self.buf):
#             print(f"b{3-idx}: {byte:#010b} {byte:#04x} {byte:#03}")
#         return self.buf
    
    def send(self, address):
        # Send datagrams via SPI bus
        self.spi.send(address,timeout=5000)
        pass
        
    def decoder(self, byte_array):
        # Give me an array, ill tell you what it reads
        buffer = 0
        for idx,byte in enumerate(byte_array):
#             print(f"b{3-idx}: {byte:#010b} {byte:#04x} {byte:#03}")
            if idx == 1:
                buffer += byte << 16
            if idx == 2:
                buffer += byte<< 8
            if idx == 3:
                buffer += byte
        return buffer
        
        
        
    def translator(self, number,byte_array):
        # Give me a number you want to put in an array and I will do it. 
        byte_array[1] = number >> 16
        byte_array[2] = (number >> 8) & 0xFF
        byte_array[3] = (number) & 0xFF
        
    def theta_to_ticks(self, theta):
        # This is assuming the 1/8th division of microstepping
        # Give me a theta, I will give you ticks
        cpr = 200*8/(360)
        ticks = theta*cpr
        return ticks
    
    def a_maxxer(self, a_max, a_max_byte_array, ramp_div, pulse_div, p_mul_div):
        a = a_max
        BA = a_max_byte_array
        RD = ramp_div
        PD = pulse_div
        PMULDIV = p_mul_div
        
        p = a/(128*(2**(RD-PD)))
        p_mul = 128
        p_div = 0
        pp =  (p_mul / (2**(3 + p_div)) )/p
#        