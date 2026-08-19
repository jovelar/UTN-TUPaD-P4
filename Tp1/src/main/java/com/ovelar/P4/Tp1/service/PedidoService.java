package com.ovelar.P4.Tp1.service;

import com.ovelar.P4.Tp1.Dto.pedido.PedidoDto;
import com.ovelar.P4.Tp1.Dto.pedido.PedidoEdit;
import com.ovelar.P4.Tp1.Enums.FormaPago;

import java.util.List;

public interface PedidoService {
    public PedidoDto save(Long idUsuario, FormaPago formaPago);
    public PedidoDto findById(long id);
    public List<PedidoDto> findAll();
    public PedidoDto update(PedidoEdit pedidoEdit, Long idPedido);
    public void deleteById(Long id);
    public PedidoDto agregarDetalle(Long idPedido, Long idProducto, int cantidad);
    public PedidoDto eliminarDetalle(Long idPedido, Long idProducto);
}