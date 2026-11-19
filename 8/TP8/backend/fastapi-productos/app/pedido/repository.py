from sqlmodel import Session, select
from app.core.repository import BaseRepository
from app.pedido.model import Pedido, DetallePedido
from app.producto.model import Producto


class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Pedido)

    def get_activos(self) -> list[Pedido]:
        return list(
            self.session.exec(
                select(Pedido).where(Pedido.deleted_at == None)
            ).all()
        )

    def get_activo_by_id(self, pedido_id: int) -> Pedido | None:
        return self.session.exec(
            select(Pedido).where(Pedido.id == pedido_id, Pedido.deleted_at == None)
        ).first()


class DetallePedidoRepository(BaseRepository[DetallePedido]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DetallePedido)

    def get_by_pedido(self, pedido_id: int) -> list[DetallePedido]:
        return list(
            self.session.exec(
                select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
            ).all()
        )


class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Producto)