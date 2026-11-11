from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.core.seed import seed_unidades_medida
from app.modules.unidades_medida.model import UnidadMedida
from app.modules.productos.model import Producto, ProductoCategoria
from app.modules.categorias.model import Categoria
from app.modules.unidades_medida.router import router as unidad_medida_router
from app.modules.productos.router import router as producto_router
from app.modules.categorias.router import router as categoria_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_unidades_medida()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Food Store - Catálogo de Productos", version="1.0.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(unidad_medida_router)
    app.include_router(producto_router)
    app.include_router(categoria_router)

    return app

app = create_app()