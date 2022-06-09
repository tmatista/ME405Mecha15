import pyb
from pyb import Timer, SPI, delay
import tmc4210drv

#Class Motor_Driver:
class Motor_Driver():
    def __init__(self):
        #timer and clock inputs
        self.AR = 2 #auto reload value (aka period)
        self.tim_num = 4 #timer number
        self.ch_num = 2
        self.compVal = 2 #compare value informs pulse width

        # Pin Initiation
        self.clkPin = pyb.Pin(pyb.Pin.cpu.B7, mode=pyb.Pin.OUT_PP) #SCL pin
        self.EN1 = pyb.Pin(pyb.Pin.cpu.C3, mode=pyb.Pin.OUT_PP, value=1) #EN1 pin
        self.EN2 = pyb.Pin(pyb.Pin.cpu.C2, mode=pyb.Pin.OUT_PP, value=1) # EN2 pin
        self.nCS1 = pyb.Pin(pyb.Pin.cpu.C0, mode=pyb.Pin.OUT_PP, value=1) #nCS1 Chip Select pin
        self.nCS2 = pyb.Pin(pyb.Pin.cpu.C4, mode=pyb.Pin.OUT_PP, value=1) #nCS2 Chip Select pin
        self.sck = pyb.Pin(pyb.Pin.cpu.B8, mode=pyb.Pin.OUT_PP) #sck pin

        ## PWM timers and clocks
        self.tim = pyb.Timer(self.tim_num, period = self.AR, prescaler = 0)
        self.clk = self.tim.channel(2, pin=self.clkPin, mode=Timer.PWM, pulse_width=self.compVal)

        ## ======= READ-ONLY REGISTERS======
        type_register = bytearray([0b01110011,
                                   0b00000000,
                                   0b00000000,
                                   0b00000000])

        self.x_actual1 = bytearray([0b00000011,
                              0b00000000,
                              0b00000000,
                              0b00000000])
        
        self.x_actual2 = bytearray([0b00000011,
                              0b00000000,
                              0b00000000,
                              0b00000000])

        v_actual = bytearray([0b00001011,
                              0b00000000,
                              0b00000000,
                              0b00000000])

        a_actual = bytearray([0b00001111,
                              0b00000000,
                              0b00000000,
                              0b00000000])

        ## ======= WRITE-ONLY REGISTERS======    

        self.x_target1 = bytearray([0b00000000,
                              0b00000000,
                              0b00000000,
                              0b00000000])
        
        self.x_target2 = bytearray([0b00000000,
                              0b00000000,
                              0b00000000,
                              0b00000000])

        v_min =    bytearray([0b00000100,
                              0b00000000,
                              0b00000000,
                              0b00001010])

#         v_max =    bytearray([0b00000110,
#                               0b00000000,
#                               0b00000000,
#                               0b10001010])
        
        v_max =    bytearray([0b00000110,
                              0b00000000,
                              0b00000001,
                              0b01100101]) # v_max = 357
        
        

        self.v_target1 =  bytearray([0b00001000,
                                     0b00000000,
                                     0b00000000,
                                     0b00000000])
        
        self.v_target2 =  bytearray([0b00001000,
                                     0b00000000,
                                     0b00000000,
                                     0b00000000])

        #A_max is set to 1040 (10000010000)
        # set to 200 (11001000)
        # set to 100 (0110100)
        # set to 255 (11111111)
        # Set to 2000 (11111010000)
#         a_max =   bytearray([0b000001100,
#                               0b00000000,
#                               0b00000111,
#                               0b11001000])


        a_max =   bytearray([0b000001100,
                              0b00000000,
                              0b00000000,
                              0b01010000]) #a_max = 80

        #This address sets the en_sd register to 1
        IF_configuration_4210 = bytearray([0b01101000,
                                           0b00000000,
                                           0b00000000,
                                           0b00100000])
        # ramp: 1 pulse:3
#         ([0b00011000,
#         0b00000000,
#         0b00110001,
#         0b00000000 ])
        # Pulse: 0 Ramp: 0
        # ramp: 6 pulse: 4
#         pulse_ramp_div = bytearray([0b00011000,
#                                     0b00000000,
#                                     0b01000110,
#                                     0b00000000 ])


        pulse_ramp_div = bytearray([0b00011000,
                                    0b00000000,
                                    0b10101000, #puls_div = 10 ramp_div = 8
                                    0b00000000 ])


        P_mul_div = bytearray([0b00010010,
                               0b00000000,
                               0b10011100,   #pmul = 156
                               0b00000010]) #pdiv = 3



        self.R_M_REF_conf = bytearray([0b00010100,
                                  0b00000000,
                                  0b00001100,
                                  0b00000000 ])

        self.vel_mode = bytearray([0b00010100,
                                  0b00000000,
                                  0b00001100,
                                  0b00000010 ])
        
        self.EN1.low()
        self.EN2.low()


        ## =======Function Calls=======
        ## TMC4210 object definitions
        self.TMC1 = tmc4210drv.TMC4210_driver()
        self.TMC2 = tmc4210drv.TMC4210_driver()

        a = self.TMC1.decoder(a_max)

        ## ========Motor Initialization=======
        #Send the en_sd register to 1
        self.nCS1.low()
        self.nCS2.low()
        self.TMC1.send(IF_configuration_4210)
        self.TMC2.send(IF_configuration_4210)

        #Set the V_min and V_max values to 10
        self.TMC1.send(v_min)
        self.TMC2.send(v_min)

        self.TMC1.send(v_max)
        self.TMC2.send(v_max)

        #Set the pulse_div and ramp_div register to 0, ramp_div divides the acceleration
        # parameter, pulse_div divides the velocity parameter
        self.TMC1.send(pulse_ramp_div)
        self.TMC2.send(pulse_ramp_div)

        #Set PMUL & PDIV
        self.TMC1.send(P_mul_div)
        self.TMC2.send(P_mul_div)

        #Set A_MAX
        self.TMC1.send(a_max)
        self.TMC2.send(a_max)

        #Set Ramp_MODE and REF_CONFIG
        self.TMC1.send(self.R_M_REF_conf)
        self.TMC2.send(self.R_M_REF_conf)
        self.nCS1.high()
        self.nCS2.high()
        
        
        
        #checking thresholds
        
        self.ck_thresh = 1
        

        #Homing External Interrupt
#         self.homeInt = ExtInt(pyb.Pin.cpu.(PIN HERE), ExtInt.IRQ_FALLING, pyb.Pin.PULL_NONE, callback = saveHome)


        ## ========End Motor Initialization========


        ## ========Motor Movement=========
    def Motor_Runner(self, theta_1, theta_2): #add offsetting from saveHome()
        
        # Take the theta_1 and theta_2 values and turn them into ticks
        ticks1 = self.TMC1.theta_to_ticks(theta_1)
        ticks2 = self.TMC2.theta_to_ticks(theta_2)
        
        # Take those ticks, put them in the x_target datagrams
        # This has to be int since it operates in binary
        self.TMC1.translator(int(ticks1), self.x_target1)
        self.TMC2.translator(int(ticks2), self.x_target2)
        
        # Send the x_target to motor 1
        self.nCS1.low()
        self.TMC1.send(self.x_target1)
        self.nCS1.high()
        
        # Send the x_target to motor 2
        self.nCS2.low()
        self.TMC2.send(self.x_target2)
        self.nCS2.high()
        
    def get_actual(self):
#         print('checking')
        check = 0
        
        self.nCS1.low() #lower pin
        tic1 = self.TMC1.send_recv(self.x_actual1)
        self.nCS1.high()
        
        self.nCS2.low() #lower pin
        tic2 = self.TMC2.send_recv(self.x_actual2)
        self.nCS2.high()
        
        pos1 = (tic1 *360 /1600)
        pos2 = (tic2 *360 /1600)
        
        return pos1, pos2


    def at_target(self, th1, th2):
#         print('checking')
        check = 0
        
        self.nCS1.low() #lower pin
        tic1 = self.TMC1.send_recv(self.x_actual1)

        self.nCS1.high()
        
        self.nCS2.low() #lower pin
        tic2 = self.TMC2.send_recv(self.x_actual2)

        self.nCS2.high()
        
        pos1 = tic1 *360 /1600
        pos2 = tic2 *360 /1600

        print("pos1 = {} pos2 = {}".format(pos1,pos2))
        print("th1 = {} th2 = {}".format(th1,th2))

        err1 = abs(pos1 - th1)
        
        err2 = abs(pos2 - th2)
        
        if err1 <= self.ck_thresh and err2 <= self.ck_thresh:
#             print('check is set to true')
            check = 1
        
        
        return check

        
if __name__ == '__main__':
    drv = Motor_Driver()
#     drv.startHoming()
#     drv.saveHome()
    drv.Motor_Runner(0,0)
#     delay(5000)
#     print(drv.at_target(360,360))
#     drv.Motor_Runner(0,0)

    
    # I am feeding this function ticks, this needs to be DEGREES
#     drv.Motor_Runner(0,360)
#     delay(10000)
#     drv.Motor_Runner(0,0)
