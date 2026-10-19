from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List
from . import schemas, services
from database import SessionDep

router = APIRouter(prefix="/productos", tags=["Productos"])


# ---------------------------------------------------------
# ALTA DE PRODUCTO
# Método: POST | Endpoint: /productos | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/", response_model=schemas.ProductoRead, status_code=status.HTTP_201_CREATED
)
def alta_producto(producto: schemas.ProductoCreate, session:SessionDep):
    return services.crear(session,producto)


# (Extra) LISTAR PRODUCTOS
@router.get(
    "/", response_model=List[schemas.ProductoRead], status_code=status.HTTP_200_OK
)
def listar_productos(session: SessionDep, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    return services.obtener_todos(session,skip, limit)


# ---------------------------------------------------------
# DETALLE DE PRODUCTO
# Método: GET | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}", response_model=schemas.ProductoRead, status_code=status.HTTP_200_OK
)
def detalle_producto(session:SessionDep,id: int = Path(..., gt=0)):
    producto = services.obtener_por_id(session,id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return producto


# ---------------------------------------------------------
# ACTUALIZACIÓN (Reemplazo Total)
# Método: PUT | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}", response_model=schemas.ProductoRead, status_code=status.HTTP_200_OK
)
def actualizar_producto(producto: schemas.ProductoCreate, session: SessionDep,id: int = Path(..., gt=0)):
    # Usamos ProductoCreate porque es un reemplazo total (exige todos los campos)
    actualizado = services.actualizar_total(session,id, producto)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return actualizado


# ---------------------------------------------------------
# ELIMINAR PRODUCTO
# Método: DELETE | Endpoint: /productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_producto(session: SessionDep, id: int = Path(..., gt=0)):
    eliminado = services.eliminar(session, id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return {"ok": True}


# ---------------------------------------------------------
# CONSULTAR STOCK (Lógica de Negocio)
# Método: GET | Endpoint: /productos/{id}/stock | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}/stock",
    response_model=schemas.ProductoStockResponse,
    status_code=status.HTTP_200_OK,
)
def consultar_stock(session: SessionDep, id: int = Path(..., gt=0)):
    resultado = services.obtener_estado_stock(session, id)  # Llamada al servicio
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return resultado  # El router solo devuelve el resultado
