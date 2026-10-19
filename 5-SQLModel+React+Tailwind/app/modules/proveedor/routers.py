from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List
from typing import Optional
from . import schemas, services
from database import SessionDep

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


# ---------------------------------------------------------
# ALTA DE proveedor
# Método: POST | Endpoint: /proveedors | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/", response_model=schemas.ProveedorRead, status_code=status.HTTP_201_CREATED
)
def alta_proveedor(proveedor: schemas.ProveedorCreate, session: SessionDep):
    return services.crear(session, proveedor)


# (Extra) LISTAR proveedorS
@router.get(
    "/", response_model=List[schemas.ProveedorRead], status_code=status.HTTP_200_OK
)
def listar_proveedors(session: SessionDep,
                      skip: int = Query(0, ge=0),
                      limit: int = Query(10,ge=1, le=50),
                      activo: Optional[bool]= Query(None)):
    return services.obtener_todos(session, skip, limit, activo)


# ---------------------------------------------------------
# DETALLE DE proveedor
# Método: GET | Endpoint: /proveedors/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK
)
def detalle_proveedor(session: SessionDep, id: int = Path(..., gt=0)):
    proveedor = services.obtener_por_id(session, id)
    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="proveedor no encontrado"
        )
    return proveedor


# ---------------------------------------------------------
# ACTUALIZACIÓN (Reemplazo Total)
# Método: PUT | Endpoint: /proveedors/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK
)
def actualizar_proveedor(proveedor: schemas.ProveedorCreate, session: SessionDep, id: int = Path(..., gt=0)):
    # Usamos proveedorCreate porque es un reemplazo total (exige todos los campos)
    actualizado = services.actualizar_total(session, id, proveedor)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="proveedor no encontrado"
        )
    return actualizado


# ---------------------------------------------------------
# ELIMINAR proveedor
# Método: DELETE | Endpoint: /proveedores/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_proveedor(session: SessionDep, id: int = Path(..., gt=0)):
    eliminado = services.eliminar(session, id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="proveedor no encontrado"
        )
    return {"ok": True}