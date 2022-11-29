import numpy as np
from numpy import sin as s
from numpy import cos as c
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
        return
    
    def f(self,state,u):
        self.ForcesAndMoments()

        return
    
    def h(self):
        return
    
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