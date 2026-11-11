from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=3)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaRead(CategoriaBase):
    id: int