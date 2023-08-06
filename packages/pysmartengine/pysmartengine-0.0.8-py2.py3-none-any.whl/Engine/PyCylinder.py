from Engine.Framework import(
    Component,
    Engine,References
)
from Engine.Table import ArrayTable

class Combustion(References):
    def __init__(self) -> None:...


# 声明C++中的类
class CylinderPressure(References):
    def __init__(self,Cylinder) -> None:...

    def init(self,ArrayTable:ArrayTable):...

    def analyze(self,etac)->None:...






# 重定义类
import numpy as np
from Engine.Cylinder import *
from .Algorithm.FileManipulate import get_pakage_dir
class CylinderGeometryPy(CylinderGeometry):
    def __init__(self, EngineType=None, bore=None, stroke=None, connecting_rod_length=None, compression_ratio=None,
                 number_of_cylinders=1):
        super().__init__(EngineType)

        # 直接由数据库读取
        if EngineType is not None:
            self.EngineType = EngineType
            from pandas import read_excel
            self.excledata=read_excel(get_pakage_dir("Engine") + "\\data\\enginedata.xlsx", index_col="机型")
            data= self.excledata.loc[EngineType]
            bore = data["bore,mm"] * 1.e-3;
            stroke = data["stroke,mm"] * 1.e-3;
            connecting_rod_length = data["connecting rod length,mm"] * 1.e-3;
            compression_ratio = data["compression ratio"];
            number_of_cylinders = data["number of cylinders"]

        self.init(bore,stroke,compression_ratio,connecting_rod_length,number_of_cylinders)
        # self.Cobj=Cylinder.CylinderGeometry(EngineType).init(bore,stroke,compression_ratio,connecting_rod_length)
        self.bore = bore
        self.stroke = stroke
        self.compression_ratio = compression_ratio
        if connecting_rod_length is None:
            print("连杆长度选择提示：")
            print("低速二冲程十字头式:{}~{}".format(3.5 * stroke / 2, 4. * stroke / 2))
            print("中速柴油机:{}~{}".format(3.8 * stroke / 2, 4.6 * stroke / 2))
            print("高速柴油机:{}~{}".format(3.5 * stroke / 2, 4.3 * stroke / 2))
        self.connecting_rod_length = connecting_rod_length
        self.__Lam = self.stroke / 2 / connecting_rod_length  # 曲柄连杆比
        if self.__Lam > 1. / 3.:
            print("请检查连杆长度是否有误，通常该连杆长度L>{}".format(3. * stroke / 2))

        if self.TDCclearanceHeight() < 0:
            raise Exception("TDC clearance height is less than 0!!!Parameters have some problem.")


        # 打印气缸容积参数
        from Engine.Table import ParameterTable
        TT=ParameterTable(0,"Engine: {} cylinder geometry".format(EngineType if EngineType is not None else ""))
        TT.append("bore","mm",self.bore*1.e3)
        TT.append("stroke","mm",self.stroke*1.e3)
        TT.append("connect rod length","mm",self.connecting_rod_length*1.e3)
        TT.append("C/R ratio","/",self.__Lam)
        TT.append("num of cylinder","/",number_of_cylinders)
        TT.append("Volume of single cylinder","cc",1.e6 * self.VH)
        TT.append("Total displacement volume","L",1.e3 * number_of_cylinders * self.VH)
        TT.append("TDC clearance height","mm",1.e3 * self.TDCclearanceHeight())
        self.num_of_cylinders = number_of_cylinders
        TT.show()

    def pim(self):
        """
        根据进气管压力计算缸内进气量
        """

    def powerplot(self,BMEPin=None):
        #首先根据活塞平均速度计算发动机转速
        import pandas as pd
        dropnan=pd.to_numeric(self.excledata["活塞平均速度,m/s"],errors='coerce').dropna().replace(0, np.nan).dropna()
        minspeed=1000
        maxspeed=dropnan.max()*30/self.connecting_rod_length

        if BMEPin is None:
            BMEP=pd.to_numeric(self.excledata["平均有效压力,Mpa"],errors='coerce').dropna().replace(0, np.nan).dropna()
            BMEPin=BMEP.mean()*1e6

        print("BMEP",BMEPin/1.e5,"bar")

        speed=np.linspace(minspeed,maxspeed,1000)
        BMEPlist=[]
        for each in speed:
            BMEPlist.append(self.VH*self.num_of_cylinders*BMEPin/(30.0*4.0/each)/1.e3)

        import matplotlib.pyplot as plt
        plt.plot(speed,BMEPlist)
        plt.xlabel("Speed(r/min)");plt.ylabel("power(kW)")
        plt.show()


        #再根据定平均有效压力计算各个转速下的功率和扭矩

    @staticmethod
    def opendatabase():
        import os
        os.startfile(get_pakage_dir("Engine") + "\\data\\enginedata.xlsx")
        # from pandas import read_excel,options
        # excledata=read_excel(get_pakage_dir("Engine") + "\\data\\enginedata.xlsx")
        # options.display.max_rows = len(excledata)
        # options.display.max_columns = len(excledata)
        # print(excledata["机型"])

    



class SingleWiebePy(SingleWiebe):
    def __init__(self) -> None:
        super().__init__()

    def init(self,SOC, dTCD, m=2, a = 6.908):
        super().init(SOC, dTCD, m, a)

    def plot(self):
        self.updateTable()
        import matplotlib.pyplot as plt
        plt.figure(1, figsize=(10, 5))
        plt.subplot(121)
        plt.plot(self.data.table[0].data, self.data.table[1].data)
        plt.xlabel("Crank angle(°CA)")
        plt.ylabel("Burn Rate (Normalized by Total Fuel Mass)")
        plt.tight_layout()
        plt.grid()

        plt.subplot(122)
        plt.plot(self.data.table[0].data, self.data.table[2].data)
        plt.xlabel("Crank angle(°CA)")
        plt.ylabel("Burned Fuel (Fraction of Total Fuel Mass)")
        plt.tight_layout()

        plt.grid()
        plt.show()



class DoubleWiebePy(DoubleWiebe):
    def __init__(self) -> None:
        super().__init__()

    def init(self,PF, PSOC, PTCD, DTCD, PM = 2, DM = 0.8, DSOCin=np.Inf):
        super().init(PF, PSOC, PTCD, DTCD, PM, DM, DSOCin)

    def plot(self):
        self.updateTable()
        import matplotlib.pyplot as plt
        plt.figure(1, figsize=(10, 5))
        plt.subplot(121)
        plt.plot(self.data.table[0].data, self.data.table[1].data)
        plt.xlabel("Crank angle(°CA)")
        plt.ylabel("Burn Rate (Normalized by Total Fuel Mass)")
        plt.tight_layout()
        plt.grid()

        plt.subplot(122)
        plt.plot(self.data.table[0].data, self.data.table[2].data)
        plt.xlabel("Crank angle(°CA)")
        plt.ylabel("Burned Fuel (Fraction of Total Fuel Mass)")
        plt.tight_layout()

        plt.grid()
        plt.show()


class HeatReleaseDataPy(HeatReleaseData):
    def __init__(self) -> None:
        super().__init__() 

    def init(self,ArrayTable):
        super().init(ArrayTable)

    def normalize(delf):
        super().normalize()

    def plot(self):
        import matplotlib.pyplot as plt
        plt.figure(1, figsize=(10, 5))
        plt.subplot(121)
        plt.plot(self.data.table[0].data, self.data.table[1].data)
        plt.xlabel("Crank angle(°CA)")
        plt.ylabel("Burn Rate (Normalized by Total Fuel Mass)")
        plt.tight_layout()
        plt.grid()

        plt.subplot(122)
        plt.plot(self.data.table[0].data, self.data.table[2].data)
        plt.xlabel("Crank angle(°CA)")
        plt.ylabel("Burned Fuel (Fraction of Total Fuel Mass)")
        plt.tight_layout()

        plt.grid()
        plt.show()

    def SOC(self):
        return super().findSOC()
    
    def EOC(self):
        return super().findEOC()

    def regwithsinglewiebe(self,SOC,TCD,m=2,a = 6.908,plot=True):
        rlt=super().regwithsingle(SOC,TCD,m,a)

        if plot:
            rlt.updateTable()
            import matplotlib.pyplot as plt
            plt.plot(self.data.table[0].data,self.data.table[1].data)

            plt.plot(rlt.data.table[0].data,rlt.data.table[1].data)

            plt.show()

        return rlt
    
    def regwithsinglewiebe(self,plot=True):
        # 找拟合的初值
        import numpy as np
        xx=[];yy=[]
        for i in range(self.data.row):
            xx.append(np.log(self.data.table[0].data[i]-self.SOC()))
            yy.append(np.log(-np.log(1.-self.data.table[2].data[i])))

        TT=ArrayTable(2,0)
        for i in range(len(xx)):
            if (not np.isnan(xx[i]) and not np.isinf(xx[i])) and (not np.isnan(yy[i]) and not np.isinf(yy[i])):
                TT.append([xx[i],yy[i]])

        # # 第一个
        import matplotlib.pyplot as plt
        if plot:plt.plot(TT.table[0].data,TT.table[1].data)

        slope1, intercept1 = np.polyfit(TT.table[0].data, TT.table[1].data, 1)

        y_pred = slope1 * np.array(TT.table[0].data) + intercept1
        
        if plot:plt.plot(TT.table[0].data,y_pred)
        if plot:plt.show()

        m1=slope1-1.0
        A1=np.exp(-intercept1/slope1)

        fip=A1/pow(6.908,-1.0/slope1)

        p=self.regwithsiglefun(self.SOC(),fip,m1)

        wiebe2=SingleWiebePy()
        wiebe2.init(p[0],p[1],p[2])
        wiebe2.updateTable()
        if plot:plt.plot(wiebe2.data.table[0].data,wiebe2.data.table[1].data)
        if plot:plt.plot(self.data.table[0].data,self.data.table[1].data)
        if plot:plt.show()

        return wiebe2


    
    def regwithdoublewiebe(self,plot=True):

        # 找拟合的初值
        import numpy as np
        xx=[];yy=[]
        for i in range(self.data.row):
            xx.append(np.log(self.data.table[0].data[i]-self.SOC()))
            yy.append(np.log(-np.log(1.-self.data.table[2].data[i])))

        TT=ArrayTable(2,0)
        for i in range(len(xx)):
            if (not np.isnan(xx[i]) and not np.isinf(xx[i])) and (not np.isnan(yy[i]) and not np.isinf(yy[i])):
                TT.append([xx[i],yy[i]])


        # 拟合并计算相关系数
        def transientpoint(x0):
            # 第一个
            T1=TT.slice(TT.table[0].data[0],x0[0],0)

            if len(T1.table[0].data)==0:
                corr1=0

            else:
                slope, intercept = np.polyfit(T1.table[0].data, T1.table[1].data, 1)

                y_pred = slope * np.array(T1.table[0].data) + intercept
                # 计算相关系数
                corr_matrix = np.corrcoef(T1.table[1].data, y_pred)
                corr1 = corr_matrix[0, 1]

            #第二个
            T2=TT.slice(x0[0],TT.table[0].data[-1],0)

            if len(T2.table[0].data)==0:
                corr2=0
            else:
                slope, intercept = np.polyfit(T2.table[0].data, T2.table[1].data, 1)

                y_pred = slope * np.array(T2.table[0].data) + intercept
                # 计算相关系数
                corr_matrix = np.corrcoef(T2.table[1].data, y_pred)
                corr2 = corr_matrix[0, 1]

            return (corr1,corr2)
        
        coeff1=[];coeff2=[];value=[]

        def coeff(num=4):
            for i in range(num,TT.row-num):
                c1,c2=transientpoint([TT.table[0].data[i]])
                coeff1.append(c1);coeff2.append(c2);value.append(TT.table[0].data[i])

        coeff();

        # 找两个都大于某一个值的索引
        maxindex=0
        sort_index = sorted(range(len(coeff1)), key=lambda i: coeff1[i])
        sorted_list = [coeff1[i] for i in sort_index]
        for ii in range(len(sorted_list)-1,0,-1):
            sorted_list[ii]<=coeff2[sort_index[ii]]
            maxindex=sort_index[ii]
            break

        # 找两个都大于某一个值的索引
        maxindex2=0
        sort_index = sorted(range(len(coeff2)), key=lambda i: coeff2[i])
        sorted_list = [coeff2[i] for i in sort_index]
        for ii in range(len(sorted_list)-1,0,-1):
            sorted_list[ii]<=coeff1[sort_index[ii]]
            maxindex2=sort_index[ii]
            break


        # 谁的最小值最小则不选谁
        small1=coeff1[maxindex] if coeff1[maxindex]<coeff2[maxindex] else coeff2[maxindex]
        small2=coeff1[maxindex2] if coeff1[maxindex2]<coeff2[maxindex2] else coeff2[maxindex2]

        idex=maxindex if small1>small2 else maxindex2

        # # 第一个
        import matplotlib.pyplot as plt
        if plot:plt.plot(TT.table[0].data,TT.table[1].data)

        x0=value[idex]

        T1=TT.slice(TT.table[0].data[0],x0,0)
        slope1, intercept1 = np.polyfit(T1.table[0].data, T1.table[1].data, 1)

        y_pred = slope1 * np.array(T1.table[0].data) + intercept1
        
        if plot:plt.plot(T1.table[0].data,y_pred)

        T2=TT.slice(x0,TT.table[0].data[-1],0)
        slope2, intercept2 = np.polyfit(T2.table[0].data, T2.table[1].data, 1)

        y_pred = slope2 * np.array(T2.table[0].data) + intercept2

        if plot:plt.plot(T2.table[0].data,y_pred)

        xintersection=-(intercept2-intercept1)/(slope2-slope1);
        yintersection=slope1*xintersection+intercept1;

        if plot:plt.scatter([xintersection],[yintersection])

        SOCd=np.exp(xintersection)+self.SOC();
        alpha=1-np.exp(-np.exp(yintersection))

        m1=slope1-1.0;m2=slope2-1.0;
        A1=np.exp(-intercept1/slope1);A2=np.exp(-intercept2/slope2)

        fip=A1/pow(6.908,-1.0/slope1);fid=A2/pow(6.908,-1.0/slope2);

        # 所有初值都已经找到

        if plot:plt.show()
        if plot:plt.plot(self.data.table[0].data,self.data.table[1].data)

        # 开始回归
        me=self.regwithdoublefun(alpha,self.SOC(),fip,fid,m1,m2,SOCd)

        print("alpha=",me[0])
        print("SOC=",me[1])
        print("TCDp=",me[2])
        print("TCDd=",me[3])
        print("m1=",me[4])
        print("m2=",me[5])
        print("SOCd=",me[6])

        wiebe2=DoubleWiebePy()
        wiebe2.init(me[0],me[1],me[2],me[3],me[4],me[5],me[6])
        wiebe2.updateTable()
        if plot:plt.plot(wiebe2.data.table[0].data,wiebe2.data.table[1].data)
        if plot:plt.show()

        return me

        return wiebe2


    def regwithdoublefun(self,alpha,SOCp,fip,fid,m1,m2,SOCd):
        from scipy.optimize import leastsq
        def error_fun(p):
            w=DoubleWiebePy()
            w.init(p[0],p[1],p[2],p[3],p[4],p[5],p[6])
            rlt=[]
            for i in range(self.data.row):
                rlt.append(self.data.table[1].data[i]-w.DX(self.data.table[0].data[i]))

            return rlt

        p_init = [alpha,SOCp,fip,fid,m1,m2,SOCd]

        # 调用leastsq函数求解
        p_fit, success = leastsq(error_fun, p_init)
        return p_fit
    
    def regwithsiglefun(self,SOCp,fip,m1):
        from scipy.optimize import leastsq
        def error_fun(p):
            w=SingleWiebePy()
            w.init(p[0],p[1],p[2])
            rlt=[]
            for i in range(self.data.row):
                rlt.append(self.data.table[1].data[i]-w.DX(self.data.table[0].data[i]))

            return rlt

        p_init = [SOCp,fip,m1]

        # 调用leastsq函数求解
        p_fit, success = leastsq(error_fun, p_init)
        return p_fit




    




        