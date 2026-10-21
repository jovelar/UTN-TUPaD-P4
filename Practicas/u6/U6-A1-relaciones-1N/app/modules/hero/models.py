from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.weapon.models import Weapon
    from app.modules.team.models import Team


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    weapon_id: int | None = Field(
        default=None,
        foreign_key="weapon.id",
        unique=True
    )

    weapon: Optional["Weapon"] = Relationship(back_populates="hero")

    team_id: int | None = Field(default=None, foreign_key="team.id")

    team: Optional["Team"] = Relationship(back_populates="heroes")