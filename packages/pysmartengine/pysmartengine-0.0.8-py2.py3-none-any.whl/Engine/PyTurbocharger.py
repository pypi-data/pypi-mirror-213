
import Engine.Turbocharger as Tur
from Engine.PyTable import ArrayTable

def Cs(T, pi, gamma=1.33, cp=None):
    """
    计算等熵膨胀后的速度
    """
    if cp is None:
        from Engine.GasProperty import cp_Justi
        cp=cp_Justi(T,2.0)
    return Tur.Cs(T,pi,gamma,cp)


def TAfterCompressor(T0, pik, etak=1, tau=1):
    """
    计算压气机后的温度
    :param T0: 环境温度(K)
    :param pik: 压气机压比
    :param etak: 压气机效率,等于1时为等熵压缩温度
    :param tau: 考虑向外散热的冷却系数，tau=1.04~1.10
    :return:压气机后的温度(K)
    """
    from Engine import GasProperty
    k = GasProperty.k_Justi(T0,237.15)
    result = T0 + T0 * (pow(pik, (k - 1) / k) - 1) / (etak * tau)
    return result


def PowerCompressor(massflowrate,T0,pik,etak=1, tau=1):
    T1=TAfterCompressor(T0, pik, etak,tau)
    print("压气机后温度K",T1)
    from Engine import GasProperty
    cp = GasProperty.cp_Justi(T0,1.e8,237.15)
    return massflowrate*cp*(T1-T0)

#计算涡轮瞬态时间
def TransientTime(Z,speed,fration):
    """
    Z:叶片数
    Speed:转速(r/min)
    fraction:转过的叶片数
    """
    return Tur.TransientTime(Z,speed,fration)

def effturbine(u:float, rho:float=0.5, alpha:float=17,D2:float=0.58,beta:float=43,fi:float=0.96,phi:float=0.80):
    """
    D2:出口轮半径与进口轮子半径之比
    fi=0.2~0.45
    """
    return Tur.effturbine(u, rho, alpha,D2,beta,fi,phi)



class CompressorMap(Tur.Compressor.CompressorMap):
    def __init__(self,mapname:str="default map") -> None:
        super().__init__(mapname)

    def init(self,arr:ArrayTable,p0:float=101325,T0:float=300,maptype:int=1,modeltype:int=0):
        """
        maptype: 0 for corrected, 1 for reduced, default: 1
        modeltype
        """
        self.Table=arr
        return super().init(arr,p0,T0,maptype,modeltype)

    def calculate(self,speed:float,pi:float)->list:
        """
        speed: Rotational speed(r/min)
        pi: Pressure ratio
        """
        return super().cal(speed,pi)
    
    def plot(self,showlegend=True):
        """
        压气机的MAP图生成
        """
        import matplotlib.pyplot as plt
        from numpy import linspace
        fig, ax = plt.subplots(2, 1, figsize=(20, 10))

        ax[1].set_xlim(0,1.2*max(self.Table.table[1].data))

        ## 画出所有线
        for each in self.keys:
            commap=self.getline(each)
            ax[1].plot(commap.table[1].data, commap.table[2].data,
                                                        label="speed=" + str(round(each,2)))
            ax[0].plot(commap.table[1].data, commap.table[3].data,
                                                        label="speed=" + str(round(each,2)),
                                                        )
        
        # surge line,喘振线
        import scipy.interpolate as inte
        xx =[];yy = []
        for each in self.keys:
            commap=self.getline(each)
            xx.append(commap.table[1].data[0])
            yy.append(commap.table[2].data[0])
        maxspeedline=self.getline(max(self.keys))
        xx1=[i for i in xx]
        yy1=[i for i in yy]
        for i in range(1,len(maxspeedline)):
            xx1.append(maxspeedline.table[1].data[i])
            yy1.append(maxspeedline.table[2].data[i])
        self.fsurgeline = inte.interp1d(xx1, yy1, kind=1)
        xx2 = linspace(min(xx), max(xx), 100)
        ax[1].plot(xx2, self.fsurgeline(xx2), "r--",linewidth=4)
        ax[1].annotate('surge line',
                       xy=(xx[(len(xx) // 2)], yy[(len(xx) // 2)]), xycoords='data',
                       xytext=(-50, 30), textcoords='offset points',
                       arrowprops=dict(arrowstyle="->"))

        # choke flow line,堵塞线
        xx =[];yy = []
        for each in self.keys:
            commap=self.getline(each)
            xx.append(commap.table[1].data[-1])
            yy.append(commap.table[2].data[-1])
        self.fchoke = inte.interp1d(xx, yy, kind=1)
        xx3 = linspace(min(xx), max(xx), 100)
        ax[1].plot(xx3, self.fchoke(xx3), "r--",linewidth=4)
        ax[1].annotate('choke flow line',
                       xy=(xx[(len(xx) // 2)], yy[(len(xx) // 2)]), xycoords='data',
                       xytext=(-10, -40), textcoords='offset points',
                       arrowprops=dict(arrowstyle="->"))


        rows=35
        col=30
        # GRP等效率线插值
        x=linspace(min(self.Table.table[1].data),max(self.Table.table[1].data),col)
        from numpy import array,append,zeros
        lines=linspace(min(self.Table.table[3].data),max(self.Table.table[3].data),10)
        # print(array([x]*10).ravel())
        xx=array([x]*rows)
        # print(xx)
        yy=array([])
        for each in x:
            yy=append(yy,linspace(0,self.fsurgeline(each),rows))
        yy.resize(col,rows)
        yy=yy.transpose()
        print(xx.shape)
        print(yy.shape)

        # 画效率线
        self.Table.GPR([xx[1][1],yy[1][1]],[1,2],3, trained=False)
        z=zeros([rows,col])
        for i in range(rows):
            for j in range(col):
                z[i][j] = self.Table.GPR([xx[i][j], yy[i][j]], [1, 2], 3, trained=True)
        contour=ax[1].contour(xx,yy,z,lines,colors='k')
        ax[1].clabel(contour,fontsize=10,colors=('k','r'))

        # 删除图例
        if showlegend:
            plt.legend(loc='best')
        else:
            ax[0].get_legend().remove()
            ax[1].get_legend().remove()

        plt.tight_layout()
        plt.show()


def flowUnitArea(P1, T1=300, R1=287.15, K1=1.4, P2=None, T2=300 , R2=287.15 , K2=1.4):
    from Engine import Valve
    return Valve.flowUnitArea(P1, T1, R1, K1, P2, T2, R2, K2)

def flowUnitAreaErik(P1, T1=300, R1=287.15, K1=1.4, P2=None, T2=300 , R2=287.15 , K2=1.4):
    from Engine import Valve
    return Valve.flowUnitAreaErik(P1, T1, R1, K1, P2, T2, R2, K2)


def TAfterTurbine(Tt, pit, etat=1):
    """
    计算涡轮后温度
    \[{\eta _T} = \frac{{1 - {{\left( {\frac{{{p_0}}}{{{p_T}}}} \right)}^{\frac{{\gamma  - 1}}{\gamma }}}}}{{1 - \frac{{{T_0}}}{{{T_T}}}}}\]
    :param Tt: 涡轮前温度,K
    :param pit: 涡轮膨胀比
    :param etat: 涡轮等熵效率
    :return: 涡轮后温度
    """
    from Engine import GasProperty
    k = GasProperty.k_Justi(Tt,1.0)
    return Tt * (1 - etat * (1 - pow(pit, -(k - 1.0) / k)))

def TurbineArea(power,massflow,pafter,Tbefore,eta):
    """
    根据压气机的需求功率以及流量求膨胀比和流通面积
    power: 压气机功率需求
    massflow: 涡轮流量
    pafter: 涡轮后压力
    Tbefore: 涡轮前温度
    eta: 涡轮效率
    """
    # 根据压气机的需求功率以及流量求膨胀比和流通面积
    import numpy as np
    from scipy.optimize import least_squares
    #求膨胀比
    Pt0=2.e5
    from Engine import GasProperty
    def fun(pt):
        T1=TAfterTurbine(Tbefore,pt/pafter,eta)#涡后温度
        cp=GasProperty.cp_Justi(Tbefore,1.,237.15)
        return massflow*cp*(Tbefore-T1)-power
    
    x0 = np.array([3.*pafter])
    res = least_squares(fun, x0)

    # while abs(fun(Pt0))>1.e-5:
    #     Pt0=Pt0-fun(Pt0)/((fun(Pt0+0.1*Pt0)-fun(Pt0-0.1*Pt0))/(0.02*Pt0))

    Pt0=res.x[0]

    print("涡轮前压力bar",Pt0/1.e5)

    AA=massflow/flowUnitArea(Pt0,Tbefore,GasProperty.Rg(1),1.3,pafter)
    #求流通面积
    print("涡轮当流通面积m^2",AA)

    print("当量直径,mm",(AA/(3.1415/4.0))**0.5*1.e3)

    print("涡轮流量",AA*flowUnitArea(Pt0,Tbefore,GasProperty.Rg(1),1.3,pafter))
    
    T1=TAfterTurbine(Tbefore,Pt0/pafter,eta)#涡后温度
    cp=GasProperty.cp_Justi(Tbefore,1.,237.15)

    print("涡轮功率kW",AA*flowUnitArea(Pt0,Tbefore,GasProperty.Rg(1),1.3,pafter)*cp*(Tbefore-T1))

    return (AA,Pt0,TAfterTurbine(Tbefore,Pt0/pafter,eta))
    

