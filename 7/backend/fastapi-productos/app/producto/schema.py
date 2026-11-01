from typing import List
from pydantic import BaseModel, Field
from app.categoria.schema import CategoriaRead


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    descripcion: str
    precio_base: float = Field(ge=0)
    imagen_url: List[str] = []
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoRead(ProductoBase):
    id: int


class ProductoReadWithCategorias(ProductoRead):
    categorias: List[CategoriaRead] = []