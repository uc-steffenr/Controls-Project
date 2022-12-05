import os
os.system('cls' if os.name == 'nt' else 'clear') #this is my line. Don't touch
import numpy as np
import rotorParams as P
import control as cnt
from numpy import array

# methods to calculate damping coefficient and natural frequency
zeta = lambda Mp: np.sqrt((np.log(Mp)**2)/(np.pi**2 + np.log(Mp)**2))
wn = lambda tr,zeta: 0.5*(np.pi/(tr*np.sqrt(1-zeta**2)))

M_inner = 8

tr_x = 2
Mp_x = 0.04
zeta_x = zeta(Mp_x)
wn_x = wn(tr_x,zeta_x)

tr_th = tr_x / M_inner
zeta_th = zeta_x
wn_th = wn(tr_th,zeta_th)

tr_y = 2
Mp_y = 0.04
zeta_y = zeta(Mp_y)
wn_y = wn(tr_y,zeta_y)

tr_phi = tr_y / M_inner
zeta_phi = zeta_y
wn_phi = wn(tr_phi,zeta_phi)

tr_z = 2
Mp_z = 0.052
zeta_z = zeta(tr_z)
wn_z = wn(tr_z,zeta_z)

tr_psi = 0.3
Mp_psi = 0.0001
zeta_psi = zeta(Mp_psi)
wn_psi = wn(tr_psi,zeta_psi)


#######################################################
#       FULL STATE FEEDBACK CONTROL: X GAINS          #
#######################################################
A_x = np.array([[0,0,1,0],
                [0,0,0,1],
                [0,-P.g,0,0],
                [0,0,0,0]])

B_x = np.array([[0],
                [0],
                [0],
                [1/P.Jx]])

C_x = np.array([[1,0,0,0],
                [0,1,0,0]])


des_char_x = np.convolve([1, 2*zeta_th*wn_th, wn_th**2],
                         [1, 2*zeta_x*wn_x, wn_x**2])

des_poles_x = np.roots(des_char_x)

if np.linalg.matrix_rank(cnt.ctrb(A_x,B_x)) != 4:
    print('The system is not controllable')
else:
    K_x = cnt.acker(A_x,B_x,des_poles_x)
    Cr_x = np.array([[1,0,0,0]])
    kr_x = -1/(Cr_x @ np.linalg.inv(A_x-B_x@K_x)@B_x)
print('K_x: ',K_x)
print('kr_x: ',kr_x)
print()


#######################################################
#       FULL STATE FEEDBACK CONTROL: Y GAINS          #
#######################################################
A_y = np.array([[0,0,1,0],
               [0,0,0,1],
               [0,P.g,0,0],
               [0,0,0,0]])

B_y = np.array([[0],
               [0],
               [0],
               [1/P.Jx]])

C_y = np.array([[1,0,0,0],
               [0,1,0,0]])

des_char_poly_y = np.convolve([1,2*zeta_phi*wn_phi,wn_phi**2],
                              [1,2*zeta_y*wn_y,wn_y**2])
des_poles_y = np.roots(des_char_poly_y)

if np.linalg.matrix_rank(cnt.ctrb(A_y,B_y)) != 4:
    print('The system is not controllable')
else:
    K_y = cnt.acker(A_y,B_y,des_poles_y)
    Cr_y = np.array([[1,0,0,0]])
    kr_y = -1/(Cr_y @ np.linalg.inv(A_y - B_y @ K_y) @ B_y)
print('K_y = ',K_y)
print('kr_y = ',kr_y)
print()


#######################################################
#       FULL STATE FEEDBACK CONTROL: Z GAINS          #
#######################################################
A_z = array([[0,1],
             [0,0]])
B_z = array([[0],
             [1/P.mass]])
C_z = array([[1,0]])

des_poles_z = np.roots([1,2*zeta_z*wn_z,wn_z**2])


if np.linalg.matrix_rank(cnt.ctrb(A_z,B_z)) != 2:
    print('The system is not controllable')
else:
    K_z = cnt.acker(A_z,B_z,des_poles_z)
    Cr_z = array([[1,0]])
    kr_z = -1/(Cr_z @ np.linalg.inv(A_z - B_z @ K_z) @ B_z)
print('K_z: ',K_z)
print('kr_z: ',kr_z)
print()


#######################################################
#       FULL STATE FEEDBACK CONTROL: PSI GAINS        #
#######################################################
A_psi = np.array([[0,1],
                 [0,0]])

B_psi = np.array([[0],
                 [1/P.Jz]])

C_psi = np.array([[1,0]])

#check inner/outer in case of future bugs ( First iteration done with  outer)
des_poles_psi = np.roots([1,2*zeta_psi*wn_psi,wn_psi**2])

if np.linalg.matrix_rank(cnt.ctrb(A_psi,B_psi)) != 2:
    print('The system is not controllable')
else:
    K_psi = cnt.acker(A_psi,B_psi,des_poles_psi)
    Cr_psi = np.array([[1,0]])
    kr_psi = -1/(Cr_psi @ np.linalg.inv(A_psi - B_psi @ K_psi) @ B_psi)

print('K_psi = ',K_psi)
print('kr_psi = ',kr_psi)
