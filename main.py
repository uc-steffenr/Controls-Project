import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rotorParams as P
import numpy as np
# include signal generator
from rotorAnimation import rotorAnimation
from dataPlotter import dataPlotter
from rotorDynamics import rotorDynamics
# include controller when that works

#################################################
#              SIMULATION PARAMETERS            #
#################################################
FUNCANIMATE = False 
plotList = ["x", "y", "z", "phi", "theta", "psi"]
#################################################
# TODO add sparate option for static plots
# TODO add option to funcAnimate dataPlots

rotor = rotorDynamics()
ref = np.array([0,0,0])
data = dataPlotter(plotList)
animy = rotorAnimation()
control = np.ones(1)


t = P.t_start
if FUNCANIMATE:
    x = rotor.state
    x_history = x.T
    i = 0

# outer loop... plot timesteps
while t < P.t_end:
    t_next_plot = t + P.t_plot

    # inner loop... calculate new states between plot timesteps
    while t < t_next_plot:
        f = (P.mc + 4*P.mf)*P.g/4
        F = np.array([[f],[f],[f],[f]])
        x = rotor.state
        y = rotor.update(F)
        t = t + P.Ts
    
    if FUNCANIMATE:
        x_history = np.append(x_history,x.T,axis=0)
        data.storeHistory(t,ref,x,control)
        i += 1
    else:
        animy.update(rotor.state)
        data.update(t,ref,rotor.state,control)
        plt.pause(0.0001)

# post-processing for animation or close sim
if FUNCANIMATE:
    ani = animation.FuncAnimation(animy.fig, animy.updateAnim, int(i), fargs=(x_history,))
    data.staticPlot(t,ref,x,control)
    plt.show(block=True)
else:
    print('Press key to close')
    plt.waitforbuttonpress()
    plt.close()