package com.ovelar.P4.Tp1.Dto.detallePedido;

import com.ovelar.P4.Tp1.Dto.producto.ProductoDto;
import com.ovelar.P4.Tp1.Entity.DetallePedido;

public record DetallePedidoDto(
        long id,
        Integer cantidad,
        Double subtotal,
        ProductoDto productoDto
) {
    public static DetallePedidoDto toDto(DetallePedido detallePedido){
        return new DetallePedidoDto(
                detallePedido.getId(),
                detallePedido.getCantidad(),
                detallePedido.getSubtotal(),
                ProductoDto.toDto(detallePedido.getProducto())
        );
    }
}