from Engine import PyTurbocharger as TT

import matplotlib.pyplot as plt
import numpy as np


for rho in np.linspace(0.1,0.9,10):
    xx=np.linspace(0.1,0.9,100)

    yy=[]

    for each in xx:
        yy.append(TT.effturbine(each,rho,10,0.26))


    plt.plot(xx,yy)
plt.show()
