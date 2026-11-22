"""
Modelo de Categoría — tabla 'categoria' en PostgreSQL.

CRUD protegido por JWT.
Cualquier usuario autenticado puede leer; crear/editar/borrar requiere rol admin.
El borrado es lógico: completa deleted_at.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Text
from sqlmodel import SQLModel, Field

from app.modules.usuarios.model import ahora


class Categoria(SQLModel, table=True):
    id:          Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    nombre:      str           = Field(max_length=100, index=True, unique=True)
    descripcion: str           = Field(default="", sa_type=Text)
    created_at:  datetime      = Field(default_factory=ahora, sa_type=DateTime(timezone=True))
    updated_at:  datetime      = Field(
        default_factory=ahora,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": ahora},
    )
    deleted_at:  Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True))


# ─── Esquemas Pydantic ───────────────────────────────────────────────────────

class CategoriaCreate(SQLModel):
    """Datos para crear una categoría."""
    nombre:      str = Field(min_length=1, max_length=100)
    descripcion: str = Field(default="")


class CategoriaUpdate(SQLModel):
    """Datos para actualizar (parcial — todos opcionales)."""
    nombre:      str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None)


class CategoriaPublic(SQLModel):
    """Vista pública de la categoría."""
    id:          int
    nombre:      str
    descripcion: str