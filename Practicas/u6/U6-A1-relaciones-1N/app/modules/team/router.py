from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.modules.team.schemas import TeamCreate
from app.modules.team import service

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/")
def create_team(
    team: TeamCreate,
    session: Session = Depends(get_session)
):
    return service.create_team(session, team)
