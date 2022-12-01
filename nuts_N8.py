import numpy as np
import rotorParams as P
from deez_N8 import *

class rotorController:
    def __init__(self):
        # x control stuff
        self.Kx = Kx
        self.krx = krx

        # y control stuff
        self.Ky = Ky
        self.kry = kry

        # z control stuff
        self.Kz = Kz
        self.krz = krz

        # psi control stuff
        self.Kpsi = Kpsi
        self.krpsi = krpsi

        self.Ts = P.Ts
    
    def updateX(self,x_r,state):
        X = state.item(0)
        theta = state.item(4)
        u = state.item(6)
        q = state.item(10)

        x = np.array([
            [X],
            [theta],
            [u],
            [q]
        ])
        xe = np.array([
            [0],
            [0],
            [0],
            [0]
        ])

        tau_theta = -self.Kx @ (x-xe) + self.krx * (x_r - X)

        return tau_theta.item(0)

    def updateY(self,y_r,state):
        y = state.item(1)
        phi = state.item(3)
        v = state.item(7)
        p = state.item(9)

        x = np.array([
            [y],
            [phi],
            [v],
            [p]
        ])
        xe = np.array([
            [0],
            [0],
            [0],
            [0]
        ])

        tau_phi = -self.Ky @ (x-xe) + self.kry * (y_r - y)

        return tau_phi.item(0)
    
    def updateZ(self,z_r,state):
        z = state.item(2)
        w = state.item(8)

        x = np.array([
            [z],
            [w]
        ])
        xe = np.array([
            [0],
            [0]
        ])

        Ftilde = -self.Kz @ (x-xe) + self.krz * (z_r - z)
        Fe = (mc + 4*mf)*g
        F = Fe + Ftilde.item(0)

        return F

    def updatePsi(self,psi_r,state):
        psi = state.item(5)
        r = state.item(11)

        x = np.array([
            [psi],
            [r]
        ])
        xe = np.array([
            [0],
            [0]
        ])

        tau_psi = -self.Kpsi @ (x-xe) + self.krpsi * (psi_r - psi)

        return tau_psi.item(0)
    
    def update(self,x_r,y_r,z_r,psi_r,state):
        # Ftot = (mc + 4*mf)*g
        # tau_phi = 0
        # tau_theta = 0
        # tau_psi = 0

        Ftot = self.updateZ(z_r,state)
        tau_phi = self.updateY(y_r,state)
        tau_theta = self.updateX(x_r,state)
        tau_psi = self.updatePsi(psi_r,state)

        return Ftot,tau_phi,tau_theta,tau_psi