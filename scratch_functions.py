import numpy as np

def zeta(Mp): return np.sqrt((np.log(Mp)**2)/(np.log(Mp)**2+np.pi**2))
def omega_n(tr, zeta): return np.pi/(tr*2)*1/(np.sqrt(1-zeta**2))

print(zeta(.01))