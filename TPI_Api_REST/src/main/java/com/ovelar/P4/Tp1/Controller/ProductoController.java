package com.ovelar.P4.Tp1.Controller;

import com.ovelar.P4.Tp1.Dto.producto.ProductoCreate;
import com.ovelar.P4.Tp1.Dto.producto.ProductoDto;
import com.ovelar.P4.Tp1.Dto.producto.ProductoEdit;
import com.ovelar.P4.Tp1.service.ProductoService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/productos")
@RequiredArgsConstructor
public class ProductoController {
    private final ProductoService productoService;

    @PostMapping
    public ProductoDto crear(@RequestBody ProductoCreate productoCreate){
        return productoService.save(productoCreate);
    }

    @GetMapping("/{id}")
    public ProductoDto buscarPoId(@PathVariable Long id){
        return productoService.findById(id);
    }

    @GetMapping
    public List<ProductoDto> listar(){
        return productoService.findAll();
    }
    @PutMapping("/{id}")
    public ProductoDto actualizar(@PathVariable Long id,
                                  @RequestBody ProductoEdit productoEdit){
        return productoService.update(productoEdit,id);
    }
    @DeleteMapping("/{id}")
    public void eliminar(@PathVariable Long id){
        productoService.deleteById(id);
    }
}
