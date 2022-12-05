import numpy as np
from numpy import sin as s
from numpy import cos as c
from numpy import tan as t
import rotorParams as P

class rotorDynamics:
    def __init__(self, alpha=0.0):
        self.state = np.array([P.x0,P.y0,-P.z0,P.phi0,P.theta0,-P.psi0,P.xdot0,P.ydot0,-P.zdot0,P.phidot0,P.thetadot0,-P.psidot0])
        self.state = np.expand_dims(self.state,1)
        self.Ts = P.Ts
        return
    
    from rotorForcesandMoments import ForcesAndMoments

    def update(self,u):
        self.rk4_step(u)
        y = self.h()
        return y
    
    def f(self,state,F):
        Ftot = F.item(0)
        tau_phi = F.item(1)
        tau_theta = F.item(2)
        tau_psi = F.item(3)

        phi = state.item(3)
        theta = state.item(4)
        psi = state.item(5)
        u = state.item(6)
        v = state.item(7)
        w = state.item(8)
        p = state.item(9)
        q = state.item(10)
        r = state.item(11)

        fx = Ftot * (-c(phi)*s(theta)*c(psi) - s(phi)*s(psi)) - P.mass*P.mu_x*u # -> air disturbance term
        fy = Ftot * (-c(phi)*s(theta)*s(psi) + s(phi)*c(psi)) - P.mass*P.mu_y*v
        fz = P.mass*P.g - Ftot*c(phi)*c(theta) - P.mass*P.mu_z*w

        #fx,fy,fz,tau_phi,tau_theta,tau_psi = self.ForcesAndMoments(state,F)

        pxddot = fx/P.mass
        pyddot = fy/P.mass
        pzddot = fz/P.mass
        phiddot = ((P.Jy-P.Jz)/P.Jx)*q*r + tau_phi/P.Jx
        thetaddot = ((P.Jz-P.Jx)/P.Jy)*p*r + tau_theta/P.Jy
        psiddot = ((P.Jx-P.Jy)/P.Jz)*p*q + tau_psi/P.Jz

        xdot = np.array([
            [u],
            [v],
            [w],
            [p],
            [q],
            [r],
            [pxddot],
            [pyddot],
            [pzddot],
            [phiddot],
            [thetaddot],
            [psiddot]
        ])

        return xdot
    
    def h(self):
        pn = self.state.item(0)
        pe = self.state.item(1)
        h = -self.state.item(2) 
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