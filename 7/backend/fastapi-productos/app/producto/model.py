from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, Integer, ForeignKey, JSON
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY

if TYPE_CHECKING:
    from app.categoria.model import Categoria


class ProductoCategoria(SQLModel, table=True):
    producto_id: int = Field(
        sa_column=Column(Integer, ForeignKey("producto.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    )
    categoria_id: int = Field(
        sa_column=Column(Integer, ForeignKey("categoria.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    )


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    precio_base: float
    imagenes_url: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    disponible: bool = True
    categorias: List["Categoria"] = Relationship(back_populates="productos", link_model=ProductoCategoria)