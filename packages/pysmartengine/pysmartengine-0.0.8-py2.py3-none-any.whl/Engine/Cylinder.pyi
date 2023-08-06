from Engine.Framework import(
    Component,
    Engine,References
)

class Cylinder(Component):
    def __init__(self, engine: Engine) -> None: ...
    
    @property
    def Pressure(self)->None:...

class CylinderGeometry(References):
    def __init__(self) -> None: ...

    def show(self):...


