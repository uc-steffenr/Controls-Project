import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from numpy import sin,cos as s,c
import rotorParams as P

def rotYaw(a):
    R = np.array([
        [c(a), -s(a), 0],
        [s(a), c(a), 0],
        [0, 0, 1]
    ])
    return R

def rotPitch(b):
    R = np.array([
        [c(b), 0, s(b)],
        [0, 1, 0],
        [-s(b), 0, c(b)]
    ])
    return R

def rotRoll(g):
    R = np.array([
        [1, 0, 0],
        [0, c(g), -s(g)],
        [0, s(g), c(g)]
    ])
    return R

def R(a,b,g):
    r = rotYaw(a) @ rotPitch(b) @ rotRoll(g)
    return r

def drawCenter(self,state):
    px = state.item(0)
    py = state.item(1)
    pz = state.item(2)
    phi = state.item(3)
    theta = state.item(4)
    psi = state.item(5)

    # define points in terms of x,y,z for ease
    x = y = P.sc/np.sqrt(2)
    z = P.h

    # body frame
    verts = np.array([
        [x, y, z],
        [-x, y, z],
        [-x, -y, z],
        [x, -y, z],
        [x, y, -z],
        [-x, y, -z],
        [-x, -y, -z],
        [x, -y, -z]
    ])

    T = np.array([px,py,pz])

    # take to inertial frame
    self.cVerts = (verts @ R(psi,theta,phi)) + T

def drawArms(self,state):
    px = state.item(0)
    py = state.item(1)
    pz = state.item(2)
    phi = state.item(3)
    theta = state.item(4)
    psi = state.item(5)

    x = y = (P.sc/np.sqrt(2)) + P.d
    z = 0
    return

def drawFans(self):
    return