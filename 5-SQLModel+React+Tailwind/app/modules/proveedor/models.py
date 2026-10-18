from typing import Optional
from sqlmodel import SQLModel, Field

class Proveedor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str
    razon_social: str
    cuit: str
    email: str = ""
    telefono: str = ""
    activo: bool = True