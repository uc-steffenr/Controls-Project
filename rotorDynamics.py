import numpy as np
from numpy import sin as s
from numpy import cos as c
from numpy import tan as t
import rotorParams as P

class rotorDynamics:
    def __init__(self, alpha=0.0):
        self.state = np.array([P.x0,P.y0,P.z0,P.phi0,P.theta0,P.psi0,P.xdot0,P.ydot0,P.zdot0,P.phidot0,P.psidot0,P.thetadot0])
        self.state = np.expand_dims(self.state,1)
        self.Ts = P.Ts
        return
    
    from rotorForcesandMoments import ForcesAndMoments

    def update(self,u):
        self.rk4_step(u)
        y = self.h()
        return y
    
    def f(self,state,F):
        pn = state.item(0)
        pe = state.item(1)
        h = state.item(2) # maybe make negative?
        phi = state.item(3)
        theta = state.item(4)
        psi = state.item(5)
        u = state.item(6)
        v = state.item(7)
        w = state.item(8)
        p = state.item(9)
        q = state.item(10)
        r = state.item(11)
        M = P.mc + 4*P.mf

        fx,fy,fz,tau_phi,tau_theta,tau_psi = self.ForcesAndMoments(state,F)

        # rotation matrix for position time derivatives
        # R1 = np.array([
        #     [c(theta)*c(psi), s(phi)*s(theta)*c(psi) - c(phi)*s(psi), c(phi)*s(theta)*c(psi) + s(phi)*s(psi)],
        #     [c(theta)*s(psi), s(phi)*s(theta)*s(psi) + c(phi)*c(psi), c(phi)*s(theta)*s(psi) - s(phi)*c(psi)],
        #     [-s(theta), s(phi)*c(theta), c(phi)*c(theta)]
        # ])
        # # position time derivatives
        # pdot = R1 @ np.array([[u],[v],[w]])

        # velocity time derivatives
        vdot = np.array([
            [r*v - q*w + (1/M)*fx],
            [p*w - r*u + (1/M)*fy],
            [q*u - p*v + (1/M)*fz]
        ])

        # rotation matrix for angle time derivatives
        # R2 = np.array([
        #     [1, s(phi)*t(theta), c(phi)*t(theta)],
        #     [0, c(phi), -s(phi)],
        #     [0, s(phi)/c(theta), c(phi)/c(theta)]
        # ])
        # # angle time derivatives
        # adot = R2 @ np.array([[p],[q],[r]])

        addot = np.array([
            [((P.Jy - P.Jz)/P.Jx)*q*r + (1/P.Jx)*tau_phi],
            [((P.Jz - P.Jx)/P.Jy)*p*r + (1/P.Jy)*tau_theta],
            [((P.Jx - P.Jy)/P.Jz)*p*q + (1/P.Jz)*tau_psi]
        ])

        pdot = np.array([[u],[v],[w]])
        adot = np.array([[p],[q],[r]])

        xdot = np.vstack((pdot,vdot,adot,addot))

        return xdot
    
    def h(self):
        pn = self.state.item(0)
        pe = self.state.item(1)
        h = self.state.item(2) # maybe make negative?
        phi = self.state.item(3)
        theta = self.state.item(4)
        psi = self.state.item(5)
        u = self.state.item(6)
        v = self.state.item(7)
        w = self.state.item(8)
        p = self.state.item(9)
        q = self.state.item(10)
        r = self.state.item(11)

        y = np.array([
            [pn],
            [pe],
            [h],
            [phi],
            [theta],
            [psi],
            [u],
            [v],
            [w],
            [p],
            [q],
            [r]
        ])

        return y
    
    def rk4_step(self,u):
        F1 = self.f(self.state,u)
        F2 = self.f(self.state + self.Ts/2 * F1, u)
        F3 = self.f(self.state + self.Ts/2 * F2, u)
        F4 = self.f(self.state + self.Ts * F3, u)
        self.state = self.state + self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)
    
    def saturate(self,u,limit):
        if abs(u) > limit:
            u = limit*np.sign(u)
        return u