from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List
from typing import Optional
from . import schemas, services

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


# ---------------------------------------------------------
# ALTA DE proveedor
# Método: POST | Endpoint: /proveedors | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/", response_model=schemas.ProveedorRead, status_code=status.HTTP_201_CREATED
)
def alta_proveedor(proveedor: schemas.ProveedorCreate):
    return services.crear(proveedor)


# (Extra) LISTAR proveedorS
@router.get(
    "/", response_model=List[schemas.ProveedorRead], status_code=status.HTTP_200_OK
)
def listar_proveedors(skip: int = Query(0, ge=0), 
                      limit: int = Query(10,ge=1, le=50),
                      activo: Optional[bool]= Query(None)):
    return services.obtener_todos(skip, limit,activo)


# ---------------------------------------------------------
# DETALLE DE proveedor
# Método: GET | Endpoint: /proveedors/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}", response_model=schemas.ProveedorRead, status_code=status.HTTP_200_OK
)
def detalle_proveedor(id: int = Path(..., gt=0)):
    proveedor = services.obtener_por_id(id)
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
def actualizar_proveedor(proveedor: schemas.ProveedorCreate, id: int = Path(..., gt=0)):
    # Usamos proveedorCreate porque es un reemplazo total (exige todos los campos)
    actualizado = services.actualizar_total(id, proveedor)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="proveedor no encontrado"
        )
    return actualizado


# ---------------------------------------------------------
# BORRADO LÓGICO
# Método: PUT | Endpoint: /proveedors/{id}/desactivar | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}/desactivar",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(id: int = Path(..., gt=0)):
    desactivado = services.desactivar(id)
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="proveedor no encontrado"
        )
    return desactivado


# # ---------------------------------------------------------
# # CONSULTAR STOCK (Lógica de Negocio)
# # Método: GET | Endpoint: /proveedors/{id}/stock | Estado: 200 OK
# # ---------------------------------------------------------
# @router.get(
#     "/{id}/stock",
#     response_model=schemas.ProveedorStockResponse,
#     status_code=status.HTTP_200_OK,
# )
# @router.get("/{id}/stock", response_model=schemas.ProveedorStockResponse)
# def consultar_stock(id: int = Path(..., gt=0)):
#     resultado = services.obtener_estado_stock(id)  # Llamada al servicio
#     if not resultado:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="proveedor no encontrado"
#         )
#     return resultado  # El router solo devuelve el resultado
