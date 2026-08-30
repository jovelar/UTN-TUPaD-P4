package com.ovelar.P4.Tp1.Repository;

import com.ovelar.P4.Tp1.Entity.Categoria;
import com.ovelar.P4.Tp1.Entity.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
 public interface UsuarioRepository extends JpaRepository<Usuario,Long> {
  Optional<Usuario>findByMail(String mail);
}
