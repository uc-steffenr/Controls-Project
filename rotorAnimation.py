import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from numpy import sin,cos as s,c
import rotorParams as P

class rotorAnimation:
    def __init__(self):
        self.flag_init = True # first time drawing figure
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.lim = 0.5 # limit for plot size
        # NOTE MAKE SURE TO UPDATE LIMITS EVERY TIME AROUND
        self.ax.set_xlim(-P.x0-self.lim,P.x0+self.lim)
        self.ax.set_ylim(-P.y0-self.lim,P.y0+self.lim)
        self.ax.set_zlim(-P.z0-self.lim,P.z0+self.lim)
        self.handle = []
    
    from ._drawRotor import drawCenter, drawArms, drawFans
    
    def update(self,state):
        return
    