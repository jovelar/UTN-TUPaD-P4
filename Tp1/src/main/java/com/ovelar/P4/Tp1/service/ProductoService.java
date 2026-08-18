package com.ovelar.P4.Tp1.service;

import com.ovelar.P4.Tp1.Dto.producto.ProductoCreate;
import com.ovelar.P4.Tp1.Dto.producto.ProductoDto;
import com.ovelar.P4.Tp1.Dto.producto.ProductoEdit;

import java.util.List;

public interface ProductoService {
    public ProductoDto save(ProductoCreate productoCreate);
    public ProductoDto findById(long id);
    public List<ProductoDto> findAll();
    public ProductoDto update(ProductoEdit productoEdit, Long idProducto);
    public void deleteById(Long id);
}
