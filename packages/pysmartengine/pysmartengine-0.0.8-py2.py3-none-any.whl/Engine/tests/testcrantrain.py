import Framework,Table

import CrankTrain,Cylinder,Environment,Valve

#创建部件

eng=Framework.Engine("WP7")

C=Cylinder.Cylinder(eng).clone(6)
# print(C)

V=Environment.Env(eng).clone(2)

Val=Valve.Valve(eng).clone(6)

Val2=Valve.Valve(eng).clone(6)

Geo=Cylinder.CylinderGeometry("Geo").init(100e-3,120e-3,17,200e-3)

Cran=CrankTrain.CrankTrain(eng)

#创建连接关系
for i in range(6):
    Val[i].connect(V[0].getport(),C[i].getport())

for i in range(6):
    Val2[i].connect(C[i].getport(2),V[1].getport())


# print(C[5].paratable)

print(eng.components["Valve12"].gettype())
# print(eng.com)
# print(C[0].getport(1))



# C1=Cylinder.Cylinder(eng)

# C2=Cylinder.Cylinder(eng)

# C3=Cylinder.Cylinder(eng)

# C4=Cylinder.Cylinder(eng)

# C5=Cylinder.Cylinder(eng)

# C6=Cylinder.Cylinder(eng)
# print(C6.Fi)



# Cran.init(2000,-110,Geo,[C1,C2,C3,C4,C5,C6],[0,120,120,120,120,120])

# Cran.init(2000,-110,Geo,C,[0,120,120,120,120,120])

# print(C[5].gettype())

# print(type(C[5].paratable))