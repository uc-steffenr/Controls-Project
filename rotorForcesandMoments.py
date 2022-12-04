import numpy as np
import rotorParams as P
from numpy import sin as s
from numpy import cos as c
import random as r


def generateWind(self):
    return

def ForcesAndMoments(self,state,F):    
    phi = self.state.item(3)
    theta = self.state.item(4)
    psi = self.state.item(5)
    u = self.state.item(6)
    v = self.state.item(7)
    w = self.state.item(8)

    M = P.mc + 4*P.mf
    # differential forces from each rotor
    df = F.item(0) # front
    dr = F.item(1) # right
    db = F.item(2) # back
    dl = F.item(3) # left

    # torques caused by rotation of fans
    # these will affect the yawing
    tau_f = P.rf*df
    tau_r = P.rf*dr
    tau_b = P.rf*db
    tau_l = P.rf*dl

    Ftot = df + dr + db + dl
    tau_phi = P.d*(dl - dr)
    tau_theta = P.d*(df - db)
    tau_psi = tau_r + tau_l - tau_f - tau_b

    fx = Ftot * (-c(phi)*s(theta)*c(psi) - s(phi)*s(psi)) # - M*P.mu_x*u # -> air disturbance term
    fy = Ftot * (-c(phi)*s(theta)*s(psi) + s(phi)*c(psi)) # - M*P.mu_y*v
    fz = M*P.g - Ftot*c(phi)*c(theta) # - M*P.mu_z*w

    return fx,fy,fz,tau_phi,tau_theta,tau_psi