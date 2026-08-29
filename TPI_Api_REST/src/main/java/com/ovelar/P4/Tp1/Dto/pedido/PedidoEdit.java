package com.ovelar.P4.Tp1.Dto.pedido;

import com.ovelar.P4.Tp1.Entity.Pedido;
import com.ovelar.P4.Tp1.Enums.Estado;
import com.ovelar.P4.Tp1.Enums.FormaPago;

public record PedidoEdit(Estado estado, FormaPago formaPago) {
    public void applyTo(Pedido pedido){
        if (this.estado != null) {
            pedido.setEstado(this.estado);
        }
        if (this.formaPago != null) {
            pedido.setFormaPago(this.formaPago);
        }
    }
}