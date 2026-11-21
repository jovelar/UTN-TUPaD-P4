from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.producto.model import Producto, ProductoCategoria
from app.categoria.model import Categoria
from app.producto.router import router as producto_router
from app.categoria.router import router as categoria_router
from app.pedido.model import Pedido, DetallePedido   


def create_app() -> FastAPI:
    app = FastAPI(title="API Productos y Categorías", version="1.0.0")
    app.include_router(pedido_router)
    app.include_router(ingrediente_router)  

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(pedido_router)
    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(ingrediente_router)

    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    return app

app = create_app()