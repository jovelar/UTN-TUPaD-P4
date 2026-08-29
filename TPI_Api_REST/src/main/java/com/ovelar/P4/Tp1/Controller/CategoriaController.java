package com.ovelar.P4.Tp1.Controller;

import com.ovelar.P4.Tp1.Dto.categoria.CategoriaCreate;
import com.ovelar.P4.Tp1.Dto.categoria.CategoriaDto;
import com.ovelar.P4.Tp1.Dto.categoria.CategoriaEdit;
import com.ovelar.P4.Tp1.service.CategoriaService;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/categorias")
@RequiredArgsConstructor
public class CategoriaController {
    private final CategoriaService categoriaService;

    @PostMapping
    public CategoriaDto crear(@RequestBody CategoriaCreate categoriaCreate){
        return categoriaService.save(categoriaCreate);
    }

    @GetMapping("/{id}")
    public CategoriaDto buscarPorId(@PathVariable Long id){
        return categoriaService.findById(id);
    }

    @GetMapping
    public List<CategoriaDto> listar(){
        return categoriaService.findAll();
    }

    @PutMapping("/{id}")
    public CategoriaDto actualizar(@PathVariable Long id,
                                   @RequestBody CategoriaEdit categoriaEdit){
        return categoriaService.update(categoriaEdit,id);
    }
    @DeleteMapping("/{id}")
    public void eliminar(@PathVariable Long id){
        categoriaService.deleteById(id);
    }
}
