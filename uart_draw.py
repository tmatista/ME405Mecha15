""" @file       405L1.py
    @brief
    @author     Tim Matista
    @author     Jason Hu
    @date       4/13/2022
"""
import serial
import numpy as np
from math import pi, cos, sin
# from matplotlib import pyplot as p
from matplotlib.animation import FuncAnimation
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-white')


port = 'COM18'
baud = 115200
x_data = []
y_data = []
a = 0.75 # in
b = 4.5/(3*pi) # inches / radian
G = 15/50

junk = ['MicroPython v1.18-246-gdf86cef59-dirty on 2022-03-24; NUCLEO-L476RG with STM32L476RG\r\n', 'Type "help()" for more information.\r\n', '>>> \r\n', 'raw REPL; CTRL-B to exit\r\n']
show = 1 #enable or disable printing of time - data

def animate(i):
    with serial.Serial(port, baud) as ser:
        ser.flush()
#         print('calling')
        while True:
            if ser.in_waiting:
#                 print('in waiting')
                line = ser.readline()
                clean = line.decode()
                # t1 and t2 are in degrees
                t1, t2 = clean.split(':')
                
                t1 = float(t1)
                t2 = float(t2)
                
                # theta1 and theta2 are in radians
                theta1 = pi*(t1)/180
                theta2 = pi*(t2)/180
                
                dth = (theta2 - theta1)
                
                
                x = (a + b*G*dth)*cos(G*theta1)
                y = (a + b*G*dth)*sin(G*theta1)
                print(x, y)
                x_data.append(x)
                y_data.append(y)
                
                p = np.linspace(0,2.85, 100)
                o = np.linspace(0,1,100)
                f = np.linspace(0,1,100)
                
                for i in range(0, len(p)):
                    o[i] =     (a + b*(p[i]*G))*cos(p[i]*G) * cos(G*theta2) + (a + b*(p[i]*G))*sin(p[i]*G) * sin(G*theta2)
                    f[i] =     (a + b*(p[i]*G))*cos(p[i]*G) * sin(G*theta2) - (a + b*(p[i]*G))*sin(p[i]*G) *  cos(G*theta2)
                
                plt.cla()
                plt.xlim(-5,5)
                plt.ylim(-5,5)
#                 plt.plot(o,f)
                plt.plot([0,5.25*cos(G*theta1)], [0,5.25*sin(G*theta1)])
                plt.plot(x, y, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")
                plt.plot(x_data,y_data)
                break

ani = FuncAnimation(plt.gcf(), animate, interval=1)
plt.tight_layout()
plt.show()
    
# with serial.Serial(port, baud) as ser: #auto-closes port when done
#     ser.flush()
#     while True:
#         try:
#             if ser.in_waiting:
#                 line = ser.readline()
#                 clean = line.decode()
#     #                 print(clean)
#                 t1, t2 = clean.split(':')
# #                 print(t1, t2)
#                 theta1 = pi*float(t1)/180
#                 theta2 = pi*float(t2)/180
#                 dth = pi*(theta2 - theta1)/180
#                 x = (a + b*G*dth)*cos(theta1)
#                 y = (a + b*G*dth)*sin(theta1)
#                 print(x, y)
#                 x_data.append(x)
#                 y_data.append(y)
                
                
                
#                 p.ion()
#                 fig = p.figure()
#                 animation.FuncAnimation(fig, animate2, fargs=(x_data, y_data), interval = 200)
#                 p.plot(x_data, y_data)
#                 p.draw()
#                 p.show()
#                 figure.canvas.draw()
#                 figure.canvas.flush_events()

#         except:
#             print("something is wrong!!")
#             break
