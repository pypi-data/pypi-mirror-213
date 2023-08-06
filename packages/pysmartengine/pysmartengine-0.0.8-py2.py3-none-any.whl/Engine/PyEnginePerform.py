from Engine import EnginePerform as E
from Engine.Cylinder import CylinderGeometry


def exhaustTemperature(bore, stroke, pme, n, ge, ps, Ts, alpha , etav , strokeNum=4 , l0= 0.495, Hu = 42496):
    """
    bore:缸径
    stroke：冲程
    pme：平均有效压力
    n：转速
    ge：油耗，大概在230左右
    ps：进气压力
    Ts：进气温度
    alpha：过量空气系数
    etav：扫气系数
    """
    return E.exhaustTemperature(bore, stroke, pme, n, ge, ps, Ts, alpha,etav, strokeNum, l0, Hu)


class MVEM(E.MVEM):
    def __init__(self,CylinderGeometry):
        super().__init__(CylinderGeometry)

    def startnewcycle(self,speed):
        super().startnewcycle(speed)


    def setvalvetiming(self,intakeopen=-377, intakeclose=-152, exhaustopen=125, exhaustclose=375):
        super().setvalvetiming(intakeopen, intakeclose, exhaustopen, exhaustclose)

    def compress(self,pimin=1.e5, Timin=313, Tr=413, xr=0, kc=1.38, phic=0.9, ivcpcoeff=1.2):
        super().compress(pimin, Timin, Tr, xr, kc, phic, ivcpcoeff)

    def plot(self):
        pass
