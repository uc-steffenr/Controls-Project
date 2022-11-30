import numpy as np
import rotorParams as P
import deez_phil as P2
from numpy import array

class control_deez_nuts:
    def __init__(self):
        self.flag = True
        self.K_x = P2.K_x
        self.Kr_x = P2.kr_x
        self.Ts = P.Ts

    def update(self, x_r, states):
        x = states.item[0]
        theta = states.item[2]
        xDot = states.item[6]
        thetaDot = states.item[8]

        p_x = array([[x, theta, xDot, thetaDot]]).T
        pe_x = array([[x_r, 0, 0, 0]]).T

        tau_x = -self.K_x @(p_x-pe_x) + self.Kr_x*(x_r-x)

        return tau_x