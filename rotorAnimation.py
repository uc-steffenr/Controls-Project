import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
# from numpy import sin,cos as s,c
import rotorParams as P

# TODO add option for zoomed out view
# TODO change animation for zoomed out view
# TODO add reference line too

# variables to change
# - FOLLOW -> NOTE maybe make string for 'follow', 'zoomed out', or 'both'
# -> both would include a top and bottom subplot, top shows simple animation of 
# zoomed out view while bottom shows close up view with more in depth animation
# NOTE maybe make it self.type rather than FOLLOW?
# - plot size (lim)
# - 

class rotorAnimation:
    def __init__(self,type='follow'):
        self.flag_init = True # first time drawing figure
        # self.FOLLOW = True  #check if figure follows rotor
        self.type = type
        self.fig = plt.figure(figsize=(10,5))
        # self.ax = self.fig.add_subplot(projection='3d')

        if self.type == 'follow':
            self.lim = 0.3 # limit for plot size
            self.axF = self.fig.add_subplot(111,projection='3d')
            self.axF.set_xlim(P.x0-self.lim,P.x0+self.lim)
            self.axF.set_ylim(P.y0-self.lim,P.y0+self.lim)
            self.axF.set_zlim(-P.z0+self.lim,-P.z0-self.lim)

            self.axF.set_xlabel('North (m)')
            self.axF.set_ylabel('East (m)')
            self.axF.set_zlabel('Down (m)')
        elif self.type == 'zoomed out':
            self.limZ = 5 # limit for plot size
            self.axZ = self.fig.add_subplot(111,projection='3d')
            self.axZ.set_xlim(P.x0-self.limZ,P.x0+self.limZ)
            self.axZ.set_ylim(P.y0-self.limZ,P.y0+self.limZ)
            self.axZ.set_zlim(-P.z0+self.limZ,-P.z0-self.limZ)

            self.axZ.set_xlabel('North (m)')
            self.axZ.set_ylabel('East (m)')
            self.axZ.set_zlabel('Down (m)')
        else: # both option
            self.axF = self.fig.add_subplot(121,projection='3d')
            self.axZ = self.fig.add_subplot(122,projection='3d')

            self.lim = 0.3
            self.limZ = 5

            self.axF.set_xlim(P.x0-self.lim,P.x0+self.lim)
            self.axF.set_ylim(P.y0-self.lim,P.y0+self.lim)
            self.axF.set_zlim(-P.z0+self.lim,-P.z0-self.lim)

            self.axZ.set_xlim(P.x0-self.limZ,P.x0+self.limZ)
            self.axZ.set_ylim(P.y0-self.limZ,P.y0+self.limZ)
            self.axZ.set_zlim(-P.z0+self.limZ,-P.z0-self.limZ)

            self.axF.set_xlabel('North (m)')
            self.axF.set_ylabel('East (m)')
            self.axF.set_zlabel('Down (m)')

            self.axZ.set_xlabel('North (m)')
            self.axZ.set_ylabel('East (m)')
            self.axZ.set_zlabel('Down (m)')

        
        self.handle = []
        self.zoomHandle = []
        self.Xhandle = []
        self.Yhandle = []
        self.Zhandle = []
        self.circle_size = 50 # number of points for fan circle
    
    from drawRotor import drawCenter, drawArms, drawFans, drawSimpleRotor

    def update(self,state):
        x = state.item(0)
        y = state.item(1)
        z = state.item(2)

        if self.type == 'follow' or self.type == 'both':
            self.drawCenter(state,face_color='r',edge_color='k',lw=1)
            self.drawArms(state)
            self.drawFans(state)
        if self.type == 'zoomed out' or self.type == 'both':
            self.drawSimpleRotor(state)

        #drawing line that tracks vtol
        self.Xhandle.append(x)
        self.Yhandle.append(y)
        self.Zhandle.append(z)
        if self.type == 'follow' or self.type == 'both':
            self.axF.plot3D(self.Xhandle,self.Yhandle,self.Zhandle, zorder=0)
        if self.type == 'zoomed out' or self.type == 'both':
            self.axZ.plot3D(self.Xhandle,self.Yhandle,self.Zhandle, zorder=0)

        if self.flag_init:
            self.flag_init = False
        else:
            if self.type == 'follow' or self.type == 'both':
                self.axF.set_xlim(x-self.lim,x+self.lim)
                self.axF.set_ylim(y-self.lim,y+self.lim)
                self.axF.set_zlim(z+self.lim,z-self.lim)
        return
    
    def updateAnim(self,i,states, time):
        x = states[i,0]
        y = states[i,1]
        z = states[i,2]
        phi = states[i,3]
        theta = states[i,4]
        psi = states[i,5]
        state = np.array([[x,y,z,phi,theta,psi]]).T

        if self.type == 'follow' or self.type == 'both':
            self.drawCenter(state,face_color='r',edge_color='k',lw=1)
            self.drawArms(state)
            self.drawFans(state)
        if self.type == 'zoomed out' or self.type == 'both':
            self.drawSimpleRotor(state)

        #drawing line that tracks vtol
        self.Xhandle.append(x)
        self.Yhandle.append(y)
        self.Zhandle.append(z)
        if self.type == 'follow' or self.type == 'both':
            self.axF.plot3D(self.Xhandle,self.Yhandle,self.Zhandle, zorder=0)
            self.axF.set_title(f'time {round(time[i],2)}')
        if self.type == 'zoomed out' or self.type == 'both':
            self.axZ.plot3D(self.Xhandle,self.Yhandle,self.Zhandle, zorder=0)
            self.axZ.set_title(f'time {round(time[i],2)}')

        if self.flag_init:
            self.flag_init = False
        else:
            if self.type == 'follow' or self.type == 'both':
                self.axF.set_xlim(x-self.lim,x+self.lim)
                self.axF.set_ylim(y-self.lim,y+self.lim)
                self.axF.set_zlim(z+self.lim,z-self.lim)
        return