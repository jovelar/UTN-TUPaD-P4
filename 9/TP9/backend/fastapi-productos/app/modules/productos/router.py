"""
Router CRUD de Productos.

HTTP puro: parsear request, validar schema Pydantic, delegar al Service,
serializar response con response_model. No contiene lógica de negocio.

Capa: Router
Conoce a: Service (vía UoW)
NO conoce a: Repository, Model (solo esquemas para response_model)

Regla de imports:
    Router → Service → UoW → Repository → Model
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.uow import UnitOfWork, get_uow
from app.core.deps import get_current_active_user, require_role
from app.modules.usuarios.model import UserPublic
from app.modules.productos.model import (
    ProductoCreate, ProductoUpdate, ProductoCategoriaCreate, ProductoPublic,
)
from app.modules.productos.service import ProductoService

router = APIRouter(prefix="/api/v1/productos", tags=["productos"])


@router.get("/", response_model=list[ProductoPublic])
def list_productos(
    _user: Annotated[UserPublic, Depends(get_current_active_user)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        service = ProductoService(uow)
        return service.list_all()


@router.get("/{producto_id}", response_model=ProductoPublic)
def get_producto(
    producto_id: int,
    _user: Annotated[UserPublic, Depends(get_current_active_user)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        service = ProductoService(uow)
        return service.get_by_id(producto_id)


@router.post("/", response_model=ProductoPublic, status_code=status.HTTP_201_CREATED)
def create_producto(
    prod_in: ProductoCreate,
    _admin: Annotated[UserPublic, Depends(require_role(["admin"]))],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        service = ProductoService(uow)
        return service.create(prod_in)


@router.patch("/{producto_id}", response_model=ProductoPublic)
def update_producto(
    producto_id: int,
    prod_in: ProductoUpdate,
    _admin: Annotated[UserPublic, Depends(require_role(["admin"]))],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        service = ProductoService(uow)
        return service.update(producto_id, prod_in)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(
    producto_id: int,
    _admin: Annotated[UserPublic, Depends(require_role(["admin"]))],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        service = ProductoService(uow)
        service.delete(producto_id)


@router.post(
    "/{producto_id}/categorias",
    response_model=ProductoPublic,
    status_code=status.HTTP_201_CREATED,
)
def asignar_categoria(
    producto_id: int,
    data: ProductoCategoriaCreate,
    _admin: Annotated[UserPublic, Depends(require_role(["admin"]))],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        service = ProductoService(uow)
        return service.asignar_categoria(producto_id, data)


@router.delete("/{producto_id}/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def quitar_categoria(
    producto_id: int,
    categoria_id: int,
    _admin: Annotated[UserPublic, Depends(require_role(["admin"]))],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        service = ProductoService(uow)
        service.quitar_categoria(producto_id, categoria_id)