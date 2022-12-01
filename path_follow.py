import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def figureEight(num_points=20, width=3, height=3):
    t = np.linspace(0,2*np.pi, num_points)
    x = np.sin(t)*width
    y = np.sin(t)*np.cos(t)*2*height
    return x,y

