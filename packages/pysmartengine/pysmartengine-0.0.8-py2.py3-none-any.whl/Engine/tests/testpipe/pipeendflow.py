# 本算例为一段开口库一端闭口的管道
# 仍然有问题，稳态结果不对

from Engine import Framework,Pipe,Orifice,Environment,GasProperty

#创建发动机
Eng=Framework.Engine("WP7")

spe=GasProperty.UDFMix({GasProperty.Air():1.0})
# spe=GasProperty.CoolPropSpe({"Air":0.5,"CarbonDioxide":0.5})

#创建所有参考
inits=GasProperty.initstate("init").init(spe,1e5,300)

inits2=GasProperty.initstate("init2").init(spe,5e5,300)

# 创建部件
P1=Pipe.PipeRound(Eng).init(inits,30e-3,100e-3,10e-3)
end=Pipe.EndFlowCap(Eng)
E=Environment.Env(Eng).init(inits2)
O=Orifice.Orifice(Eng).clone(2)

#创建连接
O[0].connect(E.getport(1),P1.getport(1))
O[1].connect(P1.getport(2),end.getport(1))

# 声明两个传感器
S1=Framework.Sensor().connect(P1.getport("p"))
S2=Framework.Sensor().connect(P1.getport("x"))

Eng.CFL=0.7
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