# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:20:02 2022

@author: Evan
"""
from dataPlotter import dataPlotter
import numpy as np
import matplotlib.pyplot as plt

# plotList = ["x", "y", "z", 
#             "phi", "theta", "psi", 
#             "u","v", "w",
#             "p", "q", "r"]

plotList = ["x", "y", "z", "psi", "theta"]

states = np.ones(12)
ref = np.zeros(4)
control = np.ones(4)
t = 0.0

datPlot = dataPlotter(plotList)

'''
Plot all at End Example
'''
#Start 

for i in range(100):
    t = i
    states = states*1.05
    datPlot.storeHistory(t, ref, states, control)
    
datPlot.staticPlot(t, ref, states, control)

#End

'''
Plot Animation During Runtime example 
'''
#Start

# for i in range(100):
#     t = i
#     states = states*1.05
#     plt.pause(0.1)
#     datPlot.update(t, ref, states, control)

#End
