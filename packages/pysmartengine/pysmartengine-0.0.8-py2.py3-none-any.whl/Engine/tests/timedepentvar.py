import Framework,Pipe,Orifice,Environment,GasProperty,Table
import matplotlib.pyplot as plt

TT=Table.ArrayTable(2,0).init("test/data/1400pre.csv");

Eng=Framework.Engine("WP7")
spe=GasProperty.UDFMix({GasProperty.Air():1.0})

#创建所有参考
inits=GasProperty.initstate("init").init(spe,1.e5,300)

E=Environment.Env(Eng).init(inits)

S=Framework.Sensor().connect(E.getport("p"))

E.addtimedependentpara("p",TT)

Eng.tstep=10

xx=[]
yy=[]

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

# plt.ion()
# for i in range(1000):
#     Eng.nextstep()
#     plt.scatter(Eng.tnow,E.paratable["p"])
#     plt.pause(0.1)

