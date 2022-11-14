import numpy as np
from numpy import sin as s
from numpy import cos as c
from rotorParams import *

class rotorDynamics:
    def __init__(self, alpha=0.0):
        return
    
    def update(self,u):
        return
    
    def f(self,state,u):
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