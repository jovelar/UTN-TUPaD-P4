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
    def __init__(self,nombre:str,descripcion:str=""):
        
        #se valida que la categoria tenga nombre
        if not nombre:
            raise ValueError("La categoria obligatoriamente debe tener un nombre")
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
        self._es_principal=valor
    
    

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
            
            #.2f formatea a 2 decimales
            publicado=f"${self._precio_base:.2f} / {self._unidad_venta.simbolo}"
        else:
            publicado=f"${self._precio_base:.2f}"
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
                    vinculo._marcar_principal(False)

        self._clasificaciones.append(ProductoCategoria(categoria,es_principal))

    def categorias(self)->tuple[ProductoCategoria,...]:
        return tuple(self._clasificaciones)



class ProductoSimple(Producto):
    def __init__(self,
                 nombre:str, precio_base:float, 
                 stock_cantidad:float, 
                 habilitado:bool, 
                 categoria:Categoria, 
                 unidad_venta:UnidadMedida|None):
        super().__init__(nombre, precio_base, stock_cantidad, habilitado, categoria, unidad_venta)

    def precio_final(self,cantidad:float)->float:
        precio=0
        
        #En el uml dice que tiene que ser float pero trabaja con entero. y se repeto eso
        #Se usa cantidad != int(cantidad) por que con type o isinstance por que al tener
        #decimal, por mas que sea 0, no lo va a reconocer como entero
        
        if cantidad<1 or cantidad!= int(cantidad):
            raise ValueError("La cantidad debe ser entera y al menos ser igual a 1")
        else:
            precio=self._precio_base*cantidad
    
        return precio

class ProductoPorPeso(Producto):
    def __init__(self, nombre:str,
                 precio_base:float,
                 stock_cantidad:float, habilitado
                 :bool,
                 categoria:self.categorias, 
                 unidad_venta:UnidadMedida):
        super().__init__(nombre, precio_base, stock_cantidad, habilitado, categoria, unidad_venta)

    def precio_final(self, cantidad):
        if cantidad<=0:
            raise ValueError("La cantidad no puede ser menor a  0")
        return round(self._precio_base*cantidad,2)

class ProductoCombo(Producto):
    def __init__(self, nombre,
                 precio_base,
                 stock_cantidad,
                 habilitado,
                 categoria,
                 unidad_venta,
                 componentes: list[Producto],
                 descuento:float):
        
        super().__init__(nombre,
                         precio_base,
                         stock_cantidad,
                         habilitado,
                         categoria,
                         unidad_venta)
        
        #validacion de minimos
        if len(componentes)<2:
            raise ValueError("Minimo 2 productos")
        self._componentes=list(componentes)
        if descuento < 0 or descuento >=1:
            raise ValueError("El descuento debe ser un decimal mayor a 0 y menor a 1")
        self._descuento=descuento
    
    def precio_final(self,cantidad)->float:
        if cantidad<1 or cantidad!= int(cantidad):
            raise ValueError("La cantidad debe ser entera y al menos ser igual a 1")
        subtotal=sum(componente.precio_final(1) for componente in self._componentes)
        return subtotal*(1-self._descuento)*cantidad

    
    #devuelve una copia de la lista de productos
    def componentes(self) -> tuple[Producto,...]:
        return tuple(self._componentes)
        

class Exportable(Protocol):
    def exportar(self)->str:
        ...