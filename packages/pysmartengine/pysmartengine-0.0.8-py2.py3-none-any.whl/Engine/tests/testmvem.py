from Engine import EnginePerform
import numpy as np

# print(EnginePerform.exhaustTemperature(108e-3,130e-3,15e5,1500,189,2.e5,300))
EnginePerform.initengine(108e-3,130e-3,17,209.7e-3,6)

for i in np.linspace(1400,5000):

    EnginePerform.MVEMstartnewcycle(i)

    EnginePerform.MVEMcompress(2.e5,300,800,0,1.33,1.0,1)

    EnginePerform.MVEMburn(0.5,0.1,120e-6,1.0)

    EnginePerform.MVEMexpanse(1.33)

    EnginePerform.MVEMgasexchange(2.e5)

    EnginePerform.MVEMendcycle(0.96)

    print("bsfc",EnginePerform.MVEMBSFC())

    print("Tt",EnginePerform.MVEMTt(1.0))

    print("air",EnginePerform.MVEMairflow())

