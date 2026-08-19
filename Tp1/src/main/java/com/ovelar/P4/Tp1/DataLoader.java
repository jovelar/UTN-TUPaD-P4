package com.ovelar.P4.Tp1;

import com.ovelar.P4.Tp1.Dto.categoria.CategoriaCreate;
import com.ovelar.P4.Tp1.Dto.categoria.CategoriaDto;
import com.ovelar.P4.Tp1.Dto.producto.ProductoCreate;
import com.ovelar.P4.Tp1.Entity.Categoria;
import com.ovelar.P4.Tp1.Entity.Producto;
import com.ovelar.P4.Tp1.service.CategoriaService;
import com.ovelar.P4.Tp1.service.ProductoService;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@RequiredArgsConstructor
@Component
public class DataLoader implements CommandLineRunner {
    private final ProductoService productoService;
    private final CategoriaService categoriaService;
    @Override
    public void run(String... args) throws Exception {

        CategoriaDto c1=categoriaService.save(new CategoriaCreate("Limpieza","Articulos de limpieza"));
        CategoriaDto c2=categoriaService.save(new CategoriaCreate("Carnes","Articulos de carne"));
        CategoriaDto c3=categoriaService.save(new CategoriaCreate("Electronicos","Articulos de electronicos"));

        

        //Producto p1=productoService.save(new ProductoCreate("Prod1","Producto 1",1200.00,400,"prod1.jpg",true));
    }
}
