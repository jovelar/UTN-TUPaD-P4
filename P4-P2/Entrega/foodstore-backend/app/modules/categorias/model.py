from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.modules.productos.model import ProductoCategoria

if TYPE_CHECKING:
    from app.modules.productos.model import Producto


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = Field(default=True)
    anulado_at: Optional[datetime] = None
    productos: List["Producto"] = Relationship(back_populates="categorias", link_model=ProductoCategoria)