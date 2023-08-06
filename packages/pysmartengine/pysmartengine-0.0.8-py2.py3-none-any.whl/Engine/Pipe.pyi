from typing import overload
from Framework import *

from GasProperty import (
    initstate
)

class ShockTube1D:
    def __init__(self) -> None: ...


class ShockTube1DEuler(ShockTube1D):
    def __init__(self,left:list,right:list) -> None: ...

    def init(self,species,range:float,dislen:float)->ShockTube1DEuler:...

    def getport(self, paraname:str) -> SensorPort: ...



class Pipe(Component):
    def __init__(self, engine: Engine) -> None: ...

    @overload
    def getport(self, paraname:str) -> SensorPort: ...

    @overload
    def getport(self,portid:int)->FlowPort:...

class PipeRound(Pipe):
    def __init__(self, engine: Engine) -> None: ...
    def init(self,initstateobj:initstate,diameter_in:float,length:float,discretization_length:float,diametet_out:float=None)->PipeRound:...

class EndFlowCap(Pipe):
    def __init__(self, engine: Engine) -> None: ...

    @overload
    def getport(self,portid:int)->FlowPort:...

