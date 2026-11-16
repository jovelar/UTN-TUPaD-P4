from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


if TYPE_CHECKING:
    from app.modules.productos.model import Producto


class TipoUnidadMedida(str,Enum):
    peso='peso'
    volumen='volumen'
    contable='contable'


class UnidadMedida(SQLModel, table=True):
    __tablename__ = "unidad_medida"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    simbolo: str = Field(unique=True)
    tipo: TipoUnidadMedida

    productos: List["Producto"] = Relationship(back_populates="unidad_venta")


class UnidadMedidaPublic(SQLModel):
    id: int
    nombre: str
    simbolo: str
    tipo: TipoUnidadMedida