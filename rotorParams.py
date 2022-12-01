import numpy as np
# from numpy import sin,cos as s,c
import matplotlib.pyplot as plt

# ----------------------------------------------
#             DIMENSIONS OF ROTOR
# ----------------------------------------------

sc = 0.05 # m -> length of side of square
d = 0.04 # m -> length of rod connecting fan to center
rf = 0.03 # m -> radius of fan
h = 0.02 # m -> thickness of center
leg_l = 0.005 # m -> length of landing legs

# ----------------------------------------------
#         MASSES AND MOMENTS OF INERTIA
# ----------------------------------------------
mc = 0.5 # kg
mf = 0.2 # kg

# from https://en.wikipedia.org/wiki/List_of_moments_of_inertia
# and https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=2324&context=facpub
Jx = (1/12)*mc*(sc**2 + h**2) + 2*d**2*mf
Jy = (1/12)*mc*(sc**2 + h**2) + 2*d**2*mf
Jz = (1/12)*mc*2*sc**2 + 4*d**2*mf
# essentially just sum of rectangular prism J and off-axis point mass J

# ----------------------------------------------
#               OTHER PARAMETERS
# ----------------------------------------------
g = 9.81
mu_x = 0.1
mu_y = 0.1
mu_z = 0.1
F_max = 15 # N

# ----------------------------------------------
#             INITIAL CONDITIONS
# ----------------------------------------------
x0 = 0
y0 = 0
z0 = 0
phi0 = 0 * np.pi/180
theta0 = 0 * np.pi/180
psi0 = 15 * np.pi/180

xdot0 = 0.0
ydot0 = 0.0
zdot0 = 0.0
phidot0 = 0.0 * np.pi/180
thetadot0 = 0.0 * np.pi/180
psidot0 = 10.0 * np.pi/180

# ----------------------------------------------
#           SIMULATION PARAMETERS
# ----------------------------------------------
t_start = 0
t_end = 50
Ts = 0.001
t_plot = 0.1