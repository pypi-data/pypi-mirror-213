from Engine import GasProperty as G
from Engine import Injector,Framework,Volume

Eng=Framework.Engine("wp7")

mix=G.UDFMix({G.CoolPropSpecie('IF97::Water'):0.8,G.Air():0.2})

init=G.initstate("init").init(G.UDFMix({G.Air():1.0,G.CoolPropSpecie('IF97::Water'):0.0}),1.e5,300)

I=Injector.Injector(Eng).init(mix,0.1,800)

V=Volume.Volume(Eng).init(init,1)

I.connect(V.getport(0))

S=Framework.Sensor().connect(V.getport("T"))

Eng.init()

# print(Eng.components)
Eng.tstep=0.001

# for i in range(10):
#     Eng.nextstep()

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
