package com.ovelar.P4.Tp1.Dto.usuario;

import com.ovelar.P4.Tp1.Entity.Usuario;
import com.ovelar.P4.Tp1.Enums.Rol;

public record UsuarioDto(
        long id,
        String nombre,
        String apellido,
        String mail,
        String celular,
        Rol rol) {
    public static UsuarioDto toDto(Usuario usuario){
        return new UsuarioDto(
                usuario.getId(),
                usuario.getNombre(),
                usuario.getApellido(),
                usuario.getMail(),
                usuario.getCelular(),
                usuario.getRol());
    }
}
