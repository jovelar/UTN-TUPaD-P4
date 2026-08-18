package com.ovelar.P4.Tp1.Entity;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "categorias")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@SuperBuilder
@ToString(callSuper = true, exclude = {"productos"})
@EqualsAndHashCode(callSuper = false, onlyExplicitlyIncluded = true)
public class Categoria extends Base {

    @EqualsAndHashCode.Include
    @Column(name = "nombre", nullable = false, unique = true, length = 100)
    private String nombre;

    @Column(name = "descripcion", length = 500)
    private String descripcion;

    @OneToMany(mappedBy = "categoria", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @Builder.Default
    private Set<Producto> productos = new HashSet<>();

    //Ya esta definido en Base.java
    //@Builder.Default
    //private Boolean eliminado=false;

    public void addProducto(Producto producto) {
        if (!productos.add(producto)) {
            throw new IllegalArgumentException("Producto ya cargado en la categoría");
        }
    }
}
