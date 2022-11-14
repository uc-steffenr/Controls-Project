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

# ----------------------------------------------
#             INITIAL CONDITIONS
# ----------------------------------------------
x0 = 12
y0 = -5
z0 = 9
phi0 = 30 * np.pi/180
theta0 = -30 * np.pi/180
psi0 = 45 * np.pi/180

xdot0 = 0.0
ydot0 = 0.0
zdot0 = 0.0
phidot0 = 0.0
thetadot0 = 0.0
psidot0 = 0.0

# ----------------------------------------------
#           SIMULATION PARAMETERS
# ----------------------------------------------
t_start = 0
t_end = 50
Ts = 0.001
t_plot = 0.1