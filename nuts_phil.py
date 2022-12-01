import numpy as np
import rotorParams as P
import deez_phil as P2
from numpy import array

class control_deez_nuts:
    def __init__(self):
        self.flag = True
        self.K_x = P2.K_x
        self.Kr_x = P2.kr_x
        self.K_z = P2.K_z
        self.Kr_z = P2.kr_z
        self.Ts = P.Ts

    def update(self, x_r, z_r, states):
        x = states.item(0)
        theta = states.item(4)
        xDot = states.item(6)
        thetaDot = states.item(10)

        p_x = array([[x, theta, xDot, thetaDot]]).T
        pe_x = array([[x_r, 0, 0, 0]]).T
        tau_theta = -self.K_x @(p_x-pe_x) + self.Kr_x*(x_r-x)

        z = states.item(2)
        zDot = states.item(8)
        p_z = array([[z, zDot]]).T
        pe_z = array([[z_r, 0]]).T

        ftot = -(-self.K_z@(p_z-pe_z)+self.Kr_z*(z_r-z)) + (P.mass*P.g)

        return tau_theta.item(0), ftot.item(0)