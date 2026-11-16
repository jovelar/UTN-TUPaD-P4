from typing import List, Optional
from fastapi import APIRouter, Path, Query, status
from . import schema as schemas, service as services
from app.core.database import SessionDep
from datetime import datetime
from .schema import CategoriaCreate, CategoriaUpdate

router = APIRouter(prefix="/api/v1/categorias", tags=["Categorías"])


@router.post("", response_model=schemas.CategoriaPublic, status_code=status.HTTP_201_CREATED)
def alta_categoria(categoria: schemas.CategoriaCreate, session: SessionDep):
    return services.crear(session, categoria)


@router.get("", response_model=List[schemas.CategoriaPublic], status_code=status.HTTP_200_OK)
def listar_categorias(
    session: SessionDep,
    activo: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
):
    return services.obtener_todas(session, activo, search)


@router.get("/{id}", response_model=schemas.CategoriaPublic, status_code=status.HTTP_200_OK)
def detalle_categoria(session: SessionDep, id: int = Path(..., gt=0)):
    return services.obtener_por_id(session, id)


@router.put("/{id}", response_model=schemas.CategoriaPublic, status_code=status.HTTP_200_OK)
def actualizar_categoria(categoria: schemas.CategoriaUpdate, session: SessionDep, id: int = Path(..., gt=0)):
    return services.actualizar_total(session, id, categoria)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def anular_categoria(session: SessionDep, id: int = Path(..., gt=0)):
    services.eliminar(session, id)