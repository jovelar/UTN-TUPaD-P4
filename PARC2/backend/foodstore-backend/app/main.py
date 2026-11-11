from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.modules.producto.model import Producto, ProductoCategoria
from app.modules.categoria.model import Categoria
from app.modules.unidades_medida.model import UnidadMedida
from app.modules.producto.router import router as producto_router
from app.modules.categoria.router import router as categoria_router
#from app.modules.unidades_medida.router import router as medida_router


def create_app() -> FastAPI:
    app = FastAPI(title="API Productos y Categorías", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #una solo aaves en vez de los routers directamente
    app.include_router(producto_router,prefix="/api/v1")
    app.include_router(categoria_router,prefix="/api/v1")

    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    return app

app = create_app()