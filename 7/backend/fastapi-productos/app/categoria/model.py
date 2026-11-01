from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.producto.model import ProductoCategoria

if TYPE_CHECKING:
    from app.producto.model import Producto


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    productos: List["Producto"] = Relationship(back_populates="categorias", link_model=ProductoCategoria)