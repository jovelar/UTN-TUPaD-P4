
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, Integer, ForeignKey

# 1. La Tabla de Enlace (Debe ir ANTES de la clase Hero)
class HeroTeamLink(SQLModel, table=True):
    __tablename__ = "hero_team_link"
    hero_id: int = Field(
        sa_column=Column(Integer, ForeignKey("hero.id", ondelete="CASCADE"), primary_key=True, nullable=False) 
    )
    team_id: int = Field(
        sa_column=Column(Integer, ForeignKey("team.id", ondelete="CASCADE"), primary_key=True, nullable=False) 
    )

# 2. modelo Hero actualizado
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    
    # Esta es la relación que conecta con Team a través del Link 
    teams: List["Team"] = Relationship(
        back_populates="hero_links",
        link_model=HeroTeamLink
    )
    