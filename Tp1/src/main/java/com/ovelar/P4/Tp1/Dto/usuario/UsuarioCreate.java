package com.ovelar.P4.Tp1.Dto.usuario;

import com.ovelar.P4.Tp1.Entity.Usuario;
import com.ovelar.P4.Tp1.Enums.Rol;

public record UsuarioCreate(String nombre,
                            String apellido,
                            String mail,
                            String celular,
                            String contrasena,
                            Rol rol) {
    public Usuario toEntity(){
        return Usuario.builder().nombre(this.nombre)
                .apellido(this.apellido)
                .mail(this.mail())
                .celular(this.celular)
                .contraseña(this.contrasena)
                .rol(this.rol)
                .build();
    }
}
