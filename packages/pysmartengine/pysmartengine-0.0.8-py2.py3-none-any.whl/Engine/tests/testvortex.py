from Engine import Pipe,GasProperty

air=GasProperty.Air()

import matplotlib.pyplot as plt
import numpy as np


V=Pipe.RankineVortex(10,air,10,1.e5)
V2=Pipe.RankineVortex(10,air,12,1.e5)

yy=[]

yy2=[]
for i in np.linspace(-100,100,1000):
    yy.append(V.V(i))
    yy2.append(V2.V(i))

plt.plot(np.linspace(-100,100,1000),yy)
plt.plot(np.linspace(-100,100,1000),yy2)

plt.show()
