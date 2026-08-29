package com.ovelar.P4.Tp1.Dto.producto;

import com.ovelar.P4.Tp1.Entity.Categoria;
import com.ovelar.P4.Tp1.Entity.Producto;

public record ProductoCreate(
        String nombre,
        String descripcion,
        Double precio,
        int stock,
        String imagen,
        Boolean disponible,
        long idCategoria
) {
    public Producto toEntity(Categoria categoria){
        return Producto.builder()
                .nombre(this.nombre)
                .precio(this.precio)
                .descripcion(this.descripcion)
                .stock(this.stock)
                .disponible(this.disponible)
                .categoria(categoria)
                .build();
    }
}
