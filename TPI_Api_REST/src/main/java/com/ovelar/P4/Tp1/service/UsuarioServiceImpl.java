package com.ovelar.P4.Tp1.service;

import com.ovelar.P4.Tp1.Dto.usuario.UsuarioCreate;
import com.ovelar.P4.Tp1.Dto.usuario.UsuarioDto;
import com.ovelar.P4.Tp1.Dto.usuario.UsuarioEdit;
import com.ovelar.P4.Tp1.Entity.Usuario;
import com.ovelar.P4.Tp1.Repository.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UsuarioServiceImpl implements  UsuarioService {

    private final UsuarioRepository usuarioRepository;

    @Override
    public UsuarioDto save(UsuarioCreate usuarioCreate) {
        Usuario usuario = usuarioCreate.toEntity();
        usuario = usuarioRepository.save(usuario);
        return UsuarioDto.toDto(usuario);
    }

    @Override
    public UsuarioDto findById(long id) {
        Usuario usuario = usuarioRepository.findById(id).orElseThrow(()->new NullPointerException("No se encontro usuario con el id "+id));
        return UsuarioDto.toDto(usuario);
    }
    public UsuarioDto findByMail(String mail) {
        Usuario usuario = usuarioRepository.findByMail(mail).orElseThrow(()->new NullPointerException("No se encontro usuario con el email "+mail));
        return UsuarioDto.toDto(usuario);
    }

    @Override
    public List<UsuarioDto> findAll() {
        List<Usuario> usuarios = usuarioRepository.findAll();
        return usuarios.stream().map(UsuarioDto::toDto).toList();
    }

    @Override
    public UsuarioDto update(UsuarioEdit usuarioEdit, Long idUsuario) {
        Usuario usuario = usuarioRepository.findById(idUsuario)
                .orElseThrow(() -> new NullPointerException("No se encontro usuario con el id " + idUsuario));
        usuarioEdit.applyTo(usuario);
        usuario = usuarioRepository.save(usuario);
        return UsuarioDto.toDto(usuario);
    }

    @Override
    public void deleteById(Long id) {
        Usuario usuario = usuarioRepository.findById(id).orElseThrow(()-> new NullPointerException("No se encontro producto con el id "+id));
        usuario.setEliminado(true);
        usuarioRepository.save(usuario);

    }

}
