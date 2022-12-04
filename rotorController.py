import numpy as np
import rotorParams as P
from numpy import array

class rotorController:
    def __init__(self,**kwargs):
        self.type = 'FSFB'
        for key,val in kwargs.items():
            if key == 'type':
                self.type = val

        if self.type == 'FSFB':
            import FSFB_gains as P2
            # x gains
            self.K_x = P2.K_x
            self.kr_x = P2.kr_x
            # y gains
            self.K_y = P2.K_y
            self.kr_y = P2.kr_y
            # z gains
            self.K_z = P2.K_z
            self.Kr_z = P2.kr_z
            # psi gains
            self.K_psi = P2.K_psi
            self.kr_psi = P2.kr_psi

        self.Ts = P.Ts

    def updateX(self,x_r,state):
        x = state.item(0)
        theta = state.item(4)
        xDot = state.item(6)
        thetaDot = state.item(10)

        if self.type == 'FSFB':
            p_x = array([[x, theta, xDot, thetaDot]]).T
            pe_x = array([[x_r, 0, 0, 0]]).T
            tau_theta = -self.K_x @ (p_x-pe_x) + self.kr_x*(x_r-x)

        return tau_theta.item(0)
    
    def updateY(self,y_r,state):
        y = state.item(1)
        phi = state.item(3)
        v = state.item(7)
        p = state.item(9)

        if self.type == 'FSFB':
            x = np.array([[y,phi,v,p]]).T
            xe = np.array([[y_r,0,0,0]]).T
            tau_phi = -self.K_y @ (x-xe) + self.kr_y * (y_r - y)

        return tau_phi.item(0)
    
    def updateZ(self,z_r,state):
        z = state.item(2)
        zDot = state.item(8)

        if self.type == 'FSFB':
            p_z = array([[z, zDot]]).T
            pe_z = array([[z_r, 0]]).T
            Ftot = -(-self.K_z@(p_z-pe_z)+self.Kr_z*(z_r-z)) + (P.mass*P.g)

        return Ftot.item(0)
    
    def updatePsi(self,psi_r,state):
        psi = state.item(5)
        r = state.item(11)
        
        if self.type == 'FSFB':
            x = np.array([[psi,r]]).T
            xe = np.array([[psi_r,0]]).T
            tau_psi = -self.K_psi @ (x-xe) + self.kr_psi * (psi_r - psi)

        return tau_psi.item(0)
    
    def update(self,x_r,y_r,z_r,psi_r,state):

        Ftot = self.updateZ(z_r,state)
        tau_phi = self.updateY(y_r,state)
        tau_theta = self.updateX(x_r,state)
        tau_psi = self.updatePsi(psi_r,state)

        # TODO add option to saturate individual fans

        return Ftot,tau_phi,tau_theta,tau_psi   