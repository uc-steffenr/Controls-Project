import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def figureEight(num_points=20, width=1, height=1):
    t = np.linspace(0,2*np.pi, num_points)
    x = np.sin(t)*width
    y = np.sin(t)*np.cos(t)*2*height
    z = 0*t
    psi = 0*t
    return {'x':x, 'y': y, 'z': z, 'psi': psi}

class pathFollow:
    def __init__(self):
        self.num_points = 20
        self.ref_list = figureEight(self.num_points)
        self.count = 0
        self.Xflag = False
        self.Yflag = False
        self.Zflag = False
        self.current_ref = np.array([self.ref_list['x'][self.count], self.ref_list['y'][self.count], self.ref_list['z'][self.count], self.ref_list['psi'][self.count]])
        

    def update(self, states):
        x = states.item(0)
        y = states.item(1)
        z = states.item(2)

        xr = self.current_ref[0]
        yr = self.current_ref[1]
        zr = self.current_ref[2]

        # print('x: ', round(x,2), round(xr,2))
        # print('y: ', round(y,2), round(yr,2))
        # print('z: ', round(z,2), round(zr,2))
        # print()

        if round(x,1) == round(xr,1):
            self.Xflag = True
        if round(z,1) == round(zr,1):
            self.Zflag = True
        if round(y,1) == round(yr,1):
            self.Yflag = True

        

        if self.Xflag and self.Yflag and self.Zflag:
            self.count += 1
            if self.num_points == self.count:
                self.count = 0
            self.current_ref = np.array([self.ref_list['x'][self.count], self.ref_list['y'][self.count], self.ref_list['z'][self.count], self.ref_list['psi'][self.count]])
            self.Xflag = False
            self.Yflag = False
            self.Zflag = False
        return self.current_ref

        # if round(x,1) == round(xr,1) and round(y,1) == round(yr,1) and round(z,1) == round(zr,1):
        #     self.count += 1
        #     if self.num_points == self.count:
        #         self.count = 0
        #     self.current_ref = np.array([self.ref_list['x'][self.count], self.ref_list['y'][self.count], self.ref_list['z'][self.count], self.ref_list['psi'][self.count]])
        # return self.current_ref
