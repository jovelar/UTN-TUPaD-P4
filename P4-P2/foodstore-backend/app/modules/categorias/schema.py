from pydantic import BaseModel, Field
from typing import Optional,Annotated
from datetime import datetime

class CategoriaBase(BaseModel):
    nombre: Annotated[str,Field(min_length=3)]
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaPublic(CategoriaBase):
    id:int
    activo:bool
    anulado_at:Optional[datetime]=None