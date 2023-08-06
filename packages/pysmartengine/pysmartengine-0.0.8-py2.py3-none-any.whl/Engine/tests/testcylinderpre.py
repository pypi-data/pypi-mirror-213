from numpy import arange
from Engine import Framework, Table,PyCylinder,CrankTrain,GasProperty
# from Engine.Cylinder import CylinderPressure,CylinderGeometry,HeatReleaseData

eng=Framework.Engine("single")

C1=PyCylinder.Cylinder(eng)

Geo=PyCylinder.PyCylinderGeometry("single")

mix=GasProperty.DieselMixture(Geo.VH*1.e5/287.15/300,0,30e-6)

Cran=CrankTrain.CrankTrain(eng).init(1400,
-110,
Geo,
[C1],
[0])


T=Table.ArrayTable().init(".//data//1400pre.csv")

# T.table[1]*=1.e5

# T.plot()

# T.plot(1)


# print(T.interp1(arange(360,540)))


Pre=PyCylinder.CylinderPressure(C1).init(T)


# Pre.PVDiagram().open()
# Pre.smooth(4).plot()

Pre.netHRR(mix).plot()

Pre.analyze()

# Pre.ploytropicIndex().plot()

Pre.PVDiagram().plot()

Pre.LogPLogV().plot()


# T.show()

# T.readcsv("1400intake.csv")

# T.plot()