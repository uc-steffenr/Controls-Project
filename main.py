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
from rotorController import rotorController
from path_follow import pathFollow

# General todo list:
# - TODO fix psi tracking
# - TODO add wind
# - TODO calculate individual fan forces and/or angular rates 
#        and saturate them
# - TODO vary physical parameters in dynamics (using like the
#         alpha terms from the homeworks)


#################################################
#              SIMULATION PARAMETERS            #
#################################################
FUNCANIMATE = False 
ANIMATE = True
# plotList = ["x", "y", "z", "u", "v", "w"]
plotList = ["x", "y", "z", "phi", "theta", "psi"]


rotor = rotorDynamics()
path = pathFollow()
ref = path.current_ref
#ref = np.array([3,3,1, np.deg2rad(15)])
data = dataPlotter(plotList)

if ANIMATE:
    # options are 'follow', 'zoomed out', or 'both'
    animy = rotorAnimation('both')
control = np.ones(1)
cont = rotorController(type='FSFBI')

t = P.t_start
if FUNCANIMATE:
    x = rotor.state
    time_history = []
    x_history = x.T
    i = 0

# outer loop... plot timesteps
while t < P.t_end:
    t_next_plot = t + P.t_plot

    # inner loop... calculate new states between plot timesteps
    while t < t_next_plot:
        Ftot,tau_phi,tau_theta,tau_psi = cont.update(ref[0],ref[1],ref[2],ref[3],rotor.state)
        F = np.array([[Ftot],[tau_phi],[tau_theta],[tau_psi]])
        x = rotor.state
        # ref = path.update(x,0.1)
        ref = path.update_Nate()
        y = rotor.update(F)
        t = t + P.Ts
    
    if ANIMATE:    
        if FUNCANIMATE:
            x_history = np.append(x_history,x.T,axis=0)
            time_history.append(t)
            data.storeHistory(t,ref,x,control)
            i += 1
        else:
            animy.update(rotor.state)
            data.update(t,ref,rotor.state,control)
            plt.pause(0.0001)
            
    else:
        data.storeHistory(t,ref,x,control)

if ANIMATE:
    # post-processing for animation or close sim
    if FUNCANIMATE:
        print()
        print('frame count:', i)
        ani = animation.FuncAnimation(animy.fig, animy.updateAnim, int(i), fargs=(x_history,time_history,),  interval=1, blit=False)
        print('saving...')
        data.staticPlot(t,ref,x,control)
        # plt.show(block=True)
        ani.save("FSFBI_Video.gif", writer=animation.PillowWriter(fps=30))
        print('done')
    else:
        print('Press key to close')
        plt.waitforbuttonpress()
        plt.close()
        
else:
    data.staticPlot(t,ref,rotor.state,control)
    plt.show(block=True)
