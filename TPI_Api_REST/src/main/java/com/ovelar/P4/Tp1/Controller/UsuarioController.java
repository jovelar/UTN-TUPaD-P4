package com.ovelar.P4.Tp1.Controller;

import com.ovelar.P4.Tp1.Dto.usuario.UsuarioCreate;
import com.ovelar.P4.Tp1.Dto.usuario.UsuarioDto;
import com.ovelar.P4.Tp1.Dto.usuario.UsuarioEdit;
import com.ovelar.P4.Tp1.service.UsuarioService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/usuarios")
@RequiredArgsConstructor
public class UsuarioController {
    private final UsuarioService usuarioService;

    @PostMapping
    public UsuarioDto crear(@Valid @RequestBody UsuarioCreate usuarioCreate){
        return usuarioService.save(usuarioCreate);
    }

    @GetMapping("/{id}")
    public UsuarioDto buscarPorId(@PathVariable Long id){
        return usuarioService.findById(id);
    }

    @GetMapping
    public List<UsuarioDto> listar(){
        return usuarioService.findAll();
    }

    @PutMapping("/{id}")
    public UsuarioDto actualizar(@PathVariable Long id,
                                 @RequestBody UsuarioEdit usuarioEdit){
        return usuarioService.update(usuarioEdit,id);
    }

    @DeleteMapping("/{id}")
    public void eliminar(@PathVariable Long id){
        usuarioService.deleteById(id);
    }
}
