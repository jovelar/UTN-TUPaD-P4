from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import SessionDep
from app.pedido.schema import PedidoCreate, PedidoUpdate, PedidoRead, PedidoReadConDetalles
from app.pedido.service import PedidoService, PedidoNoEncontrado, ProductoNoEncontrado

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


def get_pedido_service(session: SessionDep) -> PedidoService:
    return PedidoService(session)


@router.post("/", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear_pedido(data: PedidoCreate, svc: PedidoService = Depends(get_pedido_service)):
    try:
        return svc.crear(data)
    except ProductoNoEncontrado as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con id={e} no encontrado")


@router.get("/", response_model=List[PedidoRead])
def listar_pedidos(svc: PedidoService = Depends(get_pedido_service)):
    return svc.listar()


@router.get("/{pedido_id}", response_model=PedidoReadConDetalles)
def obtener_pedido(pedido_id: int, svc: PedidoService = Depends(get_pedido_service)):
    try:
        return svc.obtener(pedido_id)
    except PedidoNoEncontrado as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido con id={e} no encontrado")


@router.put("/{pedido_id}", response_model=PedidoRead)
def actualizar_pedido(pedido_id: int, data: PedidoUpdate, svc: PedidoService = Depends(get_pedido_service)):
    try:
        return svc.actualizar_estado(pedido_id, data)
    except PedidoNoEncontrado as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido con id={e} no encontrado")


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pedido(pedido_id: int, svc: PedidoService = Depends(get_pedido_service)):
    try:
        svc.eliminar(pedido_id)
    except PedidoNoEncontrado as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido con id={e} no encontrado")