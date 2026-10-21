from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.core.database import engine
from app.modules.hero.router import router as hero_router
from app.modules.weapon.router import router as weapon_router
from app.modules.team.router import router as team_router

from app.modules.hero.models import Hero
from app.modules.weapon.models import Weapon
from app.modules.team.models import Team


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(hero_router)
app.include_router(weapon_router)
app.include_router(team_router)