from Engine import Table,Turbocharger,GasProperty as G
import matplotlib.pyplot as plt,numpy as np
fig = plt.figure()
ax = fig.add_subplot(projection="3d")


T=Table.ArrayTable(2,0)

# xx=np.linspace(200,1000,100);yy=np.linspace(1,18,100)
# x,y=np.meshgrid(xx,yy)
# zz=np.zeros([len(xx),len(yy)]);zz2=np.zeros([len(xx),len(yy)])
# for i in range(len(xx)):
#     for j in range(len(yy)):
#         k=G.k_Justi(xx[i],3.61)
#         zz[i][j]=G.cp_Justi(xx[i],3.61)*xx[i]*0.8*14.72/1.e3*(1-pow(1/yy[j],(k-1)/k))
#         zz2[i][j]=4000


k=G.k_Justi(1200,3.61)
zz=G.cp_Justi(1200,3.61)*1200*0.8*14.72/1.e3*(1-pow(1/3,(k-1)/k))
print(zz)

np.savetxt("test.csv",yy,delimiter=',',fmt='%f')

    # yy.append(G.cp_Justi(i,3.61)*i*0.6*14.72/1.e3)
    # T.append([i,G.cp_Justi(i,3.61)*i*0.9*14.72/1.e3])
ax.plot_surface(x,y,zz)
ax.plot_surface(x,y,zz2)
# T.open()
plt.show()

# plt.plot(xx,yy)
# plt.show()

# Turbocharger.setturmap("Turbine_35.csv",5.e5,300,1)