import os
os.system('cls' if os.name == 'nt' else 'clear') #this is my line. Don't touch
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rotorParams as P
import numpy as np
# include signal generator
from rotorAnimation import rotorAnimation
from dataPlotter import dataPlotter
from rotorDynamics import rotorDynamics
from nuts_phil import control_deez_nuts

#################################################
#              SIMULATION PARAMETERS            #
#################################################
FUNCANIMATE = False 
ANIMATE = False
# plotList = ["x", "y", "z", "u", "v", "w"]
plotList = ["x", "y", "z"]

#################################################
# TODO add separate option for static plots
# TODO add option to funcAnimate dataPlots


rotor = rotorDynamics()
ref = np.array([3,2,1])
data = dataPlotter(plotList)
if ANIMATE:
    animy = rotorAnimation()
control = np.ones(1)
cont = control_deez_nuts()


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
        #f_tot = (P.mc + 4*P.mf)*P.g
        tau_phi = cont.updateY(ref[1], rotor.state)
        tau_theta, f_tot = cont.update(ref[0], ref[2], rotor.state)
        tau_psi = 0
        F = np.array([[f_tot],[tau_phi],[tau_theta],[tau_psi]])
        x = rotor.state
        y = rotor.update(F)
        t = t + P.Ts
    
    if ANIMATE:
    
        if FUNCANIMATE:
            x_history = np.append(x_history,x.T,axis=0)
            data.storeHistory(t,ref,x,control)
            i += 1
        else:
            animy.update(rotor.state)
            data.update(t,ref,rotor.state,control)
            plt.pause(0.0001)
            
    else:
        # print(t)
        data.storeHistory(t,ref,x,control)

if ANIMATE:
    # post-processing for animation or close sim
    if FUNCANIMATE:
        #ani = animation.FuncAnimation(animy.fig, animy.updateAnim, int(i), fargs=(x_history,))
        data.staticPlot(t,ref,x,control)
        plt.show(block=True)
    else:
        print('Press key to close')
        plt.waitforbuttonpress()
        plt.close()
        
else:
    data.staticPlot(t,ref,rotor.state,control)