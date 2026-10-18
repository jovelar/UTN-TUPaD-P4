from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session, select
from .models import Producto
from .schemas import ProductoCreate


def nombre_existente(session: Session, nombre: str, id_actual: Optional[int] = None) -> None:
    existente = session.exec(select(Producto).where(Producto.nombre == nombre)).first()
    if existente and existente.id != id_actual:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un producto con ese nombre")


def crear(session: Session, data: ProductoCreate) -> Producto:
    nombre_existente(session, data.nombre)
    nuevo = Producto(**data.model_dump())
    try:
        session.add(nuevo)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(nuevo)
    return nuevo


def obtener_todos(session: Session, skip: int, limit: int) -> List[Producto]:
    return session.exec(select(Producto).offset(skip).limit(limit)).all()


def obtener_por_id(session: Session, id: int) -> Optional[Producto]:
    return session.get(Producto, id)


def actualizar_total(session: Session, id: int, data: ProductoCreate) ->Optional[Producto]:
    producto = session.get(Producto, id)
    if not producto:
        return None
    nombre_existente(session, data.nombre, id)
    producto.sqlmodel_update(data.model_dump())
    try:
        session.add(producto)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(producto)
    return producto


def eliminar(session: Session, id: int) -> bool:
    producto = session.get(Producto, id)
    if not producto:
        return False
    try:
        session.delete(producto)
        session.commit()
    except Exception:
        session.rollback()
        raise
    return True


def obtener_estado_stock(session: Session, id: int) -> Optional[dict]:
    producto = obtener_por_id(session, id)
    if not producto:
        return None

    # La lógica de negocio vive aquí
    alerta_stock = producto.stock < producto.stock_minimo

    return {
        "stock": producto.stock,
        "bajo_stock_minimo": alerta_stock,
        "activo": producto.activo
    }