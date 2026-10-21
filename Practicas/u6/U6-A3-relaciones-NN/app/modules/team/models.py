from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.modules.hero.models import HeroTeamLink

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: str
    
    # La contraparte de la relación apuntando a Hero 
    hero_links: List["Hero"] = Relationship(
        back_populates="teams",
        link_model=HeroTeamLink
    )