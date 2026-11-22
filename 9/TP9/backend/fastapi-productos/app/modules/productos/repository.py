"""
Repositorio de Producto.

Acceso a BD: queries sin lógica de negocio.
Hereda de BaseRepository[Producto] y agrega queries específicas.

Capa: Repository
Conoce a: Model (Producto, ProductoCategoria, Categoria), Session
NO conoce a: Service, Router
"""

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.categorias.model import Categoria
from app.modules.productos.model import Producto, ProductoCategoria, CategoriaAsignada


class ProductoRepository(BaseRepository[Producto]):

    def __init__(self, session: Session):
        super().__init__(Producto, session)

    # Borrado lógico: solo registros con deleted_at nulo
    def get_by_id(self, entity_id: int) -> Producto | None:
        producto = self.session.get(Producto, entity_id)
        if producto is None or producto.deleted_at is not None:
            return None
        return producto

    def get_all(self) -> list[Producto]:
        return list(self.session.exec(
            select(Producto).where(Producto.deleted_at == None).order_by(Producto.id)  # noqa: E711
        ).all())

    def get_categorias(self, producto_id: int) -> list[CategoriaAsignada]:
        filas = self.session.exec(
            select(Categoria.id, Categoria.nombre, ProductoCategoria.es_principal)
            .join(ProductoCategoria, ProductoCategoria.categoria_id == Categoria.id)
            .where(
                ProductoCategoria.producto_id == producto_id,
                Categoria.deleted_at == None,  # noqa: E711
            )
            .order_by(Categoria.nombre)
        ).all()
        return [CategoriaAsignada(id=f[0], nombre=f[1], es_principal=f[2]) for f in filas]

    def get_vinculo(self, producto_id: int, categoria_id: int) -> ProductoCategoria | None:
        return self.session.get(ProductoCategoria, (producto_id, categoria_id))

    def add_vinculo(self, vinculo: ProductoCategoria) -> ProductoCategoria:
        self.session.add(vinculo)
        self.session.flush()
        return vinculo

    def delete_vinculo(self, vinculo: ProductoCategoria) -> None:
        self.session.delete(vinculo)
        self.session.flush()