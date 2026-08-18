package com.ovelar.P4.Tp1.Repository;

import com.ovelar.P4.Tp1.Entity.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

//Spring
@Repository
public interface ProductoRepository extends JpaRepository<Producto, Long> {
    
}