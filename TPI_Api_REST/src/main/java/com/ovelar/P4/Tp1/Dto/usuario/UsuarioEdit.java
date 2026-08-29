package com.ovelar.P4.Tp1.Dto.usuario;

import com.ovelar.P4.Tp1.Entity.Usuario;

public record UsuarioEdit(String nombre,
                          String apellido,
                          String mail,
                          String celular,
                          String contrasena){
    public void applyTo(Usuario usuario){
        if(this.nombre!=null){
            usuario.setNombre(this.nombre);
        }
        if(this.apellido!=null){
            usuario.setApellido(this.apellido);
        }
        if(this.mail!=null){
            usuario.setMail(this.mail);
        }
        if(this.celular!=null){
            usuario.setCelular(this.celular);
        }
        if(this.contrasena!=null){
            usuario.setContraseña(this.contrasena);
        }
    }
}
