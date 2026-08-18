package com.ovelar.P4.Tp1.Dto.detallePedido;

import com.ovelar.P4.Tp1.Entity.DetallePedido;
import com.ovelar.P4.Tp1.Entity.Producto;

public record DetallePedidoCreate(Integer cantidad,
                                  Double subtotal,
                                  long idProducto) {
    public DetallePedido toEntity(Producto producto){
        return DetallePedido.builder()
                .cantidad(this.cantidad)
                .producto(producto)
                .subtotal(this.subtotal)
                .build();
    }
}
