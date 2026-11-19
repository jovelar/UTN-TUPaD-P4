from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List
from . import schema as schemas, service as services
from app.core.database import SessionDep

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


@router.post(
    "/", response_model=schemas.IngredienteRead, status_code=status.HTTP_201_CREATED
)
def alta_ingrediente(ingrediente: schemas.IngredienteCreate, session: SessionDep):
    return services.crear(session, ingrediente)


@router.get(
    "/", response_model=List[schemas.IngredienteRead], status_code=status.HTTP_200_OK
)
def listar_ingredientes(session: SessionDep, skip: int = Query(0, ge=0), limit: int = Query(100, le=100)):
    return services.obtener_todas(session, skip, limit)


@router.get(
    "/{id}", response_model=schemas.IngredienteRead, status_code=status.HTTP_200_OK
)
def detalle_ingrediente(session: SessionDep, id: int = Path(..., gt=0)):
    ingrediente = services.obtener_por_id(session, id)
    if not ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado"
        )
    return ingrediente


@router.put(
    "/{id}", response_model=schemas.IngredienteRead, status_code=status.HTTP_200_OK
)
def actualizar_ingrediente(ingrediente: schemas.IngredienteCreate, session: SessionDep, id: int = Path(..., gt=0)):
    actualizada = services.actualizar_total(session, id, ingrediente)
    if not actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado"
        )
    return actualizada


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ingrediente(session: SessionDep, id: int = Path(..., gt=0)):
    eliminada = services.eliminar(session, id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado"
        )