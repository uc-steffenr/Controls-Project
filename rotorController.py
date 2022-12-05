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
        elif self.type == 'FSFBI':
            import FSFBI_gains as P2
            # x gains
            self.K_x = P2.K_x
            self.ki_x = P2.ki_x
            self.integrator_x = 0.0
            self.error_dl_x = 0.0
            # y gains
            self.K_y = P2.K_y
            self.ki_y = P2.ki_y 
            self.integrator_y = 0.0
            self.error_dl_y = 0.0
            # z gains
            self.K_z = P2.K_z
            self.ki_z = P2.ki_z
            self.integrator_z = 0.0
            self.error_dl_z = 0.0
            # psi gains
            self.K_psi = P2.K_psi
            self.ki_psi = P2.ki_psi
            self.integrator_psi = 0.0
            self.error_dl_psi = 0.0

        self.Ts = P.Ts

    def updateX(self,x_r,state):
        x = state.item(0)
        theta = state.item(4)
        xDot = state.item(6)
        thetaDot = state.item(10)

        p_x = array([[x, theta, xDot, thetaDot]]).T
        pe_x = array([[x_r, 0, 0, 0]]).T

        if self.type == 'FSFB':
            tau_theta = -self.K_x @ (p_x-pe_x) + self.kr_x*(x_r-x)
        elif self.type == 'FSFBI':
            error = x_r - x
            self.integrateErrorX(error)
            tau_theta = -self.K_x @ (p_x-pe_x) - self.ki_x*self.integrator_x

        return tau_theta.item(0)
    
    def updateY(self,y_r,state):
        y = state.item(1)
        phi = state.item(3)
        v = state.item(7)
        p = state.item(9)

        x = np.array([[y,phi,v,p]]).T
        xe = np.array([[y_r,0,0,0]]).T

        if self.type == 'FSFB':            
            tau_phi = -self.K_y @ (x-xe) + self.kr_y * (y_r - y)
        elif self.type == 'FSFBI':
            error = y_r - y
            self.integrateErrorY(error)
            tau_phi = -self.K_y @ (x-xe) - self.ki_y*self.integrator_y

        return tau_phi.item(0)
    
    def updateZ(self,z_r,state):
        z = state.item(2)
        zDot = state.item(8)

        p_z = array([[z, zDot]]).T
        pe_z = array([[z_r, 0]]).T

        if self.type == 'FSFB':            
            Ftot = -(-self.K_z@(p_z-pe_z)+self.Kr_z*(z_r-z)) + (P.mass*P.g)
        elif self.type == 'FSFBI':
            error = z_r - z
            self.integrateErrorZ(error)
            Ftot = -(-self.K_z @ (p_z-pe_z) - self.ki_z*self.integrator_z) + P.mass*P.g

        return Ftot.item(0)
    
    def updatePsi(self,psi_r,state):
        psi = state.item(5)
        r = state.item(11)

        x = np.array([[psi,r]]).T
        xe = np.array([[psi_r,0]]).T
        
        if self.type == 'FSFB':            
            tau_psi = -self.K_psi @ (x-xe) + self.kr_psi * (psi_r - psi)
        elif self.type == 'FSFBI':
            error = psi_r - psi
            self.integrateErrorPsi(error)
            tau_psi = -self.K_psi @ (x-xe) - self.ki_psi*self.integrator_psi

        return tau_psi.item(0)
    
    def update(self,x_r,y_r,z_r,psi_r,state):

        Ftot = self.updateZ(z_r,state)
        tau_phi = self.updateY(y_r,state)
        tau_theta = self.updateX(x_r,state)
        tau_psi = self.updatePsi(psi_r,state)

        # TODO add option to saturate individual fans

        return Ftot,tau_phi,tau_theta,tau_psi   
    
    def integrateErrorX(self,error):
        self.integrator_x = self.integrator_x + (self.Ts/2.0)*(error + self.error_dl_x)
        self.error_dl_x = error
    
    def integrateErrorY(self,error):
        self.integrator_y = self.integrator_y + (self.Ts/2.0)*(error + self.error_dl_y)
        self.error_dl_y = error
    
    def integrateErrorZ(self,error):
        self.integrator_z = self.integrator_z + (self.Ts/2.0)*(error + self.error_dl_z)
        self.error_dl_z = error
    
    def integrateErrorPsi(self,error):
        self.integrator_psi = self.integrator_psi + (self.Ts/2.0)*(error + self.error_dl_psi)
        self.error_dl_psi = error