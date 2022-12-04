# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:20:02 2022

@author: Evan
"""
from dataPlotter import dataPlotter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# plotList = ["x", "y", "z", 
#             "phi", "theta", "psi", 
#             "u","v", "w",
#             "p", "q", "r"]

plotList = ["x", "y", "z"]

states = np.ones(12)
ref = np.zeros(4)
control = np.ones(4)
t = 0.0

data = dataPlotter(plotList)

'''
Plot all at End Example
'''
#Start 

# for i in range(100):
#     t = i
#     states = states*1.05
#     datPlot.storeHistory(t, ref, states, control)
    
# datPlot.staticPlot(t, ref, states, control)

#End

'''
Plot Animation During Runtime example 
'''
#Start

# for i in range(100):
#     t = i
#     states = states*1.05
#     plt.pause(0.1)
#     data.update(t, ref, states, control)

#End
'''
Func Animate
'''


#Start

for i in range(100):
    t = i
    states = states*1.05
    # plt.pause(0.1)
    data.storeHistory(t, ref, states, control)

#End

refArr = np.asarray(data.refHistory)
stateArr = np.asarray(data.stateHistory)
contArr = np.asarray(data.controlHistory)



ani = animation.FuncAnimation(data.fig1, data.funcUpdate, int(i), 
                              fargs=(refArr,stateArr,contArr), 
                              interval = 10, blit = False)
# ani.save("testSave.gif", writer = animation.PillowWriter(fps = 30))
