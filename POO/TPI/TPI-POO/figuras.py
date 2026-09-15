from dataclasses import dataclass
from abc import ABC,abstractmethod
from typing import Protocol
from libreria_externa import *



class Taller:
    def __init__(self):
        self._poligonos=[]
        
    def recibir(self,poligono):
        self._poligonos.append(poligono)
    
    def restaurar(self,poligono):
        self._poligonos.remove(poligono)
    
    def inventario(self):
        return tuple(self._poligonos)

@dataclass(frozen=True)
class Etiqueta:
    texto:str

class Exportable(Protocol):
    def exportar(self) -> str:
        ...

#Punto 4.2
def exportar_todo(items: list[Exportable]) -> list[str]:
    return [item.exportar() for item in items]


class Figura(ABC):
    def __init__(self, nombre, color):
        self._nombre = nombre
        self._color = color
#        self._construida = True   # marca de que Figura.__init__ realmente corrió
        
    #Se eliminaron getters y setters innecesarios, uso de anotacion property para area
    @abstractmethod
    def area(self)->float:
        ...


class Lado:
    def __init__(self, longitud):
        if longitud <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = longitud
        self.etiqueta = None
        
    @property
    def longitud(self):
        return self._longitud
        
class Poligono(Figura,ABC):
    catalogo = []
    def __init__(self, nombre, color, lados=None, observaciones=None):
        #Uso de super
        super().__init__(nombre,color)
        #se realiza una copia defensiva para desvincular
        self._lados = list(lados) if lados is not None else []
        
        #validacion de los lados
        if len(self._lados) != self.lados_esperados():
            raise ValueError(f"{type(self).__name__} espera {self.lados_esperados()} lados, recibió {len(self._lados)}")
        self._observaciones = observaciones if observaciones is not None else []
        Poligono.catalogo.append(self)
    
    @abstractmethod
    def lados_esperados(self):
        ...
    def exportar(self) -> str:
        return f"{type(self).__name__}[{self._nombre}, {len(self._lados)} lados]"

    # >>> bucle acumulador manual en vez de comprehension <<<
    def perimetro(self):
        return sum(l.longitud for l in self._lados)


    def agregar_observacion(self, texto):
        self._observaciones.append(texto)


    def getLados(self):
        #devuelve una copia
        return list(self._lados)
    
class Pentagono(Poligono):
    def __init__(self, nombre, color, lados=None, observaciones=None) ->None:
        super().__init__(nombre,color,lados,observaciones)
    
    def lados_esperados(self) -> int:
        return 5

class Hexagono(Poligono):
    def __init__(self, nombre, color, lados=None, observaciones=None) -> None:
        super().__init__(nombre,color,lados,observaciones)
    
    def lados_esperados(self) -> int:
        return 6
    
class Cuadrado(Poligono):
    def __init__(self, nombre="cuadrado", color="negro", lados=None):
        super().__init__(nombre, color, lados if lados is not None else [])
    #Se agragaron constructores alternativos
    @classmethod
    def desde_lista_lados(cls, lista_lados, nombre="cuadrado", color="negro"):
        return cls(nombre, color, lista_lados)


    def lados_esperados(self):
        return 4

class Triangulo(Poligono):
    def __init__(self, nombre="triángulo", color="negro", lados=None):
        super().__init__(nombre, color, lados if lados is not None else [])

    @classmethod
    def desde_lista_lados(cls, lista_lados, nombre="triángulo", color="negro"):
        return cls(nombre, color, lista_lados)
    
    
    def lados_esperados(self):
        return 3



