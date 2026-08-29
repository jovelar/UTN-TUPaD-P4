package org.jcr.usuariosenmemoria.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.jcr.usuariosenmemoria.dto.UsuarioRequestDTO;
import org.jcr.usuariosenmemoria.dto.UsuarioResponseDTO;
import org.jcr.usuariosenmemoria.model.Usuario;
import org.jcr.usuariosenmemoria.service.UsuarioService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/usuarios")
@RequiredArgsConstructor
public class UsuarioController {

    private final UsuarioService service;

    @PostMapping
    public UsuarioResponseDTO crear(@Valid @RequestBody UsuarioRequestDTO dto) {
        return service.crearUsuario(dto);
    }

    @GetMapping
    public List<UsuarioResponseDTO> listar() {
        return service.listarUsuarios();
    }

    @GetMapping("/{id}")
    public UsuarioResponseDTO buscar(@PathVariable Long id) {
        return service.buscarUsuario(id);
    }
}
