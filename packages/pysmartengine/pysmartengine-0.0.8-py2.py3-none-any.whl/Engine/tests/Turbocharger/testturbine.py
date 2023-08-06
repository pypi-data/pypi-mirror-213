from Engine import Table,Turbocharger
import matplotlib.pyplot as plt,numpy as np

# Turbocharger.setturmap("Turbine_35.csv")

# TT=Table.ArrayTable(2,0)
# TT.show()

# T.setcompremap("CompressorMap.csv")

# print(T.masscom(70000,1.5))

# print(T.effcom(70000,1.5))

T=Table.ArrayTable().init("Turbine_hr40.csv")

map=Turbocharger.Turbine.TurbineMap("turbine1").init(T,1e5,500,1)



# print(map.cal(62000,1.3))

# plt.ion
# for i in range():

m=min(map.keys);mx=max(map.keys)

print(map.keys)

# spe=map.keys

# plt.ion
# plt.subplot(1,2,1)
for i in map.keys:
    t=map.getline(i)
    t.write2file("speed"+str(i)+".csv")
    plt.plot(t.table[4].data,t.table[3].data,"--")
    plt.pause(0.1)

data=Table.ArrayTable().init("data.csv")

T2=Table.ArrayTable(2,0)
# data.plot(1)
print(len(data))
xx=[];yy=[];
for i in range(len(data)):
    T2.append([map.bsr(data.table[5].data[i]/np.sqrt(data.table[7].data[i]),data.table[3].data[i]/data.table[1].data[i]),map.cal(data.table[5].data[i]/np.sqrt(data.table[7].data[i]),data.table[3].data[i]/data.table[1].data[i])[1]])
    xx.append(map.bsr(data.table[5].data[i]/np.sqrt(data.table[7].data[i]),data.table[3].data[i]/data.table[1].data[i]))
    yy.append(map.cal(data.table[5].data[i]/np.sqrt(data.table[7].data[i]),data.table[3].data[i]/data.table[1].data[i])[1])

# T2.open()
# print(xx)

plt.plot(xx,yy,linewidth=2.5)

# 将膨胀比定在1.1左右，计算涡轮的速比随转速的变化
# plt.scatter(map.bsr(30000/np.sqrt(800),1.1),map.cal(30000/np.sqrt(800),1.1)[1])
# plt.scatter(map.bsr(40000/np.sqrt(800),1.1),map.cal(40000/np.sqrt(800),1.1)[1])
# plt.scatter(map.bsr(50000/np.sqrt(800),1.1),map.cal(50000/np.sqrt(800),1.1)[1])
plt.scatter(map.bsr(60000/np.sqrt(800),1.1),map.cal(60000/np.sqrt(800),1.1)[1])
plt.pause(0.1)
plt.ioff()
plt.show()
# for i in spe:
#     xx=np.linspace(1,4)
#     yy=[]
#     for j in xx:
#         yy.append(map.cal(i,j)[0])
#     plt.plot(xx,yy,'-.')
#     plt.pause(0.1)

# plt.subplot(1,2,2)
# for i in spe:
#     t=map.getline(i)
#     plt.plot(t.table[2].data,t.table[3].data)
#     plt.pause(0.1)

# for i in spe:
#     xx=np.linspace(1,4)
#     yy=[]
#     for j in xx:
#         yy.append(map.cal(i,j)[1])
#     plt.plot(xx,yy,'-.')
#     plt.pause(0.1)

# print(map.bsr)

# for i in spe:
#     t=map.getline(i)
#     plt.plot(t.table[4].data,t.table[3].data)
#     plt.pause(0.1)

# xx=np.linspace(min(map.bsr),max(map.bsr),1000)
# yy=[]
# for i in np.linspace(min(map.bsr),max(map.bsr),1000):
#     yy.append(map.bsreff(i))

# plt.plot(xx,yy)
# plt.pause(0.1)

plt.ioff()
plt.show()




# for i in np.linspace(1,8,50):
#     [mass,eff]=map.cal(132000,i)
#     plt.scatter(mass,eff)
#     plt.pause(0.1)

# for i in np.linspace(1,5,50):
#     [mass,eff]=map.cal(130485,i)
#     plt.scatter(mass,eff)
#     plt.pause(0.1)

# plt.ioff()
# plt.show()

# print(map.keys)

# map.getspeedmap(69337.0).show()

# map.plot()
# map.show()
# map.getspeedmap(120000).show()
# map.show()
# print(map.data)
# map.data[4].plot(2,1)
# map.show()

# T.plot(1,2)