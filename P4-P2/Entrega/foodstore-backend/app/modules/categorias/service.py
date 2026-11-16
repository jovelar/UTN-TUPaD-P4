from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session, select
from .model import Categoria
from .schema import CategoriaCreate, CategoriaUpdate


def obtener_existente(session: Session, id: int) -> Categoria:
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return categoria


def nombre_existente(session: Session, nombre: str, id_actual: Optional[int] = None) -> None:
    existente = session.exec(
        select(Categoria).where(Categoria.nombre == nombre, Categoria.activo == True)
    ).first()
    if existente and existente.id != id_actual:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe una categoría activa con ese nombre")


def crear(session: Session, data: CategoriaCreate) -> Categoria:
    nombre_existente(session, data.nombre)
    nueva = Categoria(**data.model_dump())
    try:
        session.add(nueva)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(nueva)
    return nueva


def obtener_todas(session: Session, activo: Optional[bool] = None, search: Optional[str] = None) -> List[Categoria]:
    query = select(Categoria)
    if activo is False:
        query = query.where(Categoria.activo == False)
    else:
        query = query.where(Categoria.activo == True)
    if search:
        query = query.where(Categoria.nombre.ilike(f"%{search}%"))
    return session.exec(query).all()


def obtener_por_id(session: Session, id: int) -> Categoria:
    return obtener_existente(session, id)


def actualizar_total(session: Session, id: int, data: CategoriaUpdate) -> Categoria:
    categoria = obtener_existente(session, id)
    if not categoria.activo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede modificar una categoría anulada")
    nombre_existente(session, data.nombre, id)
    categoria.sqlmodel_update(data.model_dump())
    try:
        session.add(categoria)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(categoria)
    return categoria


def eliminar(session: Session, id: int) -> None:
    categoria = obtener_existente(session, id)
    if not categoria.activo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La categoría ya está anulada")
    categoria.activo = False
    categoria.anulado_at = datetime.now(timezone.utc)
    try:
        session.add(categoria)
        session.commit()
    except Exception:
        session.rollback()
        raise