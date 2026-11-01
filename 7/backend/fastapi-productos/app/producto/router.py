from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List
from . import schema as schemas, service as services
from app.core.database import SessionDep

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
def listar_productos(session: SessionDep, skip: int = Query(0, ge=0), limit: int = Query(10, le=50)):
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
# ASIGNAR CATEGORÍA A PRODUCTO
# Método: POST | Endpoint: /productos/{id}/categorias/{categoria_id} | Estado: 201 Created
# ---------------------------------------------------------
@router.post("/{id}/categorias/{categoria_id}", status_code=status.HTTP_201_CREATED)
def asignar_categoria(session: SessionDep, id: int = Path(..., gt=0), categoria_id: int = Path(..., gt=0)):
    return services.asignar_categoria(session, id, categoria_id)



# ---------------------------------------------------------
# LISTAR CATEGORÍAS DE UN PRODUCTO
# Método: GET | Endpoint: /productos/{id}/categorias | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}/categorias", response_model=List[schemas.CategoriaRead], status_code=status.HTTP_200_OK
)
def listar_categorias_producto(session: SessionDep, id: int = Path(..., gt=0)):
    categorias = services.obtener_categorias(session, id)
    if categorias is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return categorias


# ---------------------------------------------------------
# QUITAR CATEGORÍA DE PRODUCTO
# Método: DELETE | Endpoint: /productos/{id}/categorias/{categoria_id} | Estado: 200 OK
# ---------------------------------------------------------
@router.delete("/{id}/categorias/{categoria_id}", status_code=status.HTTP_200_OK)
def quitar_categoria(session: SessionDep, id: int = Path(..., gt=0), categoria_id: int = Path(..., gt=0)):
    eliminado = services.quitar_categoria(session, id, categoria_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El producto no tiene esa categoría"
        )
    return {"ok": True}

# # ---------------------------------------------------------
# # CONSULTAR STOCK (Lógica de Negocio)
# # Método: GET | Endpoint: /productos/{id}/stock | Estado: 200 OK
# # ---------------------------------------------------------
# @router.get(
#     "/{id}/stock",
#     response_model=schemas.ProductoStockResponse,
#     status_code=status.HTTP_200_OK,
# )
# @router.get("/{id}/stock", response_model=schemas.ProductoStockResponse)
# def consultar_stock(session: SessionDep, id: int = Path(..., gt=0)):
#     resultado = services.obtener_estado_stock(session, id)  # Llamada al servicio
#     if not resultado:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
#         )
#     return resultado  # El router solo devuelve el resultado

