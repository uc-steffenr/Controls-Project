import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import rotorParams as P

def figureEight(num_points=20, width=1, height=1):
    t = np.linspace(0,2*np.pi, num_points)
    x = np.sin(t)*width
    y = np.sin(t)*np.cos(t)*2*height
    z = 0*t
    psi = 0*t
    return {'x':x, 'y': y, 'z': z, 'psi': psi}

class pathFollow:
    def __init__(self):
        # self.num_points = 20
        self.num_points = int((P.t_end - P.t_start)/P.Ts)
        self.ref_list = figureEight(self.num_points)
        self.count = 0
        self.Xflag = False
        self.Yflag = False
        self.Zflag = False
        self.current_ref = np.array([self.ref_list['x'][self.count], self.ref_list['y'][self.count], self.ref_list['z'][self.count], self.ref_list['psi'][self.count]])
        
    def update(self, states,tol=0.01):
        x = states.item(0)
        y = states.item(1)
        z = states.item(2)

        xr = self.current_ref[0]
        yr = self.current_ref[1]
        zr = self.current_ref[2]

        # FIXME psi control messes up other controllers
        ##############################################################
        #                   ATTEMPT AT PSI CONTROL                   #
        ##############################################################
        # calculate commanded psi using dot product of future reference
        # value and current position
        # if self.count != self.num_points-1:
        #     self.numerator = (x + P.sc/2)*self.ref_list['x'][self.count+1] + \
        #                 y*self.ref_list['y'][self.count+1] + \
        #                 z*self.ref_list['z'][self.count+1]
        #     self.denominator = np.sqrt((x+P.sc/2)**2 + y**2 + z**2)*\
        #                 np.sqrt(self.ref_list['x'][self.count+1]**2 + \
        #                         self.ref_list['y'][self.count+1]**2 + \
        #                         self.ref_list['z'][self.count+1]**2)
        #     self.ref_list['psi'][self.count+1] = -np.arccos(self.numerator/self.denominator)
        # else:
        #     self.ref_list['psi'][self.count] = self.ref_list['psi'][self.count-1]
        # print(self.ref_list['psi'][self.count])

        if abs(x-xr) < tol:
            self.Xflag = True
        if abs(y-yr) < tol:
            self.Yflag = True
        if abs(z-zr) < tol:
            self.Zflag = True
        
        # will loiter if it is not close enough to the reference
        if self.Xflag and self.Yflag and self.Zflag:
            self.count += 1
            if self.num_points == self.count:
                self.count = 0
            self.current_ref = np.array([self.ref_list['x'][self.count], self.ref_list['y'][self.count], self.ref_list['z'][self.count], self.ref_list['psi'][self.count]])
            self.Xflag = False
            self.Yflag = False
            self.Zflag = False
        return self.current_ref
    
    def update_Nate(self):
        if self.count != self.num_points-1:
            self.count += 1
        return np.array([self.ref_list['x'][self.count], self.ref_list['y'][self.count], self.ref_list['z'][self.count], self.ref_list['psi'][self.count]])
