# database.py — core/database.py
from typing import Generator
import os
from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:TU_CONTRASENIA@localhost:5432/heroes_api",
)

engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    # FastAPI inyecta una sesión por request
    with Session(engine) as session:
        yield session