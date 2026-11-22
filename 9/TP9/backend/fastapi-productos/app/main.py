"""
Entry point de la aplicación FastAPI.

Responsabilidades:
  - Registrar routers (auth + categorías).
  - Configurar CORS para consumo desde frontend (React, etc.).
  - Crear tablas al arrancar (lifespan).
  - Health check en /health.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_all_tables
from app.modules.usuarios.router import router as auth_router, roles_router
from app.modules.categorias.router import router as categorias_router
from app.modules.productos.router import router as productos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas de BD al arrancar la aplicación."""
    # Si PostgreSQL no está disponible, la aplicación no arranca y muestra el error.
    # (Las pruebas no ejecutan el lifespan: usan SQLite en memoria.)
    create_all_tables()
    yield


app = FastAPI(
    title="API Productos y Categorías",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── CORS (ajustar origins en producción) ────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ─────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(categorias_router)
app.include_router(productos_router)


# ─── Health check ────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "version": "1.0.0"}
