package com.ovelar.P4.Tp1.Entity;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;


import java.time.LocalDateTime;

@MappedSuperclass
@NoArgsConstructor
@AllArgsConstructor
@SuperBuilder
@Getter
@Setter
@ToString
public abstract class Base {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "eliminado",nullable = false)
    @Builder.Default
    private boolean eliminado = false;

    //para evitar que se pise la fecha de creacion en un update
    @Column(name = "created_at",updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void prePersist() {
        if (this.createdAt == null) {
            this.createdAt = LocalDateTime.now();
        }
    }
}
