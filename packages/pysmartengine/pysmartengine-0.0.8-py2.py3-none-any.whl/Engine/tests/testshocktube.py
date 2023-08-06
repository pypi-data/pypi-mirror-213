# from matplotlib import pyplot as plt
from Engine import Framework,Pipe,Orifice,Environment,GasProperty,Table


Mix=GasProperty.UDFMix({GasProperty.Air():1.0})
# Mix2=GasProperty.CoolPropSpe({"Air":0.5,"CarbonDioxide":0.5})

# print(Mix2.database)


#创建部件
P2=Pipe.ShockTube1DEuler([0,5e5,1200],[1,1e5,300]).init(Mix,1,0.005) 

S=Framework.Sensor().connect(P2.getport("rho"))
S1=Framework.Sensor().connect(P2.getport("x"))

P2.CFL=0.5

# Framework.tic()
# for i in range(1000):
#     P2.nextstep()
# Framework.toc()
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
win = pg.GraphicsLayoutWidget(show=True)
curve = win.addPlot().plot(pen='y')

def update():
    try:
        if(P2.tnow<1e-3):
            P2.nextstep()
            curve.setData(S1.data,S.data)
        else:
            exit()
    except Exception as e:
        print(e)
        exit()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
pg.exec()
# P2.solve(0.4e-3).open()
# P2.animation("p",0.5e-3)


# 传感器参数
# sensor=P1.getSensor(0.4)

# plt.ion
# for i in range(300):
#     P1.nextstep()
#     # print(sensor.para)
#     plt.scatter(sensor.para["t"],sensor.para["p"])
#     plt.pause(0.1)

# plt.ioff
# plt.show