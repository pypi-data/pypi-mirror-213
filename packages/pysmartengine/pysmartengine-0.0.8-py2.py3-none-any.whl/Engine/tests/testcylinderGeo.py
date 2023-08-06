from Engine import  Framework, Table,PyCylinder,CrankTrain,GasProperty

Geo=PyCylinder.CylinderGeometryPy("Rotax914")

# Geo.plot()

Geo.powerplot(20e5)

from Engine import EnginePerform as E

print(E.BMEP(5800,70e3,1.35219e-3,4))

print(E.pim(1071059.43,1.0,1.0,0.42,300,14.3,4.395e7,287.15))

