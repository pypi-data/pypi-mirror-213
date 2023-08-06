from Engine import  Framework, PyTable,Cylinder,PyTurbocharger




C=PyTurbocharger.CompressorMap()

T=PyTable.ArrayTable().init("data\\CompressorMap2.csv")

C.init(T)

C.show()

C.plot()

# T.writeGTfile("temp.dat")
# T.show()