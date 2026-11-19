from typing import Annotated
from pydantic import BaseModel, StringConstraints


class IngredienteBase(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteRead(IngredienteBase):
    id: int
# from pydantic import BaseModel, Field


# class CategoriaBase(BaseModel):
#     nombre: str = Field(..., min_length=1)
#     descripcion: str = Field(..., min_length=3)


# class CategoriaCreate(CategoriaBase):
#     pass


# class CategoriaRead(CategoriaBase):
#     id: int

