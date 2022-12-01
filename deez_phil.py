import os
os.system('cls' if os.name == 'nt' else 'clear') #this is my line. Don't touch
import numpy as np
import rotorParams as P
import control as cnt
from numpy import array

# Doing gain calculations
zeta_O = 0.707
tr_O = 1.5
wn_O = 0.5*(np.pi/(tr_O*np.sqrt(1-zeta_O**2)))

zeta_I = 0.707
tr_I = 0.5
wn_I = 0.5*(np.pi/(tr_I*np.sqrt(1-zeta_I**2)))

# M_inner = 10

# tr_x = 0.4
# Mp_x = 0.04
# zeta_x = np.sqrt((np.log(Mp_x)**2)/(np.pi**2 + np.log(Mp_x)**2))
# wn_x = 0.5*(np.pi/(tr_x*np.sqrt(1-zeta_x**2)))

# print(zeta_x)
# print(wn_x)

# tr_th = tr_x / M_inner
# zeta_th = zeta_x
# wn_th = 0.5*(np.pi/(tr_th*np.sqrt(1-zeta_th**2)))

# tr_y = 0.4
# Mp_y = 0.04
# zeta_y = np.sqrt((np.log(Mp_y)**2)/(np.pi**2 + np.log(Mp_y)**2))
# wn_y = 0.5*(np.pi/(tr_y*np.sqrt(1-zeta_y**2)))

# tr_phi = tr_y / M_inner
# zeta_phi = zeta_y
# wn_phi = 0.5*(np.pi/(tr_phi*np.sqrt(1-zeta_phi**2)))

# tr_z = 0.47
# Mp_z = 0.052
# zeta_z = np.sqrt((np.log(Mp_z)**2)/(np.pi**2 + np.log(Mp_z)**2))
# wn_z = 0.5*(np.pi/(tr_z*np.sqrt(1-zeta_z**2)))

# tr_psi = 0.31
# Mp_psi = 0.042
# zeta_psi = np.sqrt((np.log(Mp_psi)**2)/(np.pi**2 + np.log(Mp_psi)**2))
# wn_psi = 0.5*(np.pi/(tr_psi*np.sqrt(1-zeta_psi**2)))


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

des_char_x = np.convolve([1, 2*zeta_I*wn_I, wn_I**2],
                         [1, 2*zeta_O*wn_O, wn_O**2])

des_poles_x = np.roots(des_char_x)

if np.linalg.matrix_rank(cnt.ctrb(A_x,B_x)) != 4:
    print('The system is not controllable')
else:
    K_x = cnt.acker(A_x,B_x,des_poles_x)
    Cr_x = np.array([[1,0,0,0]])
    kr_x = -1/(Cr_x @ np.linalg.inv(A_x-B_x@K_x)@B_x)
print('K_x: ',K_x)
print('kr_x: ',kr_x)
#end x motion gains

# x = [y,phi,v,p] (lmao wifi and vp)

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

des_char_poly_y = np.convolve([1,2*zeta_I*wn_I,wn_I**2],
                              [1,2*zeta_O*wn_O,wn_O**2])
des_poles_y = np.roots(des_char_poly_y)

if np.linalg.matrix_rank(cnt.ctrb(A_y,B_y)) != 4:
    print('The system is not controllable')
else:
    K_y = cnt.acker(A_y,B_y,des_poles_y)
    Cr_y = np.array([[1,0,0,0]])
    kr_y = -1/(Cr_y @ np.linalg.inv(A_y - B_y @ K_y) @ B_y)

print('K_y = ',K_y)
print('kr_y = ',kr_y)

#z motion gains
A_z = array([[0,1],
             [0,0]])

B_z = array([[0],
             [1/P.mass]])

C_z = array([[1,0]])

des_poles_z = np.roots([1,2*zeta_O*wn_O,wn_O**2])

if np.linalg.matrix_rank(cnt.ctrb(A_z,B_z)) != 2:
    print('The system is not controllable')
else:
    K_z = cnt.acker(A_z,B_z,des_poles_z)
    Cr_z = array([[1,0]])
    kr_z = -1/(Cr_z @ np.linalg.inv(A_z - B_z @ K_z) @ B_z)
print('K_z: ',K_z)
print('kr_z: ',kr_z)


# x = [psi,r]
# xdot = [r,rdot]

A_psi = np.array([[0,1],
                 [0,0]])

B_psi = np.array([[0],
                 [1/P.Jz]])

C_psi = np.array([[1,0]])

# des_char_poly_x = np.convolve([1,2*zeta_th*wn_th,wn_th**2],
#                               [1,2*zeta_x*wn_x,wn_x**2])

#check inner/outer in case of future bugs ( First iteration done with  outer)
des_poles_psi = np.roots([1,2*zeta_O*wn_O,wn_O**2])

if np.linalg.matrix_rank(cnt.ctrb(A_psi,B_psi)) != 2:
    print('The system is not controllable')
else:
    K_psi = cnt.acker(A_psi,B_psi,des_poles_psi)
    Cr_psi = np.array([[1,0]])
    kr_psi = -1/(Cr_psi @ np.linalg.inv(A_psi - B_psi @ K_psi) @ B_psi)

print('K_psi = ',K_psi)
print('kr_psi = ',kr_psi)
