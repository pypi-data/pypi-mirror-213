from Engine import Table,Turbocharger
import matplotlib.pyplot as plt,numpy as np

Turbocharger.setcompremapavi("HPC01.MAP",90000,1,1,1)

Turbocharger.setcompremapavi("LPC01.MAP",90000,1,1,1)

Turbocharger.setturmapavi("LPT01.MAP",5000,1,1,1)

# print(Turbocharger.turmaplist)