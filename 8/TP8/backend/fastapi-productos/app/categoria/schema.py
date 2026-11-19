from typing import Annotated
from pydantic import BaseModel, StringConstraints


class CategoriaBase(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    descripcion: str = ""


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaRead(CategoriaBase):
    id: int