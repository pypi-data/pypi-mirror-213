from Engine import Table,Turbocharger
import matplotlib.pyplot as plt,numpy as np

# TT=Table.ArrayTable(2,0)
# TT.show()

# T.setcompremap("CompressorMap.csv")

# print(T.masscom(70000,1.5))

# print(T.effcom(70000,1.5))

T=Table.ArrayTable().init("CompressorMap_76.csv")
T.show()

map=Turbocharger.Compressor.CompressorMap("compre").init(T)

# print(map.cal(62000,1.3))

# plt.ion
# for i in range():

# m=min(map.keys);mx=max(map.keys)
# plt.figure(figsize=(16,9))
# plt.ion
# plt.subplot(1,2,1)
# for i in map.keys:
#     t=map.getline(i)
#     plt.plot(t.table[1].data,t.table[2].data,"-.")
#     plt.pause(0.1)

print(map.cal2(0.3,2.0))
# print(map.cal2(0.3,2.9))

# for i in map.keys:
#     t=map.getline(i)
#     xx=np.linspace(1,max(t.table[2].data)*1.05)
#     yy=[]
#     for each in xx:
#         yy.append(map.cal(i,each)[0])
#     plt.plot(yy,xx)
#     plt.pause(0.1)

# #小转速外拓
# for i in np.linspace(0.5*min(map.keys),min(map.keys),10) :
#     t=map.getline(i)
#     xx=np.linspace(1,max(t.table[2].data)*1.3)
#     yy=[]
#     for each in xx:
#         yy.append(map.cal(i,each)[0])
#     plt.plot(yy,xx)
#     plt.pause(0.1)

# for i in np.linspace(max(map.keys),1.5*max(map.keys),10) :
#     t=map.getline(i)
#     xx=np.linspace(1,max(t.table[2].data)*1.5)
#     yy=[]
#     for each in xx:
#         yy.append(map.cal(i,each)[0])
#     plt.plot(yy,xx)
#     plt.pause(0.1)

# plt.subplot(1,2,2)
# for i in map.keys:
#     t=map.getline(i)
#     plt.plot(t.table[1].data,t.table[3].data,"-.")
#     plt.pause(0.1)

# for i in map.keys:
#     t=map.getline(i)
#     xx=np.linspace(1,max(t.table[2].data))
#     yy=[];zz=[]
#     for each in xx:
#         zz.append(map.cal(i,each)[0])
#         yy.append(map.cal(i,each)[1])
#     plt.plot(zz,yy)
#     plt.pause(0.1)


# print(map.cal2(0.3,2.9))

# plt.ioff()



# plt.tight_layout()
# plt.show()



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