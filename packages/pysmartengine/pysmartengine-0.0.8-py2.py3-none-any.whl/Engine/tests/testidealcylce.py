
from Engine import Framework, Table,Cylinder,CrankTrain,GasProperty,Valve,Volume


lift=Valve.ValveLift().init();
lift.move_timing(-390,-170)
# lift.data.plot()

lift2=Valve.ValveLift().init();
lift2.move_timing(160,390)
# lift2.data.plot()

eng=Framework.Engine("WP7")

V1=Valve.Valve(eng).init(lift) 

# V1.lift.data.plot()


V2=Valve.Valve(eng).init(lift2)

vol=Volume.Volume(eng)
vol2=Volume.Volume(eng)

C1=Cylinder.Cylinder(eng)

#进气
V1.connect(vol.getport(1),C1.getport(1))

#排气门
V2.connect(C1.getport(2),vol2.getport(1))


Geo=Cylinder.CylinderGeometry("WP7").init(108e-3,130e-3,17,209.7e-3)

Cran=CrankTrain.CrankTrain(eng).init(1400,
-110,
Geo,
[C1],
[0])

I=Cylinder.IdealCycle(C1)

I.compress()
I.burn()
I.expense()
I.gasexchange().plot()
I.Cylinder.Pressure.analyze()
