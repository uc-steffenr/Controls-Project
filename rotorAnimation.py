import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
# from numpy import sin,cos as s,c
import rotorParams as P

class rotorAnimation:
    def __init__(self):
        self.flag_init = True # first time drawing figure
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.lim = 0.3 # limit for plot size
        # NOTE MAKE SURE TO UPDATE LIMITS EVERY TIME AROUND
        self.ax.set_xlim(P.x0-self.lim,P.x0+self.lim)
        self.ax.set_ylim(P.y0-self.lim,P.y0+self.lim)
        self.ax.set_zlim(P.z0-self.lim,P.z0+self.lim)
        self.handle = []
        self.circle_size = 50 # number of points for fan circle

        # for key,val in kwargs.item():
        #     if key == 'face_color':
        #         self.face_color=val
        #     elif key == 'edge_color':
        #         self.edge_color=val
        #     elif key == 'edge_lw':
        #         self.edge_lw=val
        #     elif key == 'arm_lw':
        #         self.arm_lw=val
        #     elif key == 'arm_color':
        #         self.arm_color=val
        #     elif key == 'lim':
        #         self.lim=val
        #     elif key == 'circle_size':
        #         self.circle_size=val
    
    from _drawRotor import drawCenter, drawArms, drawFans
    
    def update(self,state):
        x = state.item(0)
        y = state.item(1)
        z = state.item(2)

        self.drawCenter(state,face_color='r',edge_color='k',lw=1)
        self.drawArms(state)
        self.drawFans(state)

        if self.flag_init:
            self.flag_init = False
        else:
            self.ax.set_xlim(x-self.lim,x+self.lim)
            self.ax.set_ylim(y-self.lim,y+self.lim)
            self.ax.set_zlim(z-self.lim,z+self.lim)
        return
    