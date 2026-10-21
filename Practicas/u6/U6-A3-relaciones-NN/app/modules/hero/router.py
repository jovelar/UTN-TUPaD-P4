from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.modules.hero.models import Hero, HeroTeamLink
from app.modules.hero.schemas import HeroReadWithTeams
from app.modules.hero.service import add_hero_to_team
from app.modules.team.models import Team

router = APIRouter(prefix="/heroes", tags=["heroes"])

# Crear un héroe básico
@router.post("/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# Leer un héroe con sus equipos
@router.get("/{hero_id}", response_model=HeroReadWithTeams)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# RELACIÓN N:M - Asignar un héroe a un equipo
@router.post("/{hero_id}/teams/{team_id}")
def assign_hero_to_team(hero_id: int, team_id: int, session: Session = Depends(get_session)):
    # 1. Verificamos que ambos existan
    hero = session.get(Hero, hero_id)
    team = session.get(Team, team_id)
    if not hero or not team:
        raise HTTPException(status_code=404, detail="Hero or Team not found")

    # 2. Creamos el vínculo en la tabla puente (add_hero_to_team ya verifica duplicados)
    add_hero_to_team(session, hero_id, team_id)
    return {"message": f"Héroe {hero.name} asignado al equipo {team.name}"}

# Este es el endpoint para el "unlink" (quitar un equipo de un héroe)
@router.delete("/{hero_id}/teams/{team_id}")
def remove_hero_from_team(hero_id: int, team_id: int, session: Session = Depends(get_session)):
    # 1. Buscamos el vínculo exacto en la tabla puente
    statement = select(HeroTeamLink).where(
        HeroTeamLink.hero_id == hero_id, 
        HeroTeamLink.team_id == team_id
    )
    results = session.exec(statement)
    link = results.first()
    
    # 2. Si no existe, avisamos
    if not link:
        raise HTTPException(status_code=404, detail="El vínculo no existe")
    
    # 3. Borramos el vínculo (pero el Héroe y el Equipo siguen existiendo)
    session.delete(link)
    session.commit()
    
    return {"message": "Héroe desvinculado del equipo correctamente"}