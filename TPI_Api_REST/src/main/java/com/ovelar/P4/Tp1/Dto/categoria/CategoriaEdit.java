package com.ovelar.P4.Tp1.Dto.categoria;

import com.ovelar.P4.Tp1.Entity.Categoria;

public record CategoriaEdit(String nombre, String descripcion) {
    public void applyTo(Categoria categoria){
        if(this.nombre!=null){
            categoria.setNombre(this.nombre);
        }
        if(this.descripcion!=null){
            categoria.setDescripcion(this.descripcion);
        }
    }
}
