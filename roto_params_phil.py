import numpy as np

# Physical Constants
m = 0.1         #kg
Ixx = 0.00062   #kg-m^2
Iyy = 0.00113   #kg-m^2
Izz = 0.9*(Ixx + Iyy) #kg-m^2 (Assume nearly flat object, z=0)
dx = 0.114      #m
dy = 0.0825     #m
g = 9.81  #m/s/s
DTR = 1/57.3; RTD = 57.3

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


#simulation params:
Ts = .01
t_end = 200
t_plot = .1