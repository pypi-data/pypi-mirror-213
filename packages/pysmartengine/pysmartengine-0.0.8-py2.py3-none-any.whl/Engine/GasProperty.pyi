from typing import overload
from Framework import(
    References
)

class specie:
    @overload
    def __init__(self,speciename:str) -> None: ...

    @overload
    def __init__(self)-> None: ...

    def cp(T:float,p:float)->float:...
    def cv(T:float,p:float)->float:...
    def k(T:float,p:float)->float:...
    def Rg()->float:...

class species(specie):
    def __init__(self,spedic:dict) -> None: ...

    @property
    def data(self)->dict:...

class UDFMix(specie):
    """
    User defined species
    """
    def __init__(self,mix:dict)->None:...


class Air(specie):
    """
    Air single specie

    """
    def __init__()->None:...


class DieselBurned(specie):
    def __init__()->None:...


class initstate(References):
    """
    Specify init state(Gas species, pressure and temperature) for all components
    """
    def __init__(self,name:str) -> None: ...

    def init(self,spe:species,pressure:float,T:float)->initstate:...

class CoolPropSpe(species):
    def __init__(self, spedic: dict) -> None: ...

    @property
    def database(self)->dict:...

