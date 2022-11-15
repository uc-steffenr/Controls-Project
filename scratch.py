import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from rotorAnimation import rotorAnimation
from rotorParams import *

# NOTE CHECK BACK AND MAKE SURE BODY FRAME IS RIGHT FOR NED
# I think it's good now, yaw might need to be checked out

rotorAnim = rotorAnimation()

state = np.array([x0,y0,z0,phi0,theta0,psi0,xdot0,ydot0,zdot0,phidot0,thetadot0,psidot0])
state = np.expand_dims(state,1)

rotorAnim.update(state)

plt.waitforbuttonpress()

# state = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
# state = np.expand_dims(state,1)
state = np.array([
    [0],
    [0],
    [0],
    [0 * np.pi/180], # -> phi, roll
    [0 * np.pi/180], # -> theta, pitch
    [0 * np.pi/180], # -> psi, yaw
    [0],
    [0],
    [0],
    [0],
    [0],
    [0]
])

rotorAnim.update(state)

plt.show(block=True)

# Kenny's test