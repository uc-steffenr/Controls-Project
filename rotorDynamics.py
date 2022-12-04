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
        M = P.mc + 4*P.mf

        fx = Ftot * (-c(phi)*s(theta)*c(psi) - s(phi)*s(psi)) # - M*P.mu_x*u # -> air disturbance term
        fy = Ftot * (-c(phi)*s(theta)*s(psi) + s(phi)*c(psi)) # - M*P.mu_y*v
        fz = M*P.g - Ftot*c(phi)*c(theta) # - M*P.mu_z*w

        #fx,fy,fz,tau_phi,tau_theta,tau_psi = self.ForcesAndMoments(state,F)

        # tmp = np.array([[1,1,1,1],
        #                 [0,0,P.d,P.d],
        #                 [P.d,-P.d,0,0],
        #                 [-P.rf,-P.rf,P.rf,P.rf]])
        # fanF = np.linalg.inv(tmp) @ np.array([[Ftot],[tau_phi],[tau_theta],[tau_psi]])

        # tmp = np.array([[1,1],
        #                  [P.d,-P.d]])
        # fanF_l_r = np.linalg.inv(tmp) @ np.array([[Ftot/2],[tau_phi]])
        # fanF_f_b = np.linalg.inv(tmp) @ np.array([[Ftot/2],[tau_theta]])
        # fanF = np.squeeze(np.vstack((fanF_f_b,fanF_l_r)))
        # # print(fanF.shape)    

        # for i in range(len(fanF)):
        #     fanF[i] = self.saturate(fanF[i],P.F_max)
        
        # Ftot = fanF[0] + fanF[1] + fanF[2] + fanF[3]
        # tau_phi = P.d*(fanF[2] - fanF[3])
        # tau_theta = P.d*(fanF[0] - fanF[1])
        # tau_psi = P.rf*(fanF[2] + fanF[3] - fanF[0] - fanF[1])

        # fx = Ftot * (-c(phi)*s(theta)*c(psi) - s(phi)*s(psi)) # - M*P.mu_x*u # -> air disturbance term
        # fy = Ftot * (-c(phi)*s(theta)*s(psi) + s(phi)*c(psi)) # - M*P.mu_y*v
        # fz = M*P.g - Ftot*c(phi)*c(theta) # - M*P.mu_z*w

        pxddot = fx/M
        pyddot = fy/M
        pzddot = fz/M
        # phiddot = tau_phi/P.Jx
        # thetaddot = tau_theta/P.Jy
        # psiddot = tau_psi/P.Jz

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
        h = -self.state.item(2) # maybe make negative?
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
        # self.state[2] *= -1 
        # self.state[4] *= -1
        # self.state[10] *= -1
        # self.state[5] *= -1
        # self.state[11] *= -1
    
    def saturate(self,u,limit):
        if abs(u) > limit:
            u = limit*np.sign(u)
        return u