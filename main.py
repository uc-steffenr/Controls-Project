import matplotlib.pyplot as plt
import rotorParams as P
import numpy as np
# include signal generator
from rotorAnimation import rotorAnimation
# include dataplotter once I know how to use it
from dataPlotter import dataPlotter
from rotorDynamics import rotorDynamics
# include controller when that works

plotList = ["x", "y", "z", "phi", "theta", "psi"]

rotor = rotorDynamics()
# reference stuff
ref = np.array([0,0,0])
# dataplotter
data = dataPlotter(plotList)

animation = rotorAnimation()
# controller
control = np.ones(1)

t = P.t_start

while t< P.t_end:
    t_next_plot = t + P.t_plot

    while t < t_next_plot:
        f = (P.mc + 4*P.mf)*P.g/4
        F = np.array([[f],[f],[f],[f]])
        y = rotor.update(F)
        t = t + P.Ts
    
    animation.update(rotor.state)
    data.update(t,ref,rotor.state,control)
    # dataplot
    plt.pause(0.0001)

print('Press key to close')
plt.waitforbuttonpress()
plt.close()