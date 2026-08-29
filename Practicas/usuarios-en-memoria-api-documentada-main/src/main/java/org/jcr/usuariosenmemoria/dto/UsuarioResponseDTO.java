package org.jcr.usuariosenmemoria.dto;

import org.jcr.usuariosenmemoria.model.Usuario;

public record UsuarioResponseDTO(
        Long id,
        String nombre,
        String email
) {
    public static UsuarioResponseDTO fromEntity(Usuario usuario) {
        return new UsuarioResponseDTO(
                usuario.getId(),
                usuario.getNombre(),
                usuario.getEmail()
        );
    }

}
