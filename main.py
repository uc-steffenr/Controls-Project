import matplotlib.pyplot as plt
import rotorParams as P
import numpy as np
from rotorAnimation import rotorAnimation
import matplotlib.animation as animation

# include signal generator
from rotorAnimation import rotorAnimation
# include dataplotter once I know how to use it
from rotorDynamics import rotorDynamics
# include controller when that works
animy = rotorAnimation()
rotor = rotorDynamics()
# reference stuff
# dataplotter

#animation = rotorAnimation()
# controller

t = P.t_start
X = P.state0
X_history = X.T
i=0
while t< P.t_end:
    t_next_plot = t + P.t_plot

    while t < t_next_plot:
        state = rotor.state
        y = rotor.update(state)
        X = rotor.state
        t = t + P.Ts
    
    #animation.update(state)
    X_history = np.append(X_history, X.T, axis=0)
    i += 1
    # dataplot
    #plt.pause(0.0001)

ani = animation.FuncAnimation(animy.fig, animy.update, int(i), fargs=(X_history,))
plt.show()

# print('Press key to close')
# plt.waitforbuttonpress()
# plt.close()