import os
os.system('cls' if os.name == 'nt' else 'clear') #this is my line. Don't touch
import numpy as np
import rotorParams as P
import control as cnt
from numpy import array

#Doing gain calculations

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

#X motion controller
A_x = np.array([
    [0,0,1,0],
    [0,0,0,1],
    [0,-P.g,0,0],
    [0,0,0,0]
])


B_x = np.array([[0],[0],[0],[1/P.Jx]])
C_x = np.array([
    [1,0,0,0],
    [0,1,0,0]
])

zeta = .707
tr_O = 2.5
tr_I = .5
wn_O = 2.2/tr_O
wn_I = 2.2/tr_I


des_char_x = np.convolve([1, 2*zeta*wn_O, wn_O**2],
                            [1, 2*zeta*wn_I, wn_I**2])

des_poles_x = np.roots(des_char_x)


if np.linalg.matrix_rank(cnt.ctrb(A_x,B_x)) != 4:
    print('The system is not controllable')
else:
    K_x = cnt.acker(A_x,B_x,des_poles_x)
    Cr_x = np.array([[1,0,0,0]])
    kr_x = -1/(Cr_x @ np.linalg.inv(A_x-B_x@K_x)@B_x)
print('K_x: ',K_x)
print('kr_x: ',kr_x)
###############################

