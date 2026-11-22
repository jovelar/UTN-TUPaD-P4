"""
Engine de SQLModel.

Usa PostgreSQL, configurado mediante variables de entorno.
Las pruebas reemplazan el engine que usa el Unit of Work por SQLite en memoria.
"""

from sqlmodel import SQLModel, create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def create_all_tables() -> None:
    """Crea las tablas registradas en SQLModel.metadata al arrancar la app."""
    import app.modules.usuarios.model     # noqa: F401 — registra el modelo en metadata
    import app.modules.categorias.model   # noqa: F401
    import app.modules.productos.model    # noqa: F401
    SQLModel.metadata.create_all(engine)