package com.ovelar.P4.Tp1.Dto.categoria;

import com.ovelar.P4.Tp1.Entity.Categoria;

public record CategoriaCreate(String nombre,String descripcion) {

    public Categoria toEntity(){
        return Categoria.builder()
                .nombre(this.nombre)
                .descripcion(this.descripcion)
                .build();
    }
}
