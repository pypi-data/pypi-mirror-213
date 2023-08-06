import Framework,Pipe,GasProperty

import numpy as np

spe=GasProperty.UDFMix({GasProperty.Air():1.0})

node=Pipe.Node1D(spe,0,1.e5,300)

r=node.righteig()

print(r)

print(np.vstack(r).T)
temp=np.vstack(r).T

l=node.lefteig()

print(np.vstack(l))
temp2=np.vstack(l)

print(np.dot(temp,temp2))

