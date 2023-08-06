from Framework import(
    Component,
    Engine
)

from GasProperty import(
    initstate
)

class Env(Component):
    def __init__(self, engine: Engine) -> None: ...

    def init(self,initstate:initstate)->Env:...