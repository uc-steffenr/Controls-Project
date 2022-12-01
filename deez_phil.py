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
