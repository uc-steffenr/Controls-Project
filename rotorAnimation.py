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
        self.FOLLOW = True  #check if figure follows rotor
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        if self.FOLLOW:
            self.lim = 0.3 # limit for plot size
            # NOTE MAKE SURE TO UPDATE LIMITS EVERY TIME AROUND
            self.ax.set_xlim(P.x0-self.lim,P.x0+self.lim)
            self.ax.set_ylim(P.y0-self.lim,P.y0+self.lim)
            self.ax.set_zlim(-P.z0-self.lim,-P.z0+self.lim)
        else:
            self.lim = 5 # limit for plot size
            self.ax.set_xlim(P.x0-self.lim,P.x0+self.lim)
            self.ax.set_ylim(P.y0-self.lim,P.y0+self.lim)
            self.ax.set_zlim(-P.z0-self.lim,-P.z0+self.lim)
        self.handle = []
        self.Xhandle = []
        self.Yhandle = []
        self.Zhandle = []
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

        #drawing line that tracks vtol
        self.Xhandle.append(x)
        self.Yhandle.append(y)
        self.Zhandle.append(z)
        self.ax.plot3D(self.Xhandle,self.Yhandle,self.Zhandle, zorder=0)

        if self.flag_init:
            self.flag_init = False
        else:
            if self.FOLLOW:
                self.ax.set_xlim(x-self.lim,x+self.lim)
                self.ax.set_ylim(y-self.lim,y+self.lim)
                self.ax.set_zlim(z-self.lim,z+self.lim)
        return
    
    def updateAnim(self,i,states, time):
        x = states[i,0]
        y = states[i,1]
        z = states[i,2]
        phi = states[i,3]
        theta = states[i,4]
        psi = states[i,5]
        state = np.array([[x,y,z,phi,theta,psi]]).T

        self.drawCenter(state,face_color='r',edge_color='k',lw=1)
        self.drawArms(state)
        self.drawFans(state)

        #drawing line that tracks vtol
        self.Xhandle.append(x)
        self.Yhandle.append(y)
        self.Zhandle.append(z)
        self.ax.plot3D(self.Xhandle,self.Yhandle,self.Zhandle, zorder=0, color='green')

        self.ax.set_title(f'time {round(time[i],2)}')

        if self.flag_init:
            self.flag_init = False
        else:
            if self.FOLLOW:
                self.ax.set_xlim(x-self.lim,x+self.lim)
                self.ax.set_ylim(y-self.lim,y+self.lim)
                self.ax.set_zlim(z-self.lim,z+self.lim)
        return
# state = np.array([[0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1]])
# animy = rotorAnimation()
# animy.update(0, state)
# plt.pause(2)
# animy.update(1, state)
# plt.pause(99)