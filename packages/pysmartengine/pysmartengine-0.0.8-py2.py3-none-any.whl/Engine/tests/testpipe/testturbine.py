import Table,Turbocharger
import matplotlib.pyplot as plt,numpy as np

# TT=Table.ArrayTable(2,0)
# TT.show()

# T.setcompremap("CompressorMap.csv")

# print(T.masscom(70000,1.5))

# print(T.effcom(70000,1.5))

T=Table.ArrayTable().init("test//data//turbinemap1.csv")

map=Turbocharger.Turbine.TurbineMap("compre1").init(T,1e5,300,1)

# print(map.cal(62000,1.3))

# plt.ion
# for i in range():

m=min(map.keys);mx=max(map.keys)

print(map.keys)

spe=map.keys

plt.ion
for i in spe:
    t=map.getline(i)
    plt.plot(t.table[2].data,t.table[3].data)
    plt.pause(0.1)

for i in spe:
    xx=np.linspace(1,4)
    yy=[]
    for j in xx:
        yy.append(map.cal(i,j)[1])
    plt.plot(xx,yy,'-.')
    plt.pause(0.1)

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