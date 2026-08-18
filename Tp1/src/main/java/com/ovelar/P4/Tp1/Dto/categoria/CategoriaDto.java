package com.ovelar.P4.Tp1.Dto.categoria;

import com.ovelar.P4.Tp1.Entity.Categoria;

public record CategoriaDto(long id, String nombre, String descripcion) {
    public static CategoriaDto toDto(Categoria categoria){
        return new CategoriaDto(categoria.getId(),
                categoria.getNombre(),
                categoria.getDescripcion());
    }
}
