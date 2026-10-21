from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.core.database import engine # SQLModel necesita las clases en memoria

# Importamos los modelos para que SQLModel los vea al crear las tablas
# from app.modules.weapon.models import Weapon
from app.modules.hero.models import Hero, HeroTeamLink
from app.modules.team.models import Team

# ── Routers ───────────────────────────────
from app.modules.hero.router import router as hero_router
from app.modules.team.router import router as team_router
# from app.modules.weapon.router import router as weapon_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: esta línea crea las tablas en PostgreSQL automáticamente al arrancar
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="FastAPI + SQLModel", lifespan=lifespan)

# Incluimos los routers para que aparezcan en /docs
# app.include_router(weapon_router)
app.include_router(team_router)
app.include_router(hero_router)