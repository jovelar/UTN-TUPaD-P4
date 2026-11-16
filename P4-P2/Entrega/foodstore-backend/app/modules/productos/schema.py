from datetime import datetime
from decimal import Decimal
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field
from app.modules.unidades_medida.model import UnidadMedidaPublic


class ProductoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=3)]
    descripcion: Optional[str] = None
    precio_base: Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]
    unidad_venta_id: int
    stock_cantidad: Annotated[Decimal, Field(ge=0, max_digits=12, decimal_places=3)] = Decimal("0")
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class CategoriaDeProducto(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    activo: bool
    es_principal: bool


class ProductoPublic(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio_base: float
    stock_cantidad: float
    disponible: bool
    activo: bool
    anulado_at: Optional[datetime] = None
    unidad_venta_id: int
    unidad_venta: UnidadMedidaPublic
    categorias: List[CategoriaDeProducto] = []
    hay_stock: bool


class ProductoCategoriaCreate(BaseModel):
    categoria_id: int
    es_principal: bool = False


class ProductoCategoriaPublic(BaseModel):
    producto_id: int
    categoria_id: int
    es_principal: bool