package com.ovelar.P4.Tp1.Dto.pedido;

import com.ovelar.P4.Tp1.Entity.Pedido;
import com.ovelar.P4.Tp1.Enums.Estado;
import com.ovelar.P4.Tp1.Enums.FormaPago;

import java.time.LocalDate;

public record PedidoDto(
        long id,
        LocalDate fecha,
        Estado estado,
        Double total,
        FormaPago formaPago
) {
    public static PedidoDto toDto(Pedido pedido){
        return new PedidoDto(pedido.getId(), pedido.getFecha(), pedido.getEstado(), pedido.getTotal(), pedido.getFormaPago());
    }
}