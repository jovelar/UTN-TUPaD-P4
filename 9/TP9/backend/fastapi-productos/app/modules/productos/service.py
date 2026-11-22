"""
Service de Producto — lógica de negocio.

Stateless, orquesta operaciones sobre los repositorios a través del UoW.
Lanza HTTPException. No hace commit/rollback directamente.

Capa: Service
Conoce a: UoW, Repository (indirectamente vía UoW)
NO conoce a: Router

Regla de imports:
    Router → Service → UoW → Repository → Model
"""

from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.modules.productos.model import (
    Producto, ProductoCategoria, ProductoCreate, ProductoUpdate,
    ProductoCategoriaCreate, ProductoPublic,
)


class ProductoService:
    """Lógica de negocio para CRUD de productos y sus categorías."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def _to_public(self, producto: Producto) -> ProductoPublic:
        return ProductoPublic.model_validate(
            producto,
            update={
                "imagenes_url": producto.imagenes_url or [],
                "categorias": self.uow.productos.get_categorias(producto.id),
            },
        )

    def _get_or_404(self, producto_id: int) -> Producto:
        producto = self.uow.productos.get_by_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )
        return producto

    def list_all(self) -> list[ProductoPublic]:
        """Lista todos los productos."""
        return [self._to_public(p) for p in self.uow.productos.get_all()]

    def get_by_id(self, producto_id: int) -> ProductoPublic:
        """Obtiene un producto por ID o lanza 404."""
        return self._to_public(self._get_or_404(producto_id))

    def create(self, prod_in: ProductoCreate) -> ProductoPublic:
        """Crea un nuevo producto."""
        producto = Producto.model_validate(prod_in)
        return self._to_public(self.uow.productos.add(producto))

    def update(self, producto_id: int, prod_in: ProductoUpdate) -> ProductoPublic:
        """Actualización parcial de un producto."""
        producto = self._get_or_404(producto_id)

        for key, value in prod_in.model_dump(exclude_unset=True).items():
            setattr(producto, key, value)

        return self._to_public(self.uow.productos.update(producto))

    def delete(self, producto_id: int) -> None:
        """Borrado lógico: completa deleted_at o lanza 404."""
        producto = self._get_or_404(producto_id)
        producto.deleted_at = datetime.now(timezone.utc)
        self.uow.productos.update(producto)

    def asignar_categoria(self, producto_id: int, data: ProductoCategoriaCreate) -> ProductoPublic:
        """Asigna una categoría al producto (fila en ProductoCategoria)."""
        producto = self._get_or_404(producto_id)

        if not self.uow.categorias.get_by_id(data.categoria_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )

        if self.uow.productos.get_vinculo(producto_id, data.categoria_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El producto ya tiene esa categoría",
            )

        self.uow.productos.add_vinculo(ProductoCategoria(
            producto_id=producto_id,
            categoria_id=data.categoria_id,
            es_principal=data.es_principal,
        ))
        return self._to_public(producto)

    def quitar_categoria(self, producto_id: int, categoria_id: int) -> None:
        """Quita una categoría del producto: borra la fila de enlace."""
        self._get_or_404(producto_id)

        vinculo = self.uow.productos.get_vinculo(producto_id, categoria_id)
        if not vinculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El producto no tiene esa categoría",
            )
        self.uow.productos.delete_vinculo(vinculo)