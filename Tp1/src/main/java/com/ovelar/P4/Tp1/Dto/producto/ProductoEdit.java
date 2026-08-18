package com.ovelar.P4.Tp1.Dto.producto;

import com.ovelar.P4.Tp1.Dto.categoria.CategoriaDto;
import com.ovelar.P4.Tp1.Entity.Categoria;
import com.ovelar.P4.Tp1.Entity.Producto;

public record ProductoEdit(
        String nombre,
        String descripcion,
        Double precio,
        Integer stock,
        String imagen,
        Boolean disponible,
        long idCategoria
) {

    //Solo se aceptan los parametros nuevos, se valida primero si el valor de reemplazo no es null
    // antes de aplicar
    public void applyTo(Producto producto,Categoria categoria) {
        if (this.nombre != null) {
            producto.setNombre(this.nombre);
        }
        if (this.descripcion != null) {
            producto.setDescripcion(this.descripcion);
        }
        if (this.precio != null) {
            producto.setPrecio(this.precio);
        }
        if (this.stock != null) {
            producto.setStock(this.stock);
        }
        if(this.imagen!=null){
            producto.setImagen(this.imagen);
        }
        if(this.disponible!=null){
            producto.setDisponible(this.disponible);
        }
        if(categoria!=null){
            producto.setCategoria(categoria);
        }
    }
}
