from typing import List, Optional
from sqlmodel import Session, select
from .models import Categoria
from .schemas import CategoriaCreate


def crear(session: Session, data: CategoriaCreate) -> Categoria:
    nueva = Categoria(**data.model_dump())
    try:
        session.add(nueva)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(nueva)
    return nueva


def obtener_todas(session: Session, skip: int = 0, limit: int = 10) -> List[Categoria]:
    return session.exec(select(Categoria).offset(skip).limit(limit)).all()


def obtener_por_id(session: Session, id: int) -> Optional[Categoria]:
    return session.get(Categoria, id)


def actualizar_total(session: Session, id: int, data: CategoriaCreate) -> Optional[Categoria]:
    categoria = session.get(Categoria, id)
    if not categoria:
        return None
    categoria.sqlmodel_update(data.model_dump())
    try:
        session.add(categoria)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(categoria)
    return categoria


def eliminar(session: Session, id: int) -> bool:
    categoria = session.get(Categoria, id)
    if not categoria:
        return False
    try:
        session.delete(categoria)
        session.commit()
    except Exception:
        session.rollback()
        raise
    return True