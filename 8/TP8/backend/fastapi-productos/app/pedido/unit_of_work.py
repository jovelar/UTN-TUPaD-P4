from sqlmodel import Session
from app.core.unit_of_work import UnitOfWork
from app.pedido.repository import PedidoRepository, DetallePedidoRepository, ProductoRepository


class PedidoUnitOfWork(UnitOfWork):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self.pedidos = PedidoRepository(session)
        self.detalles = DetallePedidoRepository(session)
        self.productos = ProductoRepository(session)