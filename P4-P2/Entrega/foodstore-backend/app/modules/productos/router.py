from typing import List, Optional
from fastapi import APIRouter, Path, Query, status
from . import schema as schemas, service as services
from app.core.database import SessionDep

router = APIRouter(prefix="/api/v1/productos", tags=["Productos"])


# ---------------------------------------------------------
# ALTA DE PRODUCTO
# Método: POST | Endpoint: /api/v1/productos | Estado: 201 Created
# ---------------------------------------------------------
@router.post("", response_model=schemas.ProductoPublic, status_code=status.HTTP_201_CREATED)
def alta_producto(producto: schemas.ProductoCreate, session: SessionDep):
    return services.crear(session, producto)


# ---------------------------------------------------------
# LISTAR PRODUCTOS (paginación y filtros)
# Método: GET | Endpoint: /api/v1/productos | Estado: 200 OK
# ---------------------------------------------------------
@router.get("", response_model=List[schemas.ProductoPublic], status_code=status.HTTP_200_OK)
def listar_productos(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    activo: Optional[bool] = Query(None),
    disponible: Optional[bool] = Query(None),
    categoria_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
):
    return services.obtener_todos(session, skip, limit, activo, disponible, categoria_id, search)


# ---------------------------------------------------------
# DETALLE DE PRODUCTO
# Método: GET | Endpoint: /api/v1/productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get("/{id}", response_model=schemas.ProductoPublic, status_code=status.HTTP_200_OK)
def detalle_producto(session: SessionDep, id: int = Path(..., gt=0)):
    return services.obtener_por_id(session, id)


# ---------------------------------------------------------
# ACTUALIZACIÓN (Reemplazo de los campos propios)
# Método: PUT | Endpoint: /api/v1/productos/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.put("/{id}", response_model=schemas.ProductoPublic, status_code=status.HTTP_200_OK)
def actualizar_producto(producto: schemas.ProductoUpdate, session: SessionDep, id: int = Path(..., gt=0)):
    return services.actualizar_total(session, id, producto)


# ---------------------------------------------------------
# ANULAR PRODUCTO (baja lógica)
# Método: DELETE | Endpoint: /api/v1/productos/{id} | Estado: 204 No Content
# ---------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def anular_producto(session: SessionDep, id: int = Path(..., gt=0)):
    services.eliminar(session, id)


# ---------------------------------------------------------
# CLASIFICAR PRODUCTO EN UNA CATEGORÍA
# Método: POST | Endpoint: /api/v1/productos/{id}/categorias | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/{id}/categorias",
    response_model=schemas.ProductoCategoriaPublic,
    status_code=status.HTTP_201_CREATED,
)
def asignar_categoria(vinculo: schemas.ProductoCategoriaCreate, session: SessionDep, id: int = Path(..., gt=0)):
    return services.asignar_categoria(session, id, vinculo)


# ---------------------------------------------------------
# LISTAR CATEGORÍAS DE UN PRODUCTO
# Método: GET | Endpoint: /api/v1/productos/{id}/categorias | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}/categorias",
    response_model=List[schemas.CategoriaDeProducto],
    status_code=status.HTTP_200_OK,
)
def listar_categorias_producto(session: SessionDep, id: int = Path(..., gt=0)):
    return services.obtener_categorias(session, id)