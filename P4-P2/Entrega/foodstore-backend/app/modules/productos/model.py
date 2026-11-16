from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.categorias.model import Categoria
    from app.modules.unidades_medida.model import UnidadMedida


class ProductoCategoria(SQLModel, table=True):
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)
    es_principal: bool = Field(default=False)


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    unidad_venta_id: int = Field(foreign_key="unidad_medida.id")
    nombre: str
    descripcion: Optional[str] = None
    precio_base: Decimal = Field(max_digits=10, decimal_places=2)
    stock_cantidad: Decimal = Field(default=0, max_digits=12, decimal_places=3)
    disponible: bool = Field(default=True)
    activo: bool = Field(default=True)
    anulado_at: Optional[datetime] = None
    unidad_venta: "UnidadMedida" = Relationship(back_populates="productos")
    categorias: List["Categoria"] = Relationship(back_populates="productos", link_model=ProductoCategoria)