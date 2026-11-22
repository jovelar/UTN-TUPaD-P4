"""
Modelo de Usuario — tablas 'usuario', 'rol' y 'usuariorol' en PostgreSQL.

Campos clave para seguridad:
  - password_hash: hash bcrypt (nunca texto plano).
  - roles: filas de UsuarioRol, usadas por require_role() para RBAC.
  - deleted_at: permite desactivar cuentas sin eliminarlas.
"""

from datetime import datetime, timezone
from typing import Optional
from pydantic import EmailStr
from sqlalchemy import BigInteger, CHAR, DateTime, Text
from sqlmodel import SQLModel, Field


def ahora() -> datetime:
    return datetime.now(timezone.utc)


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    nombre: str = Field(max_length=80)
    apellido: str = Field(max_length=80)
    email: str = Field(max_length=254, unique=True, index=True)
    celular: Optional[str] = Field(default=None, max_length=20)
    password_hash: str = Field(sa_type=CHAR(60))
    created_at: datetime = Field(default_factory=ahora, sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(
        default_factory=ahora,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": ahora},
    )
    deleted_at: Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True))


class Rol(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    nombre: str = Field(max_length=50, unique=True)
    descripcion: Optional[str] = Field(default=None, sa_type=Text)


class UsuarioRol(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True, sa_type=BigInteger)
    rol_id: int = Field(foreign_key="rol.id", primary_key=True, sa_type=BigInteger)
    asignado_por_id: Optional[int] = Field(default=None, foreign_key="usuario.id", sa_type=BigInteger)
    expires_at: Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True))
    created_at: datetime = Field(default_factory=ahora, sa_type=DateTime(timezone=True))


# ─── Esquemas Pydantic (sin table=True) ──────────────────────────────────────

class UserCreate(SQLModel):
    """Datos requeridos para registrar un usuario."""
    nombre:   str           = Field(min_length=1, max_length=80)
    apellido: str           = Field(min_length=1, max_length=80)
    email:    EmailStr      = Field(max_length=254)
    celular:  Optional[str] = Field(default=None, max_length=20)
    password: str           = Field(min_length=8, max_length=72)   # bcrypt usa hasta 72 bytes


class UserPublic(SQLModel):
    """Vista pública del usuario — excluye password_hash."""
    id:       int
    nombre:   str
    apellido: str
    email:    str
    celular:  Optional[str] = None
    roles:    list[str]     = []
    activo:   bool


class Token(SQLModel):
    """Respuesta del endpoint /token."""
    access_token: str
    token_type:   str = "bearer"
    expires_in:   int  # segundos hasta expiración