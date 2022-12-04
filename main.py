import os
<<<<<<< HEAD
os.system('cls' if os.name == 'nt' else 'clear')
from rotorAnimation import rotorAnimation
import numpy as np
import roto_params_phil as P
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dynamics_phil import VTOLDynamics

dyno = VTOLDynamics()
animy = rotorAnimation()

i=0
t=0
X = P.state0
X_history = X.T
u=[1,1,1,1]
while t < P.t_end:
    T_next_plot = t + P.t_plot
    while t <= T_next_plot:
        #X = X-np.array([[.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1]]).T
        dyno.update(u)
        X = dyno.state
        t += P.Ts
    X_history = np.append(X_history, X.T, axis=0)
    t = t + P.t_plot
    i+=1

ani = animation.FuncAnimation(animy.fig, animy.update, int(i), fargs=(X_history,))
plt.show()
=======
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
from path_follow import pathFollow


#################################################
#              SIMULATION PARAMETERS            #
#################################################
FUNCANIMATE = True 
ANIMATE = True
# plotList = ["x", "y", "z", "u", "v", "w"]
plotList = ["x", "y", "z", "phi", "theta", "psi"]
# plotList = ["psi"]



#################################################
# TODO add separate option for static plots
# TODO add option to funcAnimate dataPlots


rotor = rotorDynamics()
path = pathFollow()
ref = path.current_ref
#ref = np.array([3,3,1, np.deg2rad(15)])
data = dataPlotter(plotList)
#data = 'off'

if ANIMATE:
    animy = rotorAnimation()
control = np.ones(1)
cont = control_deez_nuts()


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

        #f_tot = (P.mc + 4*P.mf)*P.g
        tau_phi = cont.updateY(ref[1], rotor.state)
        tau_theta, f_tot = cont.update(ref[0], ref[2], rotor.state)
        tau_psi = cont.updatePsi(ref[3], rotor.state)
        F = np.array([[f_tot],[tau_phi],[tau_theta],[tau_psi]])
        x = rotor.state
        ref = path.update(x)
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
        # print(t)
        data.storeHistory(t,ref,x,control)

if ANIMATE:
    # post-processing for animation or close sim
    if FUNCANIMATE:
        print()
        print('frame count:', i)
        ani = animation.FuncAnimation(animy.fig, animy.updateAnim, int(i), fargs=(x_history,time_history,),  interval=1, blit=False)
        print('saving...')
        data.staticPlot(t,ref,x,control)
        #plt.show(block=True)
        ani.save("movie.gif", writer=animation.PillowWriter(fps=30))
        print('done')
    else:
        print('Press key to close')
        plt.waitforbuttonpress()
        plt.close()
        
else:
    data.staticPlot(t,ref,rotor.state,control)
    plt.show(block=True)
>>>>>>> c665eabe54a326ed05fedc80162643b44460a019
