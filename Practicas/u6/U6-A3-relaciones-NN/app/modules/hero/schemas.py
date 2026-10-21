from typing import List

from sqlmodel import SQLModel

from app.modules.team.schemas import TeamRead


class HeroReadWithTeams(SQLModel):
    id: int
    name: str
    secret_name: str
    teams: List[TeamRead] = []
