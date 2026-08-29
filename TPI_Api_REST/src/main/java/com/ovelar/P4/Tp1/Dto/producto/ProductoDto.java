package com.ovelar.P4.Tp1.Dto.producto;

import com.ovelar.P4.Tp1.Dto.categoria.CategoriaDto;
import com.ovelar.P4.Tp1.Entity.Producto;

public record ProductoDto(
        long id,
        String nombre,
        String descripcion,
        Double precio,
        int stock,
        String imagen,
        Boolean disponible,
        CategoriaDto categoriaDto
) {
    public static ProductoDto toDto(Producto producto){
        return new ProductoDto(producto.getId(),
                producto.getNombre(),
                producto.getDescripcion(),
                producto.getPrecio(),
                producto.getStock(),
                producto.getImagen(),
                producto.getDisponible(),
                producto.getCategoria()!= null ? CategoriaDto.toDto(producto.getCategoria()) : null
        );
    }
}
