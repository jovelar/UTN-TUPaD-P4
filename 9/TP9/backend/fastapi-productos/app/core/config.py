"""
Configuración centralizada leída desde variables de entorno.

Usa variables individuales de PostgreSQL y construye DATABASE_URL
con una propiedad.
Los valores sensibles (SECRET_KEY, POSTGRES_PASSWORD) viven en .env.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ─── Base de datos (PostgreSQL) ──────────────────────────
    postgres_user:     str = "postgres"
    postgres_password: str                     # Obligatoria: se lee de .env
    postgres_db:       str = "seguridad_jwt_db"
    postgres_host:     str = "localhost"
    postgres_port:     int = 5432


    # DATABASE_URL es una propiedad común (sin @computed_field): así no aparece
    # en settings.model_dump() ni en ningún volcado de la configuración, ya que
    # contiene la contraseña de la base.
    @property
    def DATABASE_URL(self) -> str:
        """
        Construye la URL de conexión a PostgreSQL.
        Las pruebas no la usan: tests/conftest.py reemplaza el engine por SQLite en memoria.
        """
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # ─── JWT ──────────────────────────────────────────────────────────────────
    SECRET_KEY: str = Field(min_length=32)   # Obligatoria, sin valor por defecto
    ALGORITHM:  str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = {
        "env_file":          ".env",
        "env_file_encoding": "utf-8",
        "extra":             "ignore",   # ignora vars extra del .env (ej. DATABASE_URL literal)
    }


# Instancia global — importar desde aquí en toda la app
settings = Settings()
