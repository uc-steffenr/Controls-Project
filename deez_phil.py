import os
os.system('cls' if os.name == 'nt' else 'clear') #this is my line. Don't touch
import numpy as np
import rotorParams as P
import control as cnt
from numpy import array

#Doing gain calculations
zeta_O = 0.707
tr_O = 2.0
wn_O = 0.5*(np.pi/(tr_O*np.sqrt(1-zeta_O**2)))


zeta_I = 0.707
tr_I = 2.5
wn_I = 0.5*(np.pi/(tr_I*np.sqrt(1-zeta_I**2)))

# wn_I = 2.2/tr_I
# wn_O = 2.2/tr_O

#big matrices
A = array([[0,0,0,0,0,0,1,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,1,0,0],
           [0,0,0,0,0,0,0,0,0,0,1,0],
           [0,0,0,0,0,0,0,0,0,0,0,1],
           [0,0,0,0,0,0,0,0,0,0,-P.g,0],
           [0,0,0,0,0,0,0,0,0,P.g,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0]])

B = array([[0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [1/P.mass,0,0,0],
           [0,1/P.Jx,0,0],
           [0,0,1/P.Jy,0],
           [0,0,0,1/P.Jz]])

C = array([[1,0,0,0,0,0,0,0,0,0,0,0],
           [0,1,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0],
           [0,0,0,1,0,0,0,0,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,0],
           [0,0,0,0,0,1,0,0,0,0,0,0]])

#X motion gains
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

des_char_x = np.convolve([1, 2*zeta_O*wn_O, wn_O**2],
                         [1, 2*zeta_I*wn_I, wn_I**2])

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


# x = [y,phi,v,p] (lmao wifi and vp)

Ay = np.array([[0,0,1,0],
               [0,0,0,1],
               [0,P.g,0,0],
               [0,0,0,0]])

By = np.array([[0],
               [0],
               [0],
               [1/P.Jx]])

Cy = np.array([[1,0,0,0],
               [0,1,0,0]])

des_char_poly_y = np.convolve([1,2*zeta_I*wn_I,wn_I**2],
                              [1,2*zeta_O*wn_O,wn_O**2])
des_poles_y = np.roots(des_char_poly_y)

if np.linalg.matrix_rank(cnt.ctrb(Ay,By)) != 4:
    print('The system is not controllable')
else:
    K_y = cnt.acker(Ay,By,des_poles_y)
    Cr_y = np.array([[1,0,0,0]])
    kr_y = -1/(Cr_y @ np.linalg.inv(Ay - By @ K_y) @ By)

print('Ky = ',K_y)
print('kry = ',kr_y)

# x = [psi,r]
# xdot = [r,rdot]

Apsi = np.array([[0,1],
                 [0,0]])

Bpsi = np.array([[0],
                 [1/P.Jz]])

Cpsi = np.array([[1,0]])

# des_char_poly_x = np.convolve([1,2*zeta_th*wn_th,wn_th**2],
#                               [1,2*zeta_x*wn_x,wn_x**2])

#check inner/outer in case of future bugs ( First iteration done with  outer)
des_poles_psi = np.roots([1,2*zeta_O*wn_O,wn_O**2])

if np.linalg.matrix_rank(cnt.ctrb(Apsi,Bpsi)) != 2:
    print('The system is not controllable')
else:
    K_psi = cnt.acker(Apsi,Bpsi,des_poles_psi)
    Cr_psi = np.array([[1,0]])
    kr_psi = -1/(Cr_psi @ np.linalg.inv(Apsi - Bpsi @ K_psi) @ Bpsi)

print('Kpsi = ',K_psi)
print('krpsi = ',kr_psi)
