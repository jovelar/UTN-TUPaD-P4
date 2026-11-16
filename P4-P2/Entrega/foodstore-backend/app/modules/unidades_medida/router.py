from typing import List
from fastapi import APIRouter, status
from sqlmodel import select
from app.core.database import SessionDep
from .model import UnidadMedida, UnidadMedidaPublic

router = APIRouter(prefix="/api/v1/unidades-medida", tags=["Unidades de medida"])


@router.get("", response_model=List[UnidadMedidaPublic], status_code=status.HTTP_200_OK)
def listar_unidades(session: SessionDep):
    return session.exec(select(UnidadMedida).order_by(UnidadMedida.id)).all()

