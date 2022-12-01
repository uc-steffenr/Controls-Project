import numpy as np
import matplotlib.pyplot as plt
import control as cnt
from rotorParams import *

# overall rise times, damping coefficients, and natural frequency
# wouldn't make sense to use different things for different states
inner_tr = 2.5
inner_zeta = 0.707
inner_wn = 0.5*(np.pi/(inner_tr*np.sqrt(1-inner_zeta**2)))

M = 10

outer_tr = M * inner_tr
outer_zeta = 0.707
outer_wn = 0.5*(np.pi/(outer_tr*np.sqrt(1-outer_zeta**2)))

print('inner_wn = ',inner_wn)
print('outer_wn = ',outer_wn)

# -----------------------------------
#             X CONTROL
# -----------------------------------
# inner loop -> theta
tr_th = inner_tr
zeta_th = inner_zeta
wn_th = inner_wn

tr_x = outer_tr # for overall... might change later
zeta_x = outer_zeta
wn_x = outer_wn

# -----------------------------------
#             Y CONTROL
# -----------------------------------
# inner loop -> phi
tr_phi = inner_tr
zeta_phi = inner_zeta
wn_phi = inner_wn

tr_y = outer_tr
zeta_y = outer_zeta
wn_y = outer_wn

# -----------------------------------
#             Z CONTROL
# -----------------------------------
tr_z = outer_wn
zeta_z = outer_zeta
wn_z = outer_wn

# -----------------------------------
#            PSI CONTROL
# -----------------------------------
tr_psi = outer_tr
zeta_psi = outer_zeta
wn_psi = outer_wn


M = mc + 4*mf

# A = np.array([
#     [0,0,0,0,0,0,1,0,0,0,0,0],
#     [0,0,0,0,0,0,0,1,0,0,0,0],
#     [0,0,0,0,0,0,0,0,1,0,0,0],
#     [0,0,0,0,0,0,0,0,0,1,0,0],
#     [0,0,0,0,0,0,0,0,0,0,1,0],
#     [0,0,0,0,0,0,0,0,0,0,0,1],
#     [0,0,0,0,-g,0,0,0,0,0,0,0],
#     [0,0,0,g,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0]
# ])

# B = np.array([
#     [0,0,0,0],
#     [0,0,0,0],
#     [0,0,0,0],
#     [0,0,0,0],
#     [0,0,0,0],
#     [0,0,0,0],
#     [0,0,0,0],
#     [0,0,0,0],
#     [1/M,0,0,0],
#     [0,1/Jx,0,0],
#     [0,0,1/Jy,0],
#     [0,0,0,1/Jz]
# ])

# NUM_ROWS = 6 # in case we want to change output matrix C to 6x12
# C = np.array([[1 if i == j else 0 for j in range(12)] for i in range(NUM_ROWS)])
# # print(C)

# des_char_poly = np.array([1,2*zeta*wn,wn**2])
# des_poles = np.roots(des_char_poly)

# if np.linalg.matrix_rank(cnt.ctrb(A,B)) != 12:
#     print('System is not controllable')
# else:
#     K = cnt.acker(A,B,des_poles)
#     Cr = np.array([
#         [1,0,0,0,0,0,0,0,0,0,0,0],
#         [0,1,0,0,0,0,0,0,0,0,0,0],
#         [0,0,1,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,1,0,0,0,0,0,0]
#     ])
#     kr = -1.0/(Cr @ np.linalg.inv(A - B @ K) @ B)

# print('K = ',K)
# print('kr = ',kr)

#################################################################
#                    Full State Feedback: X
#################################################################
# x = [x,theta,u,q]
# xdot = [u,q,udot,qdot]
Ax = np.array([
    [0,0,1,0],
    [0,0,0,1],
    [0,-g,0,0],
    [0,0,0,0]
])
Bx = np.array([
    [0],
    [0],
    [0],
    [1/Jy]
])
Cy = np.array([
    [1,0,0,0],
    [0,1,0,0]
])

des_char_poly_x = np.convolve([1,2*zeta_th*wn_th,wn_th**2],
                              [1,2*zeta_x*wn_x,wn_x**2])
des_poles_x = np.roots(des_char_poly_x)

if np.linalg.matrix_rank(cnt.ctrb(Ax,Bx)) != 4:
    print('The system is not controllable')
else:
    Kx = cnt.acker(Ax,Bx,des_poles_x)
    Cr_x = np.array([[1,0,0,0]])
    krx = -1/(Cr_x @ np.linalg.inv(Ax - Bx @ Kx) @ Bx)

print('Kx = ',Kx)
print('krx = ',krx)

#################################################################
#                    Full State Feedback: Y 
#################################################################
# x = [y,phi,v,p] (lmao wifi and vp)
Ay = np.array([
    [0,0,1,0],
    [0,0,0,1],
    [0,g,0,0],
    [0,0,0,0]
])
By = np.array([
    [0],
    [0],
    [0],
    [1/Jx]
])
Cy = np.array([
    [1,0,0,0],
    [0,1,0,0]
])

des_char_poly_y = np.convolve([1,2*zeta_phi*wn_phi,wn_phi**2],
                              [1,2*zeta_y*wn_y,wn_y**2])
des_poles_y = np.roots(des_char_poly_y)

if np.linalg.matrix_rank(cnt.ctrb(Ay,By)) != 4:
    print('The system is not controllable')
else:
    Ky = cnt.acker(Ay,By,des_poles_y)
    Cr_y = np.array([[1,0,0,0]])
    kry = -1/(Cr_y @ np.linalg.inv(Ay - By @ Ky) @ By)

print('Ky = ',Ky)
print('kry = ',kry)

#################################################################
#                    Full State Feedback: Z 
#################################################################
# x = [z,w]
# xdot = [w,wdot]
Az = np.array([
    [0,1],
    [0,0]
])
Bz = np.array([
    [0],
    [1/M]
])
Cz = np.array([
    [1,0]
])

# des_char_poly_x = np.convolve([1,2*zeta_th*wn_th,wn_th**2],
#                               [1,2*zeta_x*wn_x,wn_x**2])
des_poles_z = np.roots([1,2*zeta_z*wn_z,wn_z**2])

if np.linalg.matrix_rank(cnt.ctrb(Az,Bz)) != 2:
    print('The system is not controllable')
else:
    Kz = cnt.acker(Az,Bz,des_poles_z)
    Cr_z = np.array([[1,0]])
    krz = -1/(Cr_z @ np.linalg.inv(Az - Bz @ Kz) @ Bz)

print('Kz = ',Kz)
print('krz = ',krz)

#################################################################
#                    Full State Feedback: Psi
#################################################################
# x = [psi,r]
# xdot = [r,rdot]
Apsi = np.array([
    [0,1],
    [0,0]
])
Bpsi = np.array([
    [0],
    [1/Jz]
])
Cpsi = np.array([
    [1,0]
])

# des_char_poly_x = np.convolve([1,2*zeta_th*wn_th,wn_th**2],
#                               [1,2*zeta_x*wn_x,wn_x**2])
des_poles_psi = np.roots([1,2*zeta_psi*wn_psi,wn_psi**2])

if np.linalg.matrix_rank(cnt.ctrb(Apsi,Bpsi)) != 2:
    print('The system is not controllable')
else:
    Kpsi = cnt.acker(Apsi,Bpsi,des_poles_psi)
    Cr_psi = np.array([[1,0]])
    krpsi = -1/(Cr_psi @ np.linalg.inv(Apsi - Bpsi @ Kpsi) @ Bpsi)

print('Kpsi = ',Kpsi)
print('krpsi = ',krpsi)