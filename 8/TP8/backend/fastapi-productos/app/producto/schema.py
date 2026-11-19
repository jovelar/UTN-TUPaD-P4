from typing import Annotated, List
from pydantic import BaseModel, Field, StringConstraints
from app.categoria.schema import CategoriaRead


class ProductoBase(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    descripcion: str
    precio_base: float = Field(ge=0)
    imagenes_url: List[str] = []
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoRead(ProductoBase):
    id: int


class ProductoReadWithCategorias(ProductoRead):
    categorias: List[CategoriaRead] = []
    

class ProductoCategoriaCreate(BaseModel):
    categoria_id: int = Field(gt=0)