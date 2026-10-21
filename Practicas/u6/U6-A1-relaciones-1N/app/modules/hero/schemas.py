from typing import Optional
from sqlmodel import SQLModel

from app.modules.weapon.schemas import WeaponRead


class HeroCreate(SQLModel):
    name: str
    weapon_id: Optional[int] = None
    team_id: Optional[int] = None


class HeroRead(SQLModel):
    id: int
    name: str
    weapon_id: Optional[int] = None
    team_id: Optional[int] = None


class TeamBasicRead(SQLModel):  # esquema reducido para romper el ciclo team <-> hero
    id: int
    name: str


class HeroReadFull(HeroRead):
    weapon: Optional[WeaponRead] = None
    team: Optional[TeamBasicRead] = None