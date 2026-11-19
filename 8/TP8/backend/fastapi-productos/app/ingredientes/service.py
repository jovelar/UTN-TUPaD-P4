from typing import List, Optional
from sqlmodel import Session, select
from .model import Ingrediente
from .schema import IngredienteCreate


def crear(session: Session, data: IngredienteCreate) -> Ingrediente:
    nueva = Ingrediente(**data.model_dump())
    try:
        session.add(nueva)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(nueva)
    return nueva


def obtener_todas(session: Session, skip: int = 0, limit: int = 10) -> List[Ingrediente]:
    return session.exec(select(Ingrediente).offset(skip).limit(limit)).all()


def obtener_por_id(session: Session, id: int) -> Optional[Ingrediente]:
    return session.get(Ingrediente, id)


def actualizar_total(session: Session, id: int, data: IngredienteCreate) -> Optional[Ingrediente]:
    ingrediente = session.get(Ingrediente, id)
    if not ingrediente:
        return None
    ingrediente.sqlmodel_update(data.model_dump())
    try:
        session.add(ingrediente)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(ingrediente)
    return ingrediente


def eliminar(session: Session, id: int) -> bool:
    ingrediente = session.get(Ingrediente, id)
    if not ingrediente:
        return False
    try:
        session.delete(ingrediente)
        session.commit()
    except Exception:
        session.rollback()
        raise
    return True