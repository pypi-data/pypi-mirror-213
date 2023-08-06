from Engine import Framework,Pipe,Orifice,Environment,GasProperty,Valve,Cylinder,Volume

Framework.GPU()

Mix=GasProperty.UDFMix({GasProperty.Air():1})

#创建所有参考
inits=GasProperty.initstate("init").init(Mix,1.e5,300)
#创建所有参考
inits2=GasProperty.initstate("init2").init(Mix,3.e5,300)

inits3=GasProperty.initstate("init3").init(Mix,4e5,300)

# Mix2=GasProperty.species({"Air":0.7,"N2":0.30})

#创建发动机
Eng=Framework.Engine("WP7")

V=Valve.ValveSimple(Eng).init(0.001,type=0)

V2=Valve.ValveSimple(Eng).init(0.001,type=0)

Vol=Volume.Volume(Eng).init(inits)

Vol2=Volume.Volume(Eng).init(inits2)

Vol3=Volume.Volume(Eng).init(inits3)

V.connect(Vol.getport(1),Vol2.getport(1))
V2.connect(Vol2.getport(2),Vol3.getport(1))


S=Framework.Sensor().connect(Vol3.getport("p"))
S2=Framework.Sensor().connect(V.getport("mass")) 


Eng.init()
Eng.tstep=0.001

# for i in range(10000):
#     Eng.nextstep()
# Eng.nextstep()

# Eng.nextstep()

# Eng.nextstep()

# for i in range(100):
#     Eng.nextstep()
#     print(S.data)

xx=[];yy=[]

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
win = pg.GraphicsLayoutWidget(show=True)
curve = win.addPlot().plot(pen='y')

def update():
    Eng.nextstep()
    xx.append(Eng.tnow)
    yy.append(S.data)
    curve.setData(xx,yy)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
pg.exec()
