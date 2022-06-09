# from datasheets:
# Ihm04A1 datasheet         nucelo datasheet      l476RG datasheet
# IN1a = CN9 pin 6  -------- PB4 (digital) ------ TIM3_ch1 (AF2)
# IN2A = CN9 pin 5 -------- PB5 (digital) ------ TIM3_CH2 (AF2)
# 
# 
# in1B = CN8 pin 1 ---- PA0 (analog) ------ tim2_ch1 (AF1)
# in2B = CN8 pin 2 ---- PA1 (analog) ------ tim2_ch2 (AF1)

# EN-A = CN9 pin3 ------PA10 (digital)
# EN-B = ???

#import statements
import pyb
import utime
from pyb import ExtInt, Pin, delay, ADC, Timer, UART, repl_uart

import array


class ihm04a1:
    def __init__(self):
        
        #define pins
        self.ENA = pyb.Pin(pyb.Pin.cpu.A10, mode = pyb.Pin.OUT_PP) #Enable pin for motor A (check this pin)
        A1 = pyb.Pin(pyb.Pin.cpu.B4)
        A2 = pyb.Pin(pyb.Pin.cpu.B5)
        
        #timer and channels
        tim3 = pyb.Timer(3, freq = 20000) #check frequency
        self.t3ch1 = tim3.channel(1, pyb.Timer.PWM, pin = A1)
        self.t3ch2 = tim3.channel(2, pyb.Timer.PWM, pin = A2)

    def enable(self):
        self.ENA.high()
        print('enable A')
        
    def disable(self):
        self.ENA.low()
        print('disable A')
    
    def servo(self, servoID):
        if servoID == 1:
            return Servo(self.t3ch1, self.t3ch2)
        else:
            print("motor not configured")

class Servo:
    #ripped from 305, auto clamps duty cycle to usable amount
    def __init__(self, ch1, ch2):
        self.ch1 = ch1
        self.ch2 = ch2
        self.servoSpeed = 15
        PB0 = Pin(Pin.cpu.B0, mode=Pin.IN)
        self.adc = ADC(PB0)
        self._uthresh = 2200
        self._dthresh = 2700
        
    def set_duty(self, duty):
        
#         self.ch1.pulse_width_percent(0)
#         self.ch2.pulse_width_percent(duty)        
        if duty < 0 and duty >= -100:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(-1*duty)
        elif duty == 0:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0)
        elif duty > 0 and duty <= 100:
            self.ch1.pulse_width_percent(duty)
            self.ch2.pulse_width_percent(0)
        else:
            raise ValueError("Invalid duty cycle. Duty cycle should be between -100 and 100")            

    def motor_test(self):
        print('testing motor')
        self.set_duty(40)
        utime.sleep_ms(1000)
        self.set_duty(0)
        utime.sleep_ms(1000)
        self.set_duty(-40)
        utime.sleep_ms(1000)
        self.set_duty(0)
        print('test complete')
        
        
    def servo_test(self):
        print('testing servo')
        print('moving pen down')
        self.pd()
        utime.sleep_ms(2000)
        print('moving pen up')
        self.pu()
        utime.sleep_ms(2000)
        print('testing complete')
        
        
    def pd(self):
        pos = self.adc.read()
        if pos < self._dthresh:
            self.set_duty(self.servoSpeed)
        if pos >= self._dthresh:
            self.set_duty(0)


    def pu(self):
        pos = self.adc.read()
        if pos > self._uthresh:
            self.set_duty(-self.servoSpeed)
        if pos <= self._uthresh:
            self.set_duty(0)
        
        
if __name__ =='__main__':

    import utime
    servo_drv     = ihm04a1()
    servo_1       = servo_drv.servo(1)
    servo_drv.enable()

    while True:
        servo_1.pu()
    servo_drv.disable()

