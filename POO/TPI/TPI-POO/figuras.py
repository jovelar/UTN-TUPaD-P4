from dataclasses import dataclass
from abc import ABC,abstractmethod

class Taller:
    def __init__(self):
        self._poligonos=[]
        
    def recibir(self,poligono):
        self._poligonos.append(Poligono)
    
    def restaurar(self,poligono):
        self._poligonos.remove(poligono)
    
    def inventario(self):
        return tuple(self._poligonos)

@dataclass(frozen=True)
class Etiqueta:
    def __init(self,texto):
        self.texto=texto

#parte 3
class Poligono(ABC):
    def __init__(self):
        self._lados=[]

    @abstractmethod
    def lados_esperados(self) -> int:
        ...

    @abstractmethod
    def perimetro(self)-> float:
        ...

    @abstractmethod
    def lados(self) -> tuple(lados):
        ...

    @abstractmethod
    def exportar(self) ->str:
        ...
