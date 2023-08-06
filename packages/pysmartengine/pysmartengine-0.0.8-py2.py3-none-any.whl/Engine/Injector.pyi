from Engine.Framework import Connection,Engine


class Fuel:
    def __init__(self) -> None: ...

    @property
    def L0(self)->None:...

class Diesel2(Fuel):
    def __init__(self) -> None: ...


class Injector(Connection):
    def __init__(self, engine: Engine) -> None: ...

    def init(self,Fuel:Fuel,mass:float)->Injector:...