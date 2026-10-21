from sqlmodel import Session
from app.modules.team.models import Team
from app.modules.team.schemas import TeamCreate


def create_team(session: Session, team_data: TeamCreate):
    team = Team(**team_data.model_dump())
    session.add(team)
    session.commit()
    session.refresh(team)
    return team
