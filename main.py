import cotask
import task_share
import task_motor
import newtonraphson
import filereader
import ihm04a1Driver
from pyb import UART, repl_uart
import utime
import micropython
from ulab import numpy as np
from math import pi, cos, sin
import gc


# This file will run the cotask function and control task execution
# This file will also instantiate all the shared variables that we need. Like theta.


# These are shares made for the bell and whistle. 
actx = task_share.Share('f', thread_protect = True)
acty = task_share.Share('f', thread_protect = True)

# X is the desired X coordinate
x = task_share.Share('f', thread_protect = True)

# Y is the desired Y coordinate
y = task_share.Share('f', thread_protect = True)

# Theta_1 will control the RADIAL DISK
theta_1 = task_share.Share('f', thread_protect = True)

#Theta_2 will control the SPIRAL DISK
theta_2 = task_share.Share('f', thread_protect = True)

# PUD is the pen up/down flag
pud = task_share.Share('f', thread_protect = True)
pud.put(0.0)

# First things first, Take the inkscape hpgl file and parse it into a new file
# filename = "simple.hpgl"
# filename = "drawing.hpgl"
# filename = "single target point.hpgl"
# filename = "bigdiamond.hpgl"
filename = "timTest.hpgl"
fr = filereader.Drawer()
fr.Draw(filename)

#arrive flag, denots if motors have arrived at target location. Prevent other tasks from running again until set 1
ar_flag = task_share.Share('d', thread_protect = True) #check format instead of float use bool
ar_flag.put(1)

driver = task_motor.Motor_Driver()
driver.Motor_Runner(0,0)
hello = input('Are you ready to continue?')

# Uart initialization
repl_uart(None)
uart = UART(2,115200)
uart.init(115200, 8, 0, 1)

# def start_program():
#     repl_uart(None)
#     uart = UART(2,115200)
#     uart.init(115200, 8, 0, 1)
#     motor_driver = task_motor.Motor_Driver()
#     motor_driver.Motor_Runner(0,0)
#     hello = input('Are you ready to continue?')
#     return 

def Motor_Drv():  
    driver = task_motor.Motor_Driver() #we might be able to get rid of this line since we have alread init the motor driver
    theta1 = theta_1.get()
    theta2 = theta_2.get()
    driver.Motor_Runner(theta1, theta2)
    
    while True:
        th1, th2 = driver.get_actual()
        uart.write(f'{th1} : {th2} \n')
        if ar_flag.get() == 0: #if ar_flag is False we are not at target location so run motors
            theta1 = theta_1.get()
            theta2 = theta_2.get()
            driver.Motor_Runner(theta1, theta2)
            ar_flag.put(driver.at_target(theta1, theta2)) #update bool in ar_flag based on at_target()
            
        if ar_flag.get() == 1:
            print('motors have arrived at target location')
        yield None   
        
        
def Pen_Drv():
    servo_drv     = ihm04a1Driver.ihm04a1()
    servo_1       = servo_drv.servo(1)
    servo_drv.enable()
    while True:
        if pud.get() == 1:
            servo_1.pd()
        if pud.get() == 0:
            servo_1.pu()
        yield None

    
def get_Thetas(): #gives error on last line (blank) and attempts to address have failed... not sure how to fix but since its last line no biggie?
    raphson = newtonraphson.NewtRaph()
    theta_guess = np.array([[0],[0]])
    xyfile = open('xy.txt', 'r')
    while True:
        
        if ar_flag.get() ==0:
            yield None
        
        if ar_flag.get() == 1:
            ar_flag.put(0)
            print('generating new thetas')
            line = xyfile.readline()

            print("line: {}".format(line))
            xy_coords = line.split(',')
            
            if xy_coords[0] == '':
                print('blank')
                break
            
            x_des = float(xy_coords[0])
            y_des = float(xy_coords[1])
            ud = int(xy_coords[2])
            pud.put(ud)
            
            x_desired = np.array([ [x_des],[y_des] ])
 
             # NR outputs the value in RADIANS, this must turn to degrees
            thetas = raphson.Raphson_Runner(x_desired, theta_guess)

            theta_guess[0][0] = thetas[0][0]    #this pinion in radians
            theta_guess[1][0] = thetas[1][0]

            # Motor angles are converted to degrees here  
            theta_1.put(180*thetas[0][0]/(pi))
            theta_2.put(180*thetas[1][0]/(pi))
            
            print("target theta 1 = {}".format(theta_1.get()))
            print("target theta 2 = {}".format(theta_2.get()))
            yield None
        print('done')    


def equation_drive(): #gives error on last line (blank) and attempts to address have failed... not sure how to fix but since its last line no biggie?
    raphson = newtonraphson.NewtRaph()
    theta_guess = np.array([[0],[0]])
    c = 0
    circle = np.linspace(6,2292,382)
    offset = np.array([[2],[2]])
    while True:
        if ar_flag.get() == 0:
            yield None
            
        if ar_flag.get() == 1:
            print('Generating New Thetas')
            ar_flag.put(0)
            x_des = 1*cos(0.15*c)*offset[0][0] + cos(circle[c])
            y_des = 1*sin(0.15*c)*offset[1][0] + sin(circle[c])
            x_desired = np.array([ [x_des],[y_des] ])
            c += 1
            print(c)
            print(x_des, y_des)
            # NR outputs the value in RADIANS, this must turn to degrees
            thetas = raphson.Raphson_Runner(x_desired, theta_guess)
            
            
            theta_guess[0][0] = thetas[0][0]    #this pinion in radians
            theta_guess[1][0] = thetas[1][0]

            # Motor angles are converted to degrees here  
            theta_1.put(180*(thetas[0][0] + 6*2*pi)/(pi))
            theta_2.put(180*(thetas[1][0] + 6*2*pi)/(pi))
            
            print("target theta 1 = {}".format(theta_1.get()))
            print("target theta 2 = {}".format(theta_2.get()))
            yield None
    print('done')    
            
        
motor_task = cotask.Task(Motor_Drv, 'function_1', priority=0, period=75, profile=True, trace=True)
cotask.task_list.append(motor_task)

theta_task = cotask.Task(get_Thetas, 'function_2', priority=1, period=75, profile=True, trace=True)
cotask.task_list.append(theta_task)


# equation_task = cotask.Task(equation_drive, 'function_2', priority = 1, period = 200, profile = True, trace = True)
# cotask.task_list.append(equation_task)

pud_driver = cotask.Task(Pen_Drv, 'function_4', priority=2, period=50, profile=True, trace=True)
cotask.task_list.append(pud_driver)


while True:
    cotask.task_list.rr_sched()