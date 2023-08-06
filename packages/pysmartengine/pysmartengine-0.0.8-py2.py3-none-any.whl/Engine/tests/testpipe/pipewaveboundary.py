from Engine import Framework,Pipe,Orifice,Environment,GasProperty,Table

TT=Table.ArrayTable().init("test/data/1400pre.csv")

TT.table[0]+=144

TT.table[0]*=(30*4/1400/720)

# TT.plot()

spe=GasProperty.UDFMix({GasProperty.Air():1.0})

#创建所有参考
inits=GasProperty.initstate("init").init(spe,1.e5,300)

#创建发动机
Eng=Framework.Engine("WP7")

#创建部件
P1=Pipe.PipeRound(Eng).init(inits,80,100,5)

E=Environment.Env(Eng).init(inits).clone(2)

O=Orifice.Orifice(Eng).clone(2)

O[0].connect(E[0].getport(1),P1.getport(1))
O[1].connect(P1.getport(2),E[1].getport(1))

# 声明两个传感器
S1=Framework.Sensor().connect(P1.getport("p"))
S2=Framework.Sensor().connect(P1.getport("x"))

S3=Framework.Sensor().connect(E[0].getport("p"))
E[0].addtimedependentpara("p",TT)

Eng.init()

# for i in range(10):
#     Eng.nextstep()
x=[];y=[];

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
win = pg.GraphicsLayoutWidget(show=True)
curve = win.addPlot().plot(pen='y')
curve2 = win.addPlot().plot(pen='y')

def update():
    Eng.nextstep()
    curve.setData(S2.data,S1.data)

def update2():
    x.append(Eng.tnow)
    y.append(S3.data)
    curve2.setData(x,y)

def up():
    update()
    update2()

timer = QtCore.QTimer()
timer.timeout.connect(up)
timer.start(0)
pg.exec()