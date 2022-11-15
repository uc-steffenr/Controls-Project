from rotorAnimation import rotorAnimation
import numpy as np
import rotorParams as P
import matplotlib.pyplot as plt
import matplotlib.animation as animation

animy = rotorAnimation()

i=0
t=0
X = P.state0
X_history = X.T
while t < P.t_end:
    T_next_plot = t + P.t_plot
    while t <= T_next_plot:
        X = X-np.array([[.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1]]).T
        t += T_next_plot
    X_history = np.append(X_history, X.T, axis=0)
    i+=1
    print(i)

ani = animation.FuncAnimation(animy.fig, animy.update, int(i), fargs=(X_history,))
plt.show()