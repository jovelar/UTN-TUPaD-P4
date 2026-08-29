package com.ovelar.endpointTest.EndpointTest1;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/endpointTest")
public class SaludoController {

    //postman http://localhost:8080/saludo_1
    @GetMapping("/saludo_1")
    public String respuesta1(){
        return "Respuesta1!";
    }

    //postman http://localhost:8080/saludo_2
    @GetMapping("/saludo_2")
    public String respuesta2(){
        return "Respuesta2!";
    }

    @PostMapping()
    public String agregar(){
        return "Recurso agregado!";
    }


    @PutMapping("/{id}")
    public String actualizar(@PathVariable Long id){
        return "PUT acepta recurso "+id;
    }

    @DeleteMapping("/{id}")
    public String borrar(@PathVariable Long id){
        return "DELETE de recurso :"+id;
    }
}
