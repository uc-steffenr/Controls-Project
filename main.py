import matplotlib.pyplot as plt
import rotorParams as P
# include signal generator
from rotorAnimation import rotorAnimation
# include dataplotter once I know how to use it
from rotorDynamics import rotorDynamics
# include controller when that works

rotor = rotorDynamics()
# reference stuff
# dataplotter

animation = rotorAnimation()
# controller

t = P.t_start

while t< P.t_end:
    t_next_plot = t + P.t_plot

    while t < t_next_plot:
        state = rotor.state
        y = rotor.update(state)
        t = t + P.Ts
    
    animation.update(state)
    # dataplot
    plt.pause(0.0001)

print('Press key to close')
plt.waitforbuttonpress()
plt.close()