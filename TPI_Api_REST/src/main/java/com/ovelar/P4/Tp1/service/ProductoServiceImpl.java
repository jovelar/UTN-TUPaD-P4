package com.ovelar.P4.Tp1.service;

import com.ovelar.P4.Tp1.Dto.producto.ProductoCreate;
import com.ovelar.P4.Tp1.Dto.producto.ProductoDto;
import com.ovelar.P4.Tp1.Dto.producto.ProductoEdit;
import com.ovelar.P4.Tp1.Entity.Categoria;
import com.ovelar.P4.Tp1.Entity.Producto;
import com.ovelar.P4.Tp1.Repository.CategoriaRepository;
import com.ovelar.P4.Tp1.Repository.ProductoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
@RequiredArgsConstructor
public class ProductoServiceImpl implements  ProductoService {

    private final ProductoRepository productoRepository;
    private final CategoriaRepository categoriaRepository;

    @Override
    public ProductoDto save(ProductoCreate productoCreate) {
        Categoria categoria = categoriaRepository.findById(productoCreate.idCategoria()).orElseThrow(()-> new NullPointerException("No se encontro categoria con el id "+productoCreate.idCategoria()));
        Producto producto = productoCreate.toEntity(categoria);
        producto = productoRepository.save(producto);
        return ProductoDto.toDto(producto);
    }

    @Override
    public ProductoDto findById(long id) {
        Producto producto = productoRepository.findById(id).orElseThrow(()->new NullPointerException("No se encontro producto con el id "+id));

        return ProductoDto.toDto(producto);
    }

    @Override
    public List<ProductoDto> findAll() {
        List<Producto> productos = productoRepository.findAll();
        return productos.stream().map(ProductoDto::toDto).toList();
    }

    @Override
    public ProductoDto update(ProductoEdit productoEdit, Long idProducto) {
        Producto producto = productoRepository.findById(idProducto).orElseThrow(()-> new NullPointerException("No se encontro producto con el id "+idProducto));
        Categoria categoria = null;
        if(productoEdit.idCategoria()!=null){
            categoria=categoriaRepository.findById(productoEdit.idCategoria()).orElseThrow(()-> new NullPointerException("No se encontro categoria con el id "+productoEdit.idCategoria()));
        }
        productoEdit.applyTo(producto,categoria);
        producto=productoRepository.save(producto);
        return ProductoDto.toDto(producto);
    }

    @Override
    public void deleteById(Long id) {
        Producto producto = productoRepository.findById(id).orElseThrow(()-> new NullPointerException("No se encontro producto con el id "+id));
        producto.setEliminado(true);
        productoRepository.save(producto);
    }
}
