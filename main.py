import os
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