package org.jcr.usuariosenmemoria.service;

import lombok.RequiredArgsConstructor;
import org.jcr.usuariosenmemoria.dto.UsuarioRequestDTO;
import org.jcr.usuariosenmemoria.dto.UsuarioResponseDTO;
import org.jcr.usuariosenmemoria.model.Usuario;
import org.jcr.usuariosenmemoria.repository.UsuarioRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UsuarioService {

    private final UsuarioRepository repository;

    public UsuarioResponseDTO crearUsuario(UsuarioRequestDTO usuario) {
        // Ejemplo de validación simple
        if (usuario.nombre() == null || usuario.nombre().isBlank()) {
            throw new IllegalArgumentException("El nombre no puede estar vacío");
        }
        Usuario usuarioCreado = Usuario.builder().nombre(usuario.nombre()).email(usuario.email()).password(usuario.password()).build();
        return UsuarioResponseDTO.fromEntity(repository.save(usuarioCreado));
    }

    public List<UsuarioResponseDTO> listarUsuarios() {
        return repository.findAll()
                .stream()
                .map(UsuarioResponseDTO::fromEntity)
                .toList();
    }

    public UsuarioResponseDTO buscarUsuario(Long id) {
        Usuario usuario = repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("No existe un usuario con el ID " + id));
        return UsuarioResponseDTO.fromEntity(usuario);
    }

}