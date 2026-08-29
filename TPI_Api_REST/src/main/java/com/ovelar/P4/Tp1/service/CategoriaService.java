package com.ovelar.P4.Tp1.service;

import com.ovelar.P4.Tp1.Dto.categoria.CategoriaCreate;
import com.ovelar.P4.Tp1.Dto.categoria.CategoriaDto;
import com.ovelar.P4.Tp1.Dto.categoria.CategoriaEdit;

import java.util.List;

public interface CategoriaService {
    public CategoriaDto save(CategoriaCreate categoriaCreate);
    public CategoriaDto findById(Long id);
    public List<CategoriaDto> findAll();
    public CategoriaDto update(CategoriaEdit categoriaEdit, Long idCategoria);
    public void deleteById(Long id);
}
