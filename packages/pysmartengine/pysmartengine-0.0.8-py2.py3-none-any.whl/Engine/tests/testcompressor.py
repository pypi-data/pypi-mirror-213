from Engine import PyTurbocharger as T
from Engine import PyIntercooler as C

from Engine import Table


print(C.pressuredrop(15,0.1,1.293,0.1))

# 压气机三个压比
pr1=4.7
pr2=3.5
pr3=3.4

pamb=0.025e5;#环境压力

massflowrate=0.1 # kg/s

Table1=Table.ParameterTable(0,"first compressor")

Tamb=237.15-50;

Table1.append("Intake temperature","K",Tamb)

etac1=0.6

Table1.append("compressor eff","K",etac1)


P1=T.PowerCompressor(massflowrate,Tamb,pr1,etac1)
Table1.append("compressore power","kW",P1/1.e3)

T1=T.TAfterCompressor(Tamb,pr1,etac1)

Table1.append("T after compressor","K",T1)

T1dot=C.TafterCool(T1,0.4,273.15+20)

Table1.append("T after intercooler","K",T1dot)

Table1.show()


# 第二级压气机
Table2=Table.ParameterTable(0,"2nd compressor")

etac2=0.6

P2=T.PowerCompressor(massflowrate,T1dot,pr2,etac2)
Table2.append("Power","kW",P2/1.e3)


T2=T.TAfterCompressor(T1dot,pr2,etac2)
Table2.append("T","K",T2)

T2dot=C.TafterCool(T2,0.8,273.15+20)

print("第二级中冷器后温度",T2dot)

Table2.show()


# 第三级压气机
Table3=Table.ParameterTable(0,"3rd compressor")
etac3=0.6

P3=T.PowerCompressor(massflowrate,T2dot,pr3,etac3)
Table3.append("Power","kW",P3/1.e3)
print("第三级压气机功率",P3)

T3=T.TAfterCompressor(T2dot,pr3,etac2)

T3dot=C.TafterCool(T3,0.8,273.15+20)

print("第三级中冷器后温度",T3dot)

Table3.show()

massflowrateexhaust=massflowrate*(1+1./13.3)


# 开始计算涡轮后温度

Tt3=1000

def funTt(Tt):

# Tt1=500# 第一级涡轮前温度
# Tt2=800 #第二级压气机前温度
    AA,TT0,PT1=T.TurbineArea(P1,massflowrateexhaust,0.025e5,Tt[0],0.7)

    AA,Tt1dot,PT2=T.TurbineArea(P2,massflowrateexhaust,PT1,Tt[1],0.7)

    AA,Tt2dot,PT3=T.TurbineArea(P3,massflowrateexhaust,PT2,Tt3,0.7)

    rlt=[Tt1dot-Tt[0],Tt2dot-Tt[1]]
    return rlt

from scipy.optimize import leastsq

# 初始化参数矩阵
p_init = [500, 800]
p_fit, success = leastsq(funTt, p_init)

    

# print(T.TAfterCompressor(318,4,0.9))

# print(T.TAfterCompressor(338,3.1,0.9))