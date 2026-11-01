from .model import Producto, ProductoCategoria
from .schema import ProductoCreate
from app.categoria.model import Categoria
from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session, select



def asignar_categoria(session: Session, producto_id: int, categoria_id: int) -> ProductoCategoria:
    if not session.get(Producto, producto_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    if not session.get(Categoria, categoria_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    if session.get(ProductoCategoria, (producto_id, categoria_id)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El producto ya tiene esa categoría")
    vinculo = ProductoCategoria(producto_id=producto_id, categoria_id=categoria_id)
    try:
        session.add(vinculo)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(vinculo)
    return vinculo


def obtener_categorias(session: Session, producto_id: int) -> Optional[List[Categoria]]:
    producto = session.get(Producto, producto_id)
    if not producto:
        return None
    return producto.categorias


def quitar_categoria(session: Session, producto_id: int, categoria_id: int) -> bool:
    vinculo = session.get(ProductoCategoria, (producto_id, categoria_id))
    if not vinculo:
        return False
    try:
        session.delete(vinculo)
        session.commit()
    except Exception:
        session.rollback()
        raise
    return True

def crear(session: Session, data: ProductoCreate) -> Producto:
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