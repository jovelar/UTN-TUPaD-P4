"""
Modelo de Producto — tablas 'producto' y 'productocategoria' en PostgreSQL.

CRUD protegido por JWT.
Cualquier usuario autenticado puede leer; crear/editar/borrar requiere rol admin.
El borrado de Producto es lógico (deleted_at); quitar una categoría borra la fila de enlace.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Numeric, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import SQLModel, Field

from app.modules.usuarios.model import ahora


class ProductoCategoria(SQLModel, table=True):
    producto_id:  int      = Field(foreign_key="producto.id", primary_key=True, sa_type=BigInteger)
    categoria_id: int      = Field(foreign_key="categoria.id", primary_key=True, sa_type=BigInteger)
    es_principal: bool     = Field(default=False)
    created_at:   datetime = Field(default_factory=ahora, sa_type=DateTime(timezone=True))


class Producto(SQLModel, table=True):
    __table_args__ = (CheckConstraint("precio_base >= 0", name="ck_producto_precio_base"),)

    id:           Optional[int]       = Field(default=None, primary_key=True, sa_type=BigInteger)
    nombre:       str                 = Field(max_length=150)
    descripcion:  Optional[str]       = Field(default=None, sa_type=Text)
    precio_base:  Decimal             = Field(sa_type=Numeric(10, 2))
    imagenes_url: Optional[list[str]] = Field(default_factory=list, sa_type=ARRAY(Text))
    disponible:   bool                = Field(default=True)
    created_at:   datetime            = Field(default_factory=ahora, sa_type=DateTime(timezone=True))
    updated_at:   datetime            = Field(
        default_factory=ahora,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": ahora},
    )
    deleted_at:   Optional[datetime]  = Field(default=None, sa_type=DateTime(timezone=True))


# ─── Esquemas Pydantic ───────────────────────────────────────────────────────

class ProductoCreate(SQLModel):
    """Datos para crear un producto."""
    nombre:       str           = Field(min_length=1, max_length=150)
    descripcion:  Optional[str] = None
    precio_base:  Decimal       = Field(ge=0, max_digits=10, decimal_places=2)
    imagenes_url: list[str]     = []
    disponible:   bool          = True


class ProductoUpdate(SQLModel):
    """Datos para actualizar (parcial — todos opcionales)."""
    nombre:       str | None       = Field(default=None, min_length=1, max_length=150)
    descripcion:  str | None       = None
    precio_base:  Decimal | None   = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    imagenes_url: list[str] | None = None
    disponible:   bool | None      = None


class ProductoCategoriaCreate(SQLModel):
    """Datos para asignar una categoría a un producto."""
    categoria_id: int  = Field(gt=0)
    es_principal: bool = False


class CategoriaAsignada(SQLModel):
    """Categoría de un producto, con su indicador es_principal."""
    id:           int
    nombre:       str
    es_principal: bool


class ProductoPublic(SQLModel):
    """Vista pública del producto, con sus categorías."""
    id:           int
    nombre:       str
    descripcion:  Optional[str]
    precio_base:  float
    imagenes_url: list[str]
    disponible:   bool
    categorias:   list[CategoriaAsignada] = []