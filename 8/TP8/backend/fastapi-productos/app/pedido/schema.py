from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

EstadoPedido = Literal["PENDIENTE", "CONFIRMADO", "ENTREGADO", "CANCELADO"]


class DetallePedidoCreate(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(ge=1)


class PedidoCreate(BaseModel):
    detalles: List[DetallePedidoCreate] = Field(min_length=1)

    @field_validator("detalles")
    @classmethod
    def sin_productos_repetidos(cls, detalles: List[DetallePedidoCreate]):
        ids = [d.producto_id for d in detalles]
        if len(ids) != len(set(ids)):
            raise ValueError("Un mismo producto no puede repetirse en los detalles")
        return detalles


class PedidoUpdate(BaseModel):
    estado: EstadoPedido


class DetallePedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    producto_id: int
    cantidad: int
    precio_unitario: float


class PedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: datetime
    estado: str
    total: float


class PedidoReadConDetalles(PedidoRead):
    detalles: List[DetallePedidoRead] = []
