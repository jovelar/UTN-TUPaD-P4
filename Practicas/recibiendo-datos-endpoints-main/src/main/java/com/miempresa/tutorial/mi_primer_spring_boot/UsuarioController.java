package com.miempresa.tutorial.mi_primer_spring_boot;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/usuarios")
public class UsuarioController {

    // Ejemplo 1: @PathVariable
    @GetMapping("/{id}")
    public Map<String, Object> obtenerPorId(@PathVariable Long id) {
        Map<String, Object> respuesta = new HashMap<>();
        respuesta.put("id", id);
        respuesta.put("nombre", "Usuario " + id);
        return respuesta;
    }

    // Ejemplo 2: @RequestParam
    @GetMapping
    public Map<String, Object> filtrar(@RequestParam(required = false) String categoria,
                                       @RequestParam(defaultValue = "0") int pagina) {
        Map<String, Object> respuesta = new HashMap<>();
        respuesta.put("categoria", categoria);
        respuesta.put("pagina", pagina);
        respuesta.put("resultados", Arrays.asList("item1", "item2"));
        return respuesta;
    }

    // Ejemplo 3: @RequestBody
    @PostMapping
    public Map<String, Object> crear(@RequestBody Map<String, Object> nuevoUsuario) {
        Map<String, Object> respuesta = new HashMap<>();
        respuesta.put("mensaje", "Usuario creado con éxito");
        respuesta.put("datos", nuevoUsuario);
        return respuesta;
    }
}

