from abc import ABC,abstractmethod
from dataclasses import dataclass
import copy
from typing import Protocol

@dataclass(frozen=True)
class UnidadMedida():
    nombre:str
    simbolo:str
    tipo:str

class Categoria():
    def __init__(self,nombre:str,descripcion:str|None):
        self._nombre=nombre
        self._descripcion=descripcion

    @property
    def nombre(self)->str:
        return self._nombre
    @property
    def descripcion(self)->str:
        return self._descripcion

class ProductoCategoria():
    def __init__(self,categoria:Categoria,es_principal:bool):
        self._categoria=categoria
        self._es_principal=es_principal

    @property
    def categoria(self) ->Categoria:
        return self._categoria

    @property
    def es_principal(self)->bool:
        return self._es_principal
    
    def _marcar_principal(self,valor:bool)->None:
        self._es_principal=True
    
    

class Producto(ABC):
    def __init__(self,nombre:str,
                 precio_base:float,
                 stock_cantidad:float,
                 habilitado:bool,
                 categoria:Categoria,
                 unidad_venta:UnidadMedida|None):
        if not nombre:
            raise ValueError("Falta el nombre")

        if precio_base<0:
            raise ValueError("El precio no puede ser menor a 0")

        if stock_cantidad <0:
            raise ValueError("El stock no puede ser mernor a 0")
        
        self._nombre=nombre
        self._precio_base=precio_base
        self._stock_cantidad=stock_cantidad
        self._habilitado=habilitado
        self._unidad_venta=unidad_venta
        self._clasificaciones:list[ProductoCategoria]=[]
        self.clasificar_en(categoria,es_principal=True)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property        
    def precio_base(self) ->float:
         return self._precio_base

    @property
    def unidad_venta(self)-> UnidadMedida|None:
        return self._unidad_venta

    @property
    def disponible(self)->bool:
        return (self._habilitado and self._stock_cantidad>0)

    @property
    def precio_publicado(self)->str:
        publicado=""
        if self._unidad_venta is not None:
            publicado=f"{self._precio_base}/{self._unidad_venta.simbolo}"
        else:
            publicado=f"{self._precio_base}"
        return publicado

    @abstractmethod
    def precio_final(self,cantidad:int)->float:
        ...

    def habilitar(self)-> None:
        self._habilitado=True


    def deshabilitar(self)->None:
        self._habilitado=False

    def clasificar_en(self,categoria:Categoria,es_principal:bool=False)->None:
        if not isinstance(categoria,Categoria):
            raise ValueError("la clasificacion no existe")

        for vinculo in self._clasificaciones:
            if vinculo.categoria is categoria:
                raise ValueError(f"el producto ya esta asginado en {categoria.nombre}")

        if es_principal:
            for vinculo in self._clasificaciones:
                if vinculo.es_principal:
                    vinculo.marcar_principal(False)

        self._clasificaciones.append(ProductoCategoria(categoria,es_principal))

    def categorias(self)->tuple[ProductoCategoria,...]:
        return tuple(self._clasificaciones)



class ProductoSimple(Producto):
    def __init__(self, nombre, precio_base, stock_cantidad, habilitado, categoria, unidad_venta):
        super().__init__(nombre, precio_base, stock_cantidad, habilitado, categoria, unidad_venta)

    def precio_final(self,cantidad:float)->float:
        return self._precio_base*cantidad

class ProductoPorPeso(Producto):
    def __init__(self, nombre, precio_base, stock_cantidad, habilitado, categoria, unidad_venta):
        super().__init__(nombre, precio_base, stock_cantidad, habilitado, categoria, unidad_venta)

    def precio_final(self, cantidad):
        return super().precio_final(cantidad)

class ProductoCombo(Producto):
    def __init__(self, nombre, precio_base, stock_cantidad, habilitado, categoria, unidad_venta):
        super().__init__(nombre, precio_base, stock_cantidad, habilitado, categoria, unidad_venta)
        self._componentes=list[Producto]
        self._descuento:float
    
    def precio_final(self,cantidad)->float:
        return (self._precio_base*cantidad)*(1-self._descuento)

class Exportable(Protocol):
    def exportar(self)->str:
        ...