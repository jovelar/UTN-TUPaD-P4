from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.modules.hero.models import Hero
from app.modules.hero.schemas import HeroCreate
from app.modules.team.models import Team


def create_hero(session: Session, hero_data: HeroCreate):
    if hero_data.team_id is not None:
        team = session.get(Team, hero_data.team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

    hero = Hero(**hero_data.model_dump())
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


def get_hero(session: Session, hero_id: int):
    statement = (
        select(Hero)
        .where(Hero.id == hero_id)
        .options(selectinload(Hero.weapon), selectinload(Hero.team))
    )
    return session.exec(statement).first()