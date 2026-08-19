package com.ovelar.P4.Tp1;

import com.ovelar.P4.Tp1.Dto.categoria.CategoriaCreate;
import com.ovelar.P4.Tp1.Dto.categoria.CategoriaDto;
import com.ovelar.P4.Tp1.Dto.detallePedido.DetallePedidoCreate;
import com.ovelar.P4.Tp1.Dto.pedido.PedidoDto;
import com.ovelar.P4.Tp1.Dto.pedido.PedidoEdit;
import com.ovelar.P4.Tp1.Dto.producto.ProductoCreate;
import com.ovelar.P4.Tp1.Dto.producto.ProductoDto;
import com.ovelar.P4.Tp1.Dto.usuario.UsuarioCreate;
import com.ovelar.P4.Tp1.Dto.usuario.UsuarioDto;
import com.ovelar.P4.Tp1.Entity.Categoria;
import com.ovelar.P4.Tp1.Entity.Producto;
import com.ovelar.P4.Tp1.Entity.Usuario;
import com.ovelar.P4.Tp1.Enums.Estado;
import com.ovelar.P4.Tp1.Enums.FormaPago;
import com.ovelar.P4.Tp1.Enums.Rol;
import com.ovelar.P4.Tp1.service.CategoriaService;
import com.ovelar.P4.Tp1.service.PedidoService;
import com.ovelar.P4.Tp1.service.ProductoService;
import com.ovelar.P4.Tp1.service.UsuarioService;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;

@RequiredArgsConstructor
@Component
public class DataLoader implements CommandLineRunner {
    private final ProductoService productoService;
    private final CategoriaService categoriaService;
    public final UsuarioService usuarioService;
    public final PedidoService pedidoService;
    @Override
    public void run(String... args) throws Exception {

        CategoriaDto c1=categoriaService.save(new CategoriaCreate("Limpieza","Articulos de limpieza"));
        CategoriaDto c2=categoriaService.save(new CategoriaCreate("Carnes","Articulos de carne"));
        CategoriaDto c3=categoriaService.save(new CategoriaCreate("Electronicos","Articulos de electronicos"));

        ProductoDto p1=productoService.save(new ProductoCreate("Prod1","Producto 1",1200.00,400,"prod1.jpg",true,c1.id()));
        ProductoDto p2=productoService.save(new ProductoCreate("Prod2","Producto 2",1300.00,400,"prod2.jpg",true,c1.id()));
        ProductoDto p3=productoService.save(new ProductoCreate("Prod3","Producto 3",1310.00,400,"prod3.jpg",true,c1.id()));
        ProductoDto p4=productoService.save(new ProductoCreate("Prod4","Producto 4",1322.00,400,"prod4.jpg",true,c2.id()));
        ProductoDto p5=productoService.save(new ProductoCreate("Prod5","Producto 5",2222.00,400,"prod5.jpg",true,c2.id()));
        ProductoDto p6=productoService.save(new ProductoCreate("Prod6","Producto 6",8222.00,400,"prod6.jpg",true,c2.id()));
        ProductoDto p7=productoService.save(new ProductoCreate("Prod7","Producto 7",9222.00,400,"prod7.jpg",true,c3.id()));
        ProductoDto p8=productoService.save(new ProductoCreate("Prod8","Producto 8",5222.00,400,"prod8.jpg",true,c3.id()));
        ProductoDto p9=productoService.save(new ProductoCreate("Prod9","Producto 9",7222.00,400,"prod9.jpg",true,c3.id()));
        ProductoDto p10=productoService.save(new ProductoCreate("Prod10","Producto 10",5222.00,400,"prod10.jpg",true,c3.id()));

        UsuarioDto u1=usuarioService.save(new UsuarioCreate("Pepe", "Argento", "racingcampeon@gmail.com", "011123456", "racing10", Rol.USUARIO));
        UsuarioDto u2=usuarioService.save(new UsuarioCreate("Moni", "Argento", "boluda@gmail.com", "011123456", "pepe", Rol.USUARIO));

        // Pedido 1 — usuario u1, 2 detalles
        PedidoDto ped1 = pedidoService.save(u1.id(), FormaPago.EFECTIVO);
        pedidoService.agregarDetalle(ped1.id(), p1.id(), 2);
        pedidoService.agregarDetalle(ped1.id(), p2.id(), 1);

// Pedido 2 — usuario u2, 3 detalles
        PedidoDto ped2 = pedidoService.save(u2.id(), FormaPago.TARJETA);
        pedidoService.agregarDetalle(ped2.id(), p4.id(), 3);
        pedidoService.agregarDetalle(ped2.id(), p7.id(), 1);
        pedidoService.agregarDetalle(ped2.id(), p10.id(), 2);

// Pedido 3 — usuario u1, 2 detalles
        PedidoDto ped3 = pedidoService.save(u1.id(), FormaPago.TRANSFERENCIA);
        pedidoService.agregarDetalle(ped3.id(), p3.id(), 1);
        pedidoService.agregarDetalle(ped3.id(), p5.id(), 2);

        //Producto p1=productoService.save(new ProductoCreate("Prod1","Producto 1",1200.00,400,"prod1.jpg",true));
    }
}
