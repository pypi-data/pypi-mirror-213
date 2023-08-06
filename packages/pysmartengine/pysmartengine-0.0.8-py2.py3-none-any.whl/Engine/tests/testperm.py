import EnginePerform as E


import Framework,Pipe,Orifice,Environment,GasProperty

print(E.les([1,2,5.1,6.5],[3,4,7,8.2],3))

#创建发动机
# Eng=Framework.Engine("WP7")


#创建所有参考
# inits=GasProperty.initstate("init").init(GasProperty.species(Air=0.7,N2=0.30),p=3.e5)


# print(inits.p)
# print(E.Perf(init=Eng))