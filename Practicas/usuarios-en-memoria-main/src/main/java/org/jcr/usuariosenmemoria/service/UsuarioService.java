package org.jcr.usuariosenmemoria.service;

import lombok.RequiredArgsConstructor;
import org.jcr.usuariosenmemoria.model.Usuario;
import org.jcr.usuariosenmemoria.repository.UsuarioRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class UsuarioService {

    private final UsuarioRepository repository;

    public Usuario crearUsuario(Usuario usuario) {
        // Ejemplo de validación simple
        if (usuario.getNombre() == null || usuario.getNombre().isBlank()) {
            throw new IllegalArgumentException("El nombre no puede estar vacío");
        }
        return repository.guardar(usuario);
    }

    public List<Usuario> listarUsuarios() {
        return repository.listar();
    }

    public Optional<Usuario> buscarUsuario(Long id) {
        return repository.buscarPorId(id);
    }
}