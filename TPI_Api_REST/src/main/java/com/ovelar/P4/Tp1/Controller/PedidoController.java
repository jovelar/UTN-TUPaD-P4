package com.ovelar.P4.Tp1.Controller;

import com.ovelar.P4.Tp1.Dto.categoria.CategoriaDto;
import com.ovelar.P4.Tp1.Dto.pedido.PedidoDto;
import com.ovelar.P4.Tp1.Dto.pedido.PedidoEdit;
import com.ovelar.P4.Tp1.Enums.FormaPago;
import com.ovelar.P4.Tp1.service.PedidoService;
import lombok.AllArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/pedidos")
@RequiredArgsConstructor
public class PedidoController {
    private final PedidoService pedidoService;

    @PostMapping
    public PedidoDto crear(@RequestParam Long idUsuario,
                           @RequestParam FormaPago formaPago){
        return pedidoService.save(idUsuario,formaPago);
    }

    @GetMapping("/{id}")
    public PedidoDto buscarPorId(@PathVariable Long id){
        return pedidoService.findById(id);
    }

    @GetMapping
    public List<PedidoDto> listar(){
        return pedidoService.findAll();
    }

    @PutMapping("/{id}")
    public PedidoDto actualizar(@PathVariable Long id,
                                @RequestBody PedidoEdit pedidoEdit){
        return pedidoService.update(pedidoEdit,id);
    }

    @DeleteMapping("/{id}")
        public void eliminar(@PathVariable Long id){
            pedidoService.deleteById(id);
        }
    @PostMapping("/{id}/detalles")
    public PedidoDto agregarDetalle(@PathVariable Long id,
                                    @RequestParam Long idProducto,
                                    @RequestParam int cantidad) {
        return pedidoService.agregarDetalle(id, idProducto, cantidad);
    }

    @DeleteMapping("/{id}/detalles/{idProducto}")
    public PedidoDto eliminarDetalle(@PathVariable Long id,
                                     @PathVariable Long idProducto) {
        return pedidoService.eliminarDetalle(id, idProducto);
    }
    }

