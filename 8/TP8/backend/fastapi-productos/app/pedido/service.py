from datetime import datetime
from sqlmodel import Session
from app.pedido.model import Pedido, DetallePedido
from app.pedido.schema import PedidoCreate, PedidoUpdate, PedidoRead, PedidoReadConDetalles, DetallePedidoRead
from app.pedido.unit_of_work import PedidoUnitOfWork


class ProductoNoEncontrado(Exception):
    pass


class PedidoNoEncontrado(Exception):
    pass


class PedidoService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def _get_activo(self, uow: PedidoUnitOfWork, pedido_id: int) -> Pedido:
        pedido = uow.pedidos.get_activo_by_id(pedido_id)
        if pedido is None:
            raise PedidoNoEncontrado(pedido_id)
        return pedido

    def crear(self, data: PedidoCreate) -> PedidoRead:
        with PedidoUnitOfWork(self._session) as uow:
            pedido = uow.pedidos.add(Pedido(estado="PENDIENTE", total=0))
            total = 0.0
            for item in data.detalles:
                producto = uow.productos.get_by_id(item.producto_id)
                if producto is None:
                    raise ProductoNoEncontrado(item.producto_id)
                uow.detalles.add(DetallePedido(
                    pedido_id=pedido.id,
                    producto_id=producto.id,
                    cantidad=item.cantidad,
                    precio_unitario=producto.precio_base,
                ))
                total += item.cantidad * producto.precio_base
            pedido.total = total
            result = PedidoRead.model_validate(pedido)
        return result

    def listar(self) -> list[PedidoRead]:
        with PedidoUnitOfWork(self._session) as uow:
            pedidos = uow.pedidos.get_activos()
            result = [PedidoRead.model_validate(p) for p in pedidos]
        return result

    def obtener(self, pedido_id: int) -> PedidoReadConDetalles:
        with PedidoUnitOfWork(self._session) as uow:
            pedido = self._get_activo(uow, pedido_id)
            detalles = uow.detalles.get_by_pedido(pedido_id)
            result = PedidoReadConDetalles(
                id=pedido.id,
                fecha=pedido.fecha,
                estado=pedido.estado,
                total=pedido.total,
                detalles=[DetallePedidoRead.model_validate(d) for d in detalles],
            )
        return result

    def actualizar_estado(self, pedido_id: int, data: PedidoUpdate) -> PedidoRead:
        with PedidoUnitOfWork(self._session) as uow:
            pedido = self._get_activo(uow, pedido_id)
            pedido.estado = data.estado
            uow.pedidos.add(pedido)
            result = PedidoRead.model_validate(pedido)
        return result

    def eliminar(self, pedido_id: int) -> None:
        with PedidoUnitOfWork(self._session) as uow:
            pedido = self._get_activo(uow, pedido_id)
            pedido.deleted_at = datetime.now()
            uow.pedidos.add(pedido)