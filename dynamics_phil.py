import numpy as np
import sympy as sp
from numpy import sin, cos
import roto_params_phil as P

class VTOLDynamics:
    def __init__(self):
        self.state = P.state0
        self.Ts = P.Ts
        self.count = 0
        #self.PE = self.ml*self.g(self.h-self.d*sin(self.theta))   +   self.mc*self.g*self.h   +   self.mr*self.g*(self.h+self.d*sin(self.theta))
        #self.L = self.KE-self.PE
#DONE
    def saturate(self, u):
        if abs(u) > abs(P.F_max):
            u = P.F_max*np.sign(u)
        return u

#done
    def rk4_step(self, u):
        # Integrate ODE using Runge-Kutta RK4 algorithm
        F1 = self.f(self.state, u)
        F2 = self.f(self.state + self.Ts / 2 * F1, u)
        F3 = self.f(self.state + self.Ts / 2 * F2, u)
        F4 = self.f(self.state + self.Ts * F3, u)
        self.state = self.state + self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)

#Done
#This is deffinitely not the best way to write this, but I really don't care
    def f(self, state, u):
        # Returns: time derivative of state vector (xdot)
        
        #  State Vector Reference:
        #idx  0, 1, 2, 3, 4, 5,  6,   7,   8,   9, 10, 11
        #x = [u, v, w, p, q, r, phi, the, psi, xE, yE, hE]
        
        # Store state variables in a readable format
        x = state
        self.count += 2
        if self.count >1: quit()
        
        ub = x[0,0]
        vb = x[1,0]
        wb = x[2,0]
        p = x[3,0]
        q = x[4,0]
        r = x[5,0]
        phi = x[6,0]
        theta = x[7,0]
        psi = x[8,0]
        xE = x[9,0]
        yE = x[10,0]
        hE = x[11,0]
        
        # Calculate forces from propeller inputs (u)
        F1 = u[0]
        F2 = u[1]
        F3 = u[2]
        F4 = u[3]
        Fz = F1 + F2 + F3 + F4
        L = (F2 + F3) * P.dy - (F1 + F4) * P.dy
        M = (F1 + F3) * P.dx - (F2 + F4) * P.dx
        #N = -T(F1,dx,dy) - T(F2,dx,dy) + T(F3,dx,dy) + T(F4,dx,dy)
        N=0
        
        # Pre-calculate trig values
        cphi = np.cos(phi);   sphi = np.sin(phi)
        cthe = np.cos(theta); sthe = np.sin(theta)
        cpsi = np.cos(psi);   spsi = np.sin(psi)
        
        # Calculate the derivative of the state matrix using EOM
        xdot = np.zeros(12)
        
        xdot[0] = -P.g * sthe + r * vb - q * wb  # = udot
        xdot[1] = P.g * sphi*cthe - r * ub + p * wb # = vdot
        xdot[2] = 1/P.m * (-Fz) + P.g*cphi*cthe + q * ub - p * vb # = wdot
        xdot[3] = 1/P.Ixx * (L + (P.Iyy - P.Izz) * q * r)  # = pdot
        xdot[4] = 1/P.Iyy * (M + (P.Izz - P.Ixx) * p * r)  # = qdot
        xdot[5] = 1/P.Izz * (N + (P.Ixx - P.Iyy) * p * q)  # = rdot
        xdot[6] = p + (q*sphi + r*cphi) * sthe / cthe  # = phidot
        xdot[7] = q * cphi - r * sphi  # = thetadot
        xdot[8] = (q * sphi + r * cphi) / cthe  # = psidot
        
        xdot[9] = cthe*cpsi*ub + (-cphi*spsi + sphi*sthe*cpsi) * vb + \
            (sphi*spsi+cphi*sthe*cpsi) * wb  # = xEdot
            
        xdot[10] = cthe*spsi * ub + (cphi*cpsi+sphi*sthe*spsi) * vb + \
            (-sphi*cpsi+cphi*sthe*spsi) * wb # = yEdot
            
        xdot[11] = -1*(-sthe * ub + sphi*cthe * vb + cphi*cthe * wb) # = hEdot
        print(xdot)
        return xdot

#Done
    def h(self):
        z = self.state.item(0)
        h = self.state.item(1)
        theta = self.state.item(2)
        zDot = self.state.item(3)
        hDot = self.state.item(4)
        thetaDot = self.state.item(5)
        y = np.array([z, h, theta, zDot, hDot, thetaDot])
        return y

#techincally Done
    def update(self, u):
        #u = self.saturate(u)
        #self.get_Euler
        self.rk4_step(u)
        #self.saturate_bar()
        y = self.h()
        return y