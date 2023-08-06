import Framework,Pipe,Orifice,Environment,GasProperty

M=GasProperty.CoolPropSpe({"Air":1.0})

Framework.tic()

for i in range(1000):
    M.cp(300,1.e5)

    # print(M.cv(300,1.e5))

    # print(M.k(300,1.e5))

    # print(M.Rg())

Framework.toc()