package com.ovelar.P4.Tp1.service;

import com.ovelar.P4.Tp1.Dto.usuario.UsuarioCreate;
import com.ovelar.P4.Tp1.Dto.usuario.UsuarioDto;
import com.ovelar.P4.Tp1.Dto.usuario.UsuarioEdit;

import java.util.List;

public interface UsuarioService {
    public UsuarioDto save(UsuarioCreate usuarioCreate);
    public UsuarioDto findById(long id);
    public List<UsuarioDto> findAll();
    public UsuarioDto update(UsuarioEdit usuarioEdit, Long idUsuario);
    public void deleteById(Long id);
}
