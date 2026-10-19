from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session, select
from .models import Proveedor
from .schemas import ProveedorCreate


def codigo_existente(session: Session, codigo: str, id_actual: Optional[int] = None) -> None:
    existente = session.exec(select(Proveedor).where(Proveedor.codigo == codigo)).first()
    if existente and existente.id != id_actual:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El codigo de proveedor ya existe")


def crear(session: Session, data: ProveedorCreate) -> Proveedor:
    codigo_existente(session, data.codigo)
    nuevo = Proveedor(**data.model_dump())
    try:
        session.add(nuevo)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(nuevo)
    return nuevo


def obtener_todos(session: Session, skip: int, limit: int, activo: Optional[bool]) -> List[Proveedor]:
    consulta = select(Proveedor)
    if activo is not None:
        consulta = consulta.where(Proveedor.activo == activo)
    return session.exec(consulta.offset(skip).limit(limit)).all()


def obtener_por_id(session: Session, id: int) -> Optional[Proveedor]:
    return session.get(Proveedor, id)


def actualizar_total(session: Session, id: int, data: ProveedorCreate) -> Optional[Proveedor]:
    proveedor = session.get(Proveedor, id)
    if not proveedor:
        return None
    codigo_existente(session, data.codigo, id)
    proveedor.sqlmodel_update(data.model_dump())
    try:
        session.add(proveedor)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(proveedor)
    return proveedor



def eliminar(session: Session, id: int) -> bool:
    proveedor = session.get(Proveedor, id)
    if not proveedor:
        return False
    try:
        session.delete(proveedor)
        session.commit()
    except Exception:
        session.rollback()
        raise
    return True