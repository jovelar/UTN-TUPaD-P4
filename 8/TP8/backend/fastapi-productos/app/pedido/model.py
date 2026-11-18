from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Pedido(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    fecha:datetime = Field(default_factory=datetime.now)
    estado:str = Field(default="PENDIENTE")
    total:float
    deleted_at:Optional[datetime]=Field(default=None)
    
    
class DetallePedido(SQLModel,table=True):
    pedido_id:int=Field(foreign_key="pedido.id",primary_key=True)
    producto_id:int=Field(foreign_key="producto.id",primary_key=True)
    cantidad:int
    precio_unitario:float