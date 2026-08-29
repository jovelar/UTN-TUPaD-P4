package com.ovelar.P4.Tp1.Entity;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;
import org.hibernate.annotations.SQLRestriction;

@Entity
@Table(name = "detalles_pedido")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@SuperBuilder
@ToString(callSuper = true)
//Por si se da la baja logica
@SQLRestriction("eliminado = false")
@EqualsAndHashCode(callSuper = false, onlyExplicitlyIncluded = true)
public class DetallePedido extends Base {

    @Column(name = "cantidad",nullable = false)
    private Integer cantidad;

    @Column(name = "subtotal", nullable = false)
    private Double subtotal;

    @EqualsAndHashCode.Include
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "producto_id",nullable = false)
    private com.ovelar.P4.Tp1.Entity.Producto producto;

    public void calcularSubtotal() {
        if (this.producto != null && this.cantidad != null) {
            this.subtotal = this.producto.getPrecio() * this.cantidad;
        }
    }
}
