from Engine import Framework,Pipe,Orifice,Environment,GasProperty,Valve

#创建发动机
Eng=Framework.Engine("WP7")

spe=GasProperty.UDFMix({GasProperty.Air():1.0})

#创建所有参考
inits=GasProperty.initstate("init").init(spe,1.e5,300)

inits2=GasProperty.initstate("init2").init(spe,5.e5,300)

#创建部件
P1=Pipe.PipeRound(Eng).init(inits,30e-3,100e-3,1e-3)

E=Environment.Env(Eng).init(inits2).clone(2)

V=Valve.ValveSimple(Eng).init(10e-3,0)

O=Orifice.Orifice(Eng)

O.connect(E[0].getport(1),P1.getport(1))

V.connect(P1.getport(2),E[1].getport(1))

# 声明两个传感器
S1=Framework.Sensor().connect(P1.getport("p"))
S2=Framework.Sensor().connect(P1.getport("x"))

Eng.init()

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
win = pg.GraphicsLayoutWidget(show=True)
curve = win.addPlot().plot(pen='y')

def update():
    
    Eng.nextstep()
    curve.setData(S2.data,S1.data)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)
pg.exec()
