from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session, select
from .model import Producto, ProductoCategoria
from .schema import (
    ProductoCreate,
    ProductoUpdate,
    ProductoPublic,
    CategoriaDeProducto,
    ProductoCategoriaCreate,
)
from app.modules.categorias.model import Categoria
from app.modules.unidades_medida.model import UnidadMedida, UnidadMedidaPublic, TipoUnidadMedida


def obtener_existente(session: Session, id: int) -> Producto:
    producto = session.get(Producto, id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto


def nombre_existente(session: Session, nombre: str, id_actual: Optional[int] = None) -> None:
    existente = session.exec(
        select(Producto).where(Producto.nombre == nombre, Producto.activo == True)
    ).first()
    if existente and existente.id != id_actual:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un producto activo con ese nombre")


def validar_unidad_y_stock(session: Session, data: ProductoCreate) -> None:
    unidad = session.get(UnidadMedida, data.unidad_venta_id)
    if not unidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidad de medida no encontrada")
    # RN-10: en unidades contables el stock tiene que ser entero
    if unidad.tipo == TipoUnidadMedida.contable and data.stock_cantidad % 1 != 0:
        raise HTTPException(status_code=422, detail="El stock debe ser un número entero para unidades contables")


def categorias_de_producto(session: Session, producto_id: int) -> List[CategoriaDeProducto]:
    vinculos = session.exec(
        select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
    ).all()
    categorias = []
    for vinculo in vinculos:
        categoria = session.get(Categoria, vinculo.categoria_id)
        categorias.append(
            CategoriaDeProducto(
                id=categoria.id,
                nombre=categoria.nombre,
                descripcion=categoria.descripcion,
                activo=categoria.activo,
                es_principal=vinculo.es_principal,
            )
        )
    return categorias


def armar_public(session: Session, producto: Producto) -> ProductoPublic:
    unidad = producto.unidad_venta
    return ProductoPublic(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio_base=float(producto.precio_base),
        stock_cantidad=float(producto.stock_cantidad),
        disponible=producto.disponible,
        activo=producto.activo,
        anulado_at=producto.anulado_at,
        unidad_venta_id=producto.unidad_venta_id,
        unidad_venta=UnidadMedidaPublic(
            id=unidad.id, nombre=unidad.nombre, simbolo=unidad.simbolo, tipo=unidad.tipo
        ),
        categorias=categorias_de_producto(session, producto.id),
        # RN-11: se calcula en cada lectura, no se guarda
        hay_stock=producto.stock_cantidad > 0,
    )


def crear(session: Session, data: ProductoCreate) -> ProductoPublic:
    nombre_existente(session, data.nombre)
    validar_unidad_y_stock(session, data)
    nuevo = Producto(**data.model_dump())
    try:
        session.add(nuevo)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(nuevo)
    return armar_public(session, nuevo)


def obtener_todos(
    session: Session,
    skip: int,
    limit: int,
    activo: Optional[bool] = None,
    disponible: Optional[bool] = None,
    categoria_id: Optional[int] = None,
    search: Optional[str] = None,
) -> List[ProductoPublic]:
    query = select(Producto)
    if activo is False:
        query = query.where(Producto.activo == False)
    else:
        query = query.where(Producto.activo == True)
    if disponible is not None:
        query = query.where(Producto.disponible == disponible)
    if categoria_id is not None:
        query = query.join(ProductoCategoria, ProductoCategoria.producto_id == Producto.id).where(
            ProductoCategoria.categoria_id == categoria_id
        )
    if search:
        query = query.where(Producto.nombre.ilike(f"%{search}%"))
    productos = session.exec(query.order_by(Producto.id).offset(skip).limit(limit)).all()
    return [armar_public(session, producto) for producto in productos]


def obtener_por_id(session: Session, id: int) -> ProductoPublic:
    return armar_public(session, obtener_existente(session, id))


def actualizar_total(session: Session, id: int, data: ProductoUpdate) -> ProductoPublic:
    producto = obtener_existente(session, id)
    if not producto.activo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede modificar un producto anulado")
    nombre_existente(session, data.nombre, id)
    validar_unidad_y_stock(session, data)
    producto.sqlmodel_update(data.model_dump())
    try:
        session.add(producto)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(producto)
    return armar_public(session, producto)


def eliminar(session: Session, id: int) -> None:
    producto = obtener_existente(session, id)
    if not producto.activo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El producto ya está anulado")
    producto.activo = False
    producto.anulado_at = datetime.now(timezone.utc)
    try:
        session.add(producto)
        session.commit()
    except Exception:
        session.rollback()
        raise


def asignar_categoria(session: Session, producto_id: int, data: ProductoCategoriaCreate) -> ProductoCategoria:
    producto = obtener_existente(session, producto_id)
    categoria = session.get(Categoria, data.categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    if not producto.activo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede clasificar un producto anulado")
    if not categoria.activo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede clasificar en una categoría anulada")
    if session.get(ProductoCategoria, (producto_id, data.categoria_id)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El producto ya tiene esa categoría")
    # RN-09: si la nueva es principal, la anterior deja de serlo
    if data.es_principal:
        anteriores = session.exec(
            select(ProductoCategoria).where(
                ProductoCategoria.producto_id == producto_id,
                ProductoCategoria.es_principal == True,
            )
        ).all()
        for anterior in anteriores:
            anterior.es_principal = False
            session.add(anterior)
    vinculo = ProductoCategoria(
        producto_id=producto_id, categoria_id=data.categoria_id, es_principal=data.es_principal
    )
    try:
        session.add(vinculo)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(vinculo)
    return vinculo


def obtener_categorias(session: Session, producto_id: int) -> List[CategoriaDeProducto]:
    obtener_existente(session, producto_id)
    return categorias_de_producto(session, producto_id)