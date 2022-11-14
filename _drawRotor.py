import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from numpy import sin as s
from numpy import cos as c
import rotorParams as P

def rotYaw(a):
    R_ = np.array([
        [c(a), -s(a), 0],
        [s(a), c(a), 0],
        [0, 0, 1]
    ])
    return R_

def rotPitch(b):
    R_ = np.array([
        [c(b), 0, s(b)],
        [0, 1, 0],
        [-s(b), 0, c(b)]
    ])
    return R_

def rotRoll(g):
    R_ = np.array([
        [1, 0, 0],
        [0, c(g), -s(g)],
        [0, s(g), c(g)]
    ])
    return R_

def R(a,b,g):
    r = rotYaw(a) @ rotPitch(b) @ rotRoll(g)
    return r

def drawCenter(self,state,**kwargs):
    px = state.item(0)
    py = state.item(1)
    pz = state.item(2)
    phi = state.item(3)
    theta = state.item(4)
    psi = state.item(5)

    face_color = 'r'
    edge_color = 'k'
    lw = 1

    for key,val in kwargs.items():
        if key == 'face_color':
            face_color = val
        elif key == 'edge_color':
            edge_color = val
        elif key == 'lw':
            lw = val

    # define points in terms of x,y,z for ease
    x = y = P.sc/2
    z = P.h

    # top and bottom faces (z constant)
    self.face1 = np.array([
        [x,y,z],
        [-x,y,z],
        [-x,-y,z],
        [x,-y,z]
    ])
    self.face2 = np.copy(self.face1); self.face2[:,2] *= -1

    # first set of lateral faces (x constant)
    self.face3 = np.array([
        [x,y,z],
        [x,-y,z],
        [x,-y,-z],
        [x,y,-z]
    ])
    self.face4 = np.copy(self.face3); self.face4[:,0] *= -1

    # second set of lateral faces (y constant)
    self.face5 = np.array([
        [x,y,z],
        [-x,y,z],
        [-x,y,-z],
        [x,y,-z]
    ])
    self.face6 = np.copy(self.face5); self.face6[:,1] *= -1

    T = np.array([px,py,pz])
    T = np.tile(T,(self.face1.shape[0],1))

    # rotate and translate points
    self.face1 = (self.face1 @ R(psi,theta,phi)) + T
    self.face2 = (self.face2 @ R(psi,theta,phi)) + T
    self.face3 = (self.face3 @ R(psi,theta,phi)) + T
    self.face4 = (self.face4 @ R(psi,theta,phi)) + T
    self.face5 = (self.face5 @ R(psi,theta,phi)) + T
    self.face6 = (self.face6 @ R(psi,theta,phi)) + T

    # get faces in list format for Poly3DCollection
    self.face1 = [list(zip(self.face1[:,0],self.face1[:,1],self.face1[:,2]))]
    self.face2 = [list(zip(self.face2[:,0],self.face2[:,1],self.face2[:,2]))]
    self.face3 = [list(zip(self.face3[:,0],self.face3[:,1],self.face3[:,2]))]
    self.face4 = [list(zip(self.face4[:,0],self.face4[:,1],self.face4[:,2]))]
    self.face5 = [list(zip(self.face5[:,0],self.face5[:,1],self.face5[:,2]))]
    self.face6 = [list(zip(self.face6[:,0],self.face6[:,1],self.face6[:,2]))]

    if self.flag_init:
        f1 = Poly3DCollection(self.face1,color=face_color,edgecolor=edge_color,lw=lw)
        f2 = Poly3DCollection(self.face2,color=face_color,edgecolor=edge_color,lw=lw)
        f3 = Poly3DCollection(self.face3,color=face_color,edgecolor=edge_color,lw=lw)
        f4 = Poly3DCollection(self.face4,color=face_color,edgecolor=edge_color,lw=lw)
        f5 = Poly3DCollection(self.face5,color=face_color,edgecolor=edge_color,lw=lw)
        f6 = Poly3DCollection(self.face6,color=face_color,edgecolor=edge_color,lw=lw)

        self.ax.add_collection3d(f1)
        self.ax.add_collection3d(f2)
        self.ax.add_collection3d(f3)
        self.ax.add_collection3d(f4)
        self.ax.add_collection3d(f5)
        self.ax.add_collection3d(f6)

        self.handle.append(f1)
        self.handle.append(f2)
        self.handle.append(f3)
        self.handle.append(f4)
        self.handle.append(f5)
        self.handle.append(f6)

    else:
        # self.handle[0].set_verts(self.cLines)
        self.handle[0].set_verts(self.face1)
        self.handle[1].set_verts(self.face2)
        self.handle[2].set_verts(self.face3)
        self.handle[3].set_verts(self.face4)
        self.handle[4].set_verts(self.face5)
        self.handle[5].set_verts(self.face6)



def drawArms(self,state):
    px = state.item(0)
    py = state.item(1)
    pz = state.item(2)
    phi = state.item(3)
    theta = state.item(4)
    psi = state.item(5)

    lw = 2

    x1 = y1 = P.sc/2
    x2 = y2 = np.sqrt(2)*P.d + P.sc/2
    # z = 0

    verts = np.array([
        [x1,y1,0],
        [x2,y2,0],           # arm 1 points
        [-x1,y1,0],
        [-x2,y2,0],          # arm 2 points
        [x1,-y1,0],
        [x2,-y2,0],           # arm 3 points
        [-x1,-y1,0],
        [-x2,-y2,0]           # arm 4 points
    ])

    T = np.array([px,py,pz])
    T = np.tile(T,(verts.shape[0],1))

    verts = (verts @ R(psi,theta,phi)) + T

    arm1x = [verts[0,0],verts[1,0]]
    arm1y = [verts[0,1],verts[1,1]]
    arm1z = [verts[0,2],verts[1,2]]

    arm2x = [verts[2,0],verts[3,0]]
    arm2y = [verts[2,1],verts[3,1]]
    arm2z = [verts[2,2],verts[3,2]]

    arm3x = [verts[4,0],verts[5,0]]
    arm3y = [verts[4,1],verts[5,1]]
    arm3z = [verts[4,2],verts[5,2]]

    arm4x = [verts[6,0],verts[7,0]]
    arm4y = [verts[6,1],verts[7,1]]
    arm4z = [verts[6,2],verts[7,2]]
    
    if self.flag_init:
        arm1, = self.ax.plot3D(arm1x,arm1y,arm1z,'-o',color='k',lw=lw)
        arm2, = self.ax.plot3D(arm2x,arm2y,arm2z,'-o',color='k',lw=lw)
        arm3, = self.ax.plot3D(arm3x,arm3y,arm3z,'-o',color='k',lw=lw)
        arm4, = self.ax.plot3D(arm4x,arm4y,arm4z,'-o',color='k',lw=lw)

        self.handle.append(arm1)
        self.handle.append(arm2)
        self.handle.append(arm3)
        self.handle.append(arm4)

    else:
        self.handle[6].set_data_3d((arm1x,arm1y,arm1z))
        self.handle[7].set_data_3d((arm2x,arm2y,arm2z))
        self.handle[8].set_data_3d((arm3x,arm3y,arm3z))
        self.handle[9].set_data_3d((arm4x,arm4y,arm4z))


def drawFans(self,state):
    px = state.item(0)
    py = state.item(1)
    pz = state.item(2)
    phi = state.item(3)
    theta = state.item(4)
    psi = state.item(5)

    alpha = np.linspace(0,2*np.pi,self.circle_size)
    x = np.sqrt(2)*P.d + P.sc/2

    fan1 = np.array([x-P.rf*c(alpha),x+P.rf*s(alpha),np.zeros(self.circle_size)])
    fan2 = np.array([x-P.rf*c(alpha),-x+P.rf*s(alpha),np.zeros(self.circle_size)])
    fan3 = np.array([-x-P.rf*c(alpha),x+P.rf*s(alpha),np.zeros(self.circle_size)])
    fan4 = np.array([-x-P.rf*c(alpha),-x+P.rf*s(alpha),np.zeros(self.circle_size)])


    T = np.array([px,py,pz])
    
    for i in range(fan1.shape[1]):
        fan1[:,i] = np.matmul(fan1[:,i],R(psi,theta,phi)) + T
        fan2[:,i] = np.matmul(fan2[:,i],R(psi,theta,phi)) + T
        fan3[:,i] = np.matmul(fan3[:,i],R(psi,theta,phi)) + T
        fan4[:,i] = np.matmul(fan4[:,i],R(psi,theta,phi)) + T
    
    
    fan1 = [list(zip(fan1[0,:],fan1[1,:],fan1[2,:]))]
    fan2 = [list(zip(fan2[0,:],fan2[1,:],fan2[2,:]))]
    fan3 = [list(zip(fan3[0,:],fan3[1,:],fan3[2,:]))]
    fan4 = [list(zip(fan4[0,:],fan4[1,:],fan4[2,:]))]


    if self.flag_init:
        fan1poly = Poly3DCollection(fan1,color='b',lw=2,alpha=0.5,edgecolor='k')
        fan2poly = Poly3DCollection(fan2,color='b',lw=2,alpha=0.5,edgecolor='k')
        fan3poly = Poly3DCollection(fan3,color='b',lw=2,alpha=0.5,edgecolor='k')
        fan4poly = Poly3DCollection(fan4,color='b',lw=2,alpha=0.5,edgecolor='k')

        self.ax.add_collection3d(fan1poly)
        self.ax.add_collection3d(fan2poly)
        self.ax.add_collection3d(fan3poly)
        self.ax.add_collection3d(fan4poly)

        self.handle.append(fan1poly)
        self.handle.append(fan2poly)
        self.handle.append(fan3poly)
        self.handle.append(fan4poly)
    
    else:
        self.handle[10].set_verts(fan1)
        self.handle[11].set_verts(fan2)
        self.handle[12].set_verts(fan3)
        self.handle[13].set_verts(fan4)
