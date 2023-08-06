from Framework import(
    Component,
    Engine
)

from GasProperty import(
    initstate
)

class Volume(Component):
    def __init__(self, engine: Engine) -> None: ...

    def init(self,initobj:initstate,Vol:float)->Volume:...

    
