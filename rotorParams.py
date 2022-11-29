import numpy as np
# from numpy import sin,cos as s,c
import matplotlib.pyplot as plt

# ----------------------------------------------
#         MASSES AND MOMENTS OF INERTIA
# ----------------------------------------------
mc = 0.5 # kg
mf = 0.2 # kg
Jc = 2
Jf = 2 # these are placeholders for real numbers

# ----------------------------------------------
#             DIMENSIONS OF ROTOR
# ----------------------------------------------
sc = 0.05 # m -> length of side of square
d = 0.04 # m -> length of rod connecting fan to center
rf = 0.03 # m -> radius of fan
h = 0.02 # m -> thickness of center
leg_l = 0.005 # m -> length of landing legs

# ----------------------------------------------
#             INITIAL CONDITIONS
# ----------------------------------------------
x0 = 0
y0 = 0
z0 = 0
phi0 = 0 * np.pi/180
theta0 = 0 * np.pi/180
psi0 = 0 * np.pi/180

xdot0 = 0.0
ydot0 = 0.0
zdot0 = 0.0
phidot0 = 0.0
thetadot0 = 0.0
psidot0 = 0.0
state0 = np.array([[x0,y0,z0,phi0,theta0,psi0,xdot0,ydot0,zdot0,phidot0,thetadot0,psidot0]]).T

# ----------------------------------------------
#           SIMULATION PARAMETERS
# ----------------------------------------------
t_start = 0
t_end = 50
Ts = 0.001
t_plot = 0.1