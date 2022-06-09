#This is just copy pasted from the webpage
from ulab import numpy as np
# from numpy.linalg import inv, solve
from math import cos, sin, atan, pi, inf
import math
from pyb import delay
# import imageio
# import matplotlib.pyplot as plt
# from IPython.display import Image
# import matplotlib.pyplot as plt

class NewtRaph():
    
    def __init__(self):
        ## Givens
        self.a = 0.75 
        self.b = 4.5/(2*pi*1.5) #in/rad
        self.G = 15/50 #gear ratio
        self.info = np.array([[0],[0]])


    # This function takes in x_desired and returns a hypotenuse and an angle
    # It stores this data in an array called 'info' whose first element is the hypotenuse and the second element is the theta it makes with X
    def calculate(self,x_des):
        a = self.a
        b = self.b
        G = self.G
        hyp = ((x_des[0][0])**2 + (x_des[1][0])**2)**0.5
        rot_theta = atan(x_des[0][0]/x_des[1][0])
        self.info[0][0] = hyp
        self.info[1][0] = rot_theta
        
        return self.info


    def g(self,x, theta):
        a = self.a
        b = self.b
        G = self.G
        delta_theta = theta[1][0] - theta[0][0]
        g = np.array([   [x[0][0] - (a + G*b*delta_theta)*cos(G*theta[0][0])],
                         [x[1][0] - (a + G*b*delta_theta)*sin(G*theta[0][0])]   ])
        return g


    def dg_dtheta(self,theta):
        a = self.a
        b = self.b
        G = self.G
        delta_theta = theta[1][0] - theta[0][0]
        
        dgx_dt1 = G*b*cos(G*theta[0][0]) + G*(a + G*b*delta_theta)*sin(G*theta[0][0])
        
        dgx_dt2 = -G*b*cos(G*theta[0][0])
        
        dgy_dt1 = G*b*sin(G*theta[0][0]) - G*(a + G*b*delta_theta)*cos(G*theta[0][0])
        
        dgy_dt2 = -G*b*sin(G*theta[0][0])
       
        dg_dtheta = np.array([[  dgx_dt1 , dgx_dt2] , [dgy_dt1, dgy_dt2 ]])

        return np.linalg.inv(dg_dtheta)


    def NewtonRaphson(self, fcn, jacobian, guess, thresh):
        a = self.a
        b = self.b
        G = self.G
        theta = guess
        error = inf
        error = np.linalg.norm(fcn(theta))
        
        while error > thresh:
            
            theta = theta - np.dot(jacobian(theta),fcn(theta))       
            error = np.linalg.norm(fcn(theta))
        
#         print("NR is returning theta")
        return theta



    def Raphson_Runner(self, x_desired, theta_guess):
        x_des = x_desired
        theta = self.NewtonRaphson(lambda th: self.g(x_des,th), self.dg_dtheta, theta_guess, 1e-5)
#         print(50*180*theta[0][0]/(15*pi))
#         print(50*180*theta[1][0]/(15*pi))        
        
        return theta
    
if __name__ == '__main__':
    NR = NewtRaph()
    x_desired = np.array([ [2] , [1] ])
    theta_guess = np.array([ [0] , [0] ])
    theta = NR.Raphson_Runner(x_desired, theta_guess)
    print(f't1: {180*theta[0][0]/(pi)}')
    print(f't2: {180*theta[1][0]/(pi)}')
    
#     print(f't1: {50*180*theta[0][0]/(15*pi)}')
#     print(f't2: {50*180*theta[1][0]/(15*pi)}')