import os
os.system('cls' if os.name == 'nt' else 'clear') #this is my line. Don't touch
import numpy as np
import rotorParams as P
import control as cnt
from numpy import array

# TODO tune gains for figure eight path

# methods to calculate damping coefficient and natural frequency
zeta = lambda Mp: np.sqrt((np.log(Mp)**2)/(np.pi**2 + np.log(Mp)**2))
wn = lambda tr,zeta: 0.5*(np.pi/(tr*np.sqrt(1-zeta**2)))

M_inner = 8

#--------------------------------------------
#               x parameters
# -------------------------------------------
tr_x = 1
Mp_x = 0.04
zeta_x = zeta(Mp_x)
wn_x = wn(tr_x,zeta_x)
x_integrator = -20

tr_th = tr_x / M_inner
zeta_th = zeta_x
wn_th = wn(tr_th,zeta_th)

#--------------------------------------------
#               y parameters
# -------------------------------------------
tr_y = 1
Mp_y = 0.04
zeta_y = zeta(Mp_y)
wn_y = wn(tr_y,zeta_y)
y_integrator = -10

tr_phi = tr_y / M_inner
zeta_phi = zeta_y
wn_phi = wn(tr_phi,zeta_phi)

#--------------------------------------------
#               z parameters
# -------------------------------------------
tr_z = 0.35
Mp_z = 0.04
zeta_z = zeta(tr_z)
wn_z = wn(tr_z,zeta_z)
z_integrator = -60

#--------------------------------------------
#               psi parameters
# -------------------------------------------
tr_psi = 0.3
Mp_psi = 0.0001
zeta_psi = zeta(Mp_psi)
wn_psi = wn(tr_psi,zeta_psi)
psi_integrator = -1


#######################################################
#                   FSFBI: X GAINS                    #
#######################################################
A_x = np.array([[0,0,1,0],
                [0,0,0,1],
                [0,-P.g,0,0],
                [0,0,0,0]])
B_x = np.array([[0],
                [0],
                [0],
                [1/P.Jx]])
Cr_x = np.array([1,0,0,0])

A1_x = np.vstack((np.hstack((A_x, np.zeros((np.size(A_x,1),1)))),
                  np.hstack((-Cr_x,0))))
B1_x = np.vstack((B_x,0))

integrator_pole_x = np.array([x_integrator])
des_char_poly_x = np.convolve(np.convolve([1,2*zeta_th*wn_th,wn_th**2],
                                          [1,2*zeta_x*wn_x,wn_x**2]),
                                          np.poly([integrator_pole_x]))
des_poles_x = np.roots(des_char_poly_x)

if np.linalg.matrix_rank(cnt.ctrb(A1_x,B1_x)) != 5:
    print('The system is not controllable')
else:
    K1_x = cnt.acker(A1_x,B1_x,des_poles_x)
    K_x = np.array([[K1_x.item(0),K1_x.item(1),K1_x.item(2),K1_x.item(3)]])
    ki_x = K1_x.item(4)
    print('K_x = ',K_x)
    print('ki_x = ',ki_x)

#######################################################
#                   FSFBI: Y GAINS                    #
#######################################################
A_y = np.array([[0,0,1,0],
               [0,0,0,1],
               [0,P.g,0,0],
               [0,0,0,0]])
B_y = np.array([[0],
               [0],
               [0],
               [1/P.Jx]])
Cr_y = np.array([1,0,0,0])

A1_y = np.vstack((np.hstack((A_y, np.zeros((np.size(A_y,1),1)))),
                  np.hstack((-Cr_y,0))))
B1_y = np.vstack((B_y,0))

integrator_pole_y = np.array([y_integrator])
des_char_poly_y = np.convolve(np.convolve([1,2*zeta_phi*wn_phi,wn_phi**2],
                                          [1,2*zeta_y*wn_y,wn_y**2]),
                                          np.poly([integrator_pole_y]))
des_poles_y = np.roots(des_char_poly_y)

if np.linalg.matrix_rank(cnt.ctrb(A1_y,B1_y)) != 5:
    print('The system is not controllable')
else:
    K1_y = cnt.acker(A1_y,B1_y,des_poles_y)
    K_y = np.array([[K1_y.item(0),K1_y.item(1),K1_y.item(2),K1_y.item(3)]])
    ki_y = K1_y.item(4)
    print('K_y = ',K_y)
    print('ki_y = ',ki_y)

#######################################################
#                   FSFBI: Z GAINS                    #
#######################################################
A_z = array([[0,1],
             [0,0]])
B_z = array([[0],
             [1/P.mass]])
Cr_z = np.array([1,0])

A1_z = np.vstack((np.hstack((A_z, np.zeros((np.size(A_z,1),1)))),
                  np.hstack((-Cr_z,0))))
B1_z = np.vstack((B_z,0))

integrator_pole_z = np.array([z_integrator])
des_char_poly_z = np.convolve([1,2*zeta_z*wn_z,wn_z**2],np.poly([integrator_pole_z]))
des_poles_z = np.roots(des_char_poly_z)

if np.linalg.matrix_rank(cnt.ctrb(A1_z,B1_z)) != 3:
    print('The system is not controllable')
else:
    K1_z = cnt.acker(A1_z,B1_z,des_poles_z)
    K_z = np.array([[K1_z.item(0),K1_z.item(1)]])
    ki_z = K1_y.item(2)
    print('K_z = ',K_z)
    print('ki_z = ',ki_z)

#######################################################
#                  FSFBI: PSI GAINS                   #
#######################################################
A_psi = np.array([[0,1],
                 [0,0]])
B_psi = np.array([[0],
                 [1/P.Jz]])
Cr_psi = np.array([1,0])

A1_psi = np.vstack((np.hstack((A_psi, np.zeros((np.size(A_psi,1),1)))),
                  np.hstack((-Cr_psi,0))))
B1_psi = np.vstack((B_psi,0))

integrator_pole_psi = np.array([psi_integrator])
des_char_poly_psi = np.convolve([1,2*zeta_psi*wn_psi,wn_psi**2],np.poly([integrator_pole_psi]))
des_poles_psi = np.roots(des_char_poly_psi)

if np.linalg.matrix_rank(cnt.ctrb(A1_psi,B1_psi)) != 3:
    print('The system is not controllable')
else:
    K1_psi = cnt.acker(A1_psi,B1_psi,des_poles_psi)
    K_psi = np.array([[K1_psi.item(0),K1_psi.item(1)]])
    ki_psi = K1_psi.item(2)
    print('K_psi = ',K_psi)
    print('ki_psi = ',ki_psi)