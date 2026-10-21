from fastapi import HTTPException
from sqlmodel import Session, select
from app.modules.hero.models import Hero, HeroTeamLink
from app.modules.team.models import Team

# Función para AGREGAR al equipo
def add_hero_to_team(session: Session, hero_id: int, team_id: int):
    hero = session.get(Hero, hero_id)
    team = session.get(Team, team_id)
    if not hero or not team:
        return None

    # Evitar duplicados
    existing = session.exec(
        select(HeroTeamLink).where(
            HeroTeamLink.hero_id == hero_id,
            HeroTeamLink.team_id == team_id
        )
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="El héroe ya pertenece a ese equipo")

    link = HeroTeamLink(hero_id=hero_id, team_id=team_id)
    session.add(link)
    session.commit()

    return session.get(Hero, hero_id)

# Función para QUITAR del equipo 
def remove_hero_from_team(session: Session, hero_id: int, team_id: int):
    link = session.exec(
        select(HeroTeamLink).where(
            HeroTeamLink.hero_id == hero_id, 
            HeroTeamLink.team_id == team_id  
        )
    ).first() 
    
    if not link: 
        return None
        
    session.delete(link) 
    session.commit() 
    return session.get(Hero, hero_id) 