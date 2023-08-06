from Engine import Framework,Pipe,Orifice,Environment,GasProperty

spe=GasProperty.UDFMix({GasProperty.Air():1.0})

#创建所有参考
inits=GasProperty.initstate("init").init(spe,1.e5,300)
inits2=GasProperty.initstate("init2").init(spe,5e5,300)
inits3=GasProperty.initstate("init3").init(spe,1.e5,300)

#创建发动机
Eng=Framework.Engine("WP7")

#创建部件
P1=Pipe.PipeRound(Eng).init(inits,80e-3,100,0.5)
E=Environment.Env(Eng).init(inits2)
E2=Environment.Env(Eng).init(inits3)
O=Orifice.Orifice(Eng).clone(2)

#创建连接
O[0].connect(E.getport(1),P1.getport(1))
O[1].connect(P1.getport(2),E2.getport(1))

# 声明两个传感器
S1=Framework.Sensor().connect(P1.getport("p"))
S2=Framework.Sensor().connect(P1.getport("x"))

# print(S.data)
# for i in range(1000):
#     Eng.nextstep()

# print(S.data)
Eng.init()

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
win = pg.GraphicsLayoutWidget(show=True)
curve = win.addPlot().plot(pen='y')

def update():
    if(Eng.tnow<1000.0):
        Eng.nextstep()
        curve.setData(S2.data,S1.data)
    else:
        exit()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
pg.exec()
