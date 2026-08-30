package com.ovelar.P4.Tp1.service;

import com.ovelar.P4.Tp1.Dto.pedido.PedidoDto;
import com.ovelar.P4.Tp1.Dto.pedido.PedidoEdit;
import com.ovelar.P4.Tp1.Entity.Pedido;
import com.ovelar.P4.Tp1.Entity.Producto;
import com.ovelar.P4.Tp1.Entity.Usuario;
import com.ovelar.P4.Tp1.Enums.FormaPago;
import com.ovelar.P4.Tp1.Repository.PedidoRepository;
import com.ovelar.P4.Tp1.Repository.ProductoRepository;
import com.ovelar.P4.Tp1.Repository.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PedidoServiceImpl implements PedidoService {

    private final PedidoRepository pedidoRepository;
    private final UsuarioRepository usuarioRepository;
    private final ProductoRepository productoRepository;

    @Override
    public PedidoDto save(Long idUsuario, FormaPago formaPago) {
        Usuario usuario = usuarioRepository.findById(idUsuario)
                .orElseThrow(() -> new NullPointerException("No se encontro usuario con el id " + idUsuario));

        Pedido pedido = Pedido.builder()
                .formaPago(formaPago)
                .build();

        pedido = pedidoRepository.save(pedido);

        usuario.addPedido(pedido);
        usuarioRepository.save(usuario);

        return PedidoDto.toDto(pedido);
    }

    @Override
    public PedidoDto findById(long id) {
        Pedido pedido = pedidoRepository.findById(id)
                .orElseThrow(() -> new NullPointerException("No se encontro pedido con el id " + id));
        return PedidoDto.toDto(pedido);
    }

    @Override
    public List<PedidoDto> findAll() {
        List<Pedido> pedidos = pedidoRepository.findAll();
        return pedidos.stream().map(PedidoDto::toDto).toList();
    }

    @Override
    public PedidoDto update(PedidoEdit pedidoEdit, Long idPedido) {
        Pedido pedido = pedidoRepository.findById(idPedido)
                .orElseThrow(() -> new NullPointerException("No se encontro pedido con el id " + idPedido));
        pedidoEdit.applyTo(pedido);
        pedido = pedidoRepository.save(pedido);
        return PedidoDto.toDto(pedido);
    }

    @Override
    public void deleteById(Long id) {
        Pedido pedido = pedidoRepository.findById(id)
                .orElseThrow(() -> new NullPointerException("No se encontro pedido con el id " + id));
        pedido.setEliminado(true);
        pedidoRepository.save(pedido);
    }

    @Override
    public PedidoDto agregarDetalle(Long idPedido, Long idProducto, int cantidad) {
        Pedido pedido = pedidoRepository.findById(idPedido)
                .orElseThrow(() -> new NullPointerException("No se encontro pedido con el id " + idPedido));
        Producto producto = productoRepository.findById(idProducto)
                .orElseThrow(() -> new NullPointerException("No se encontro producto con el id " + idProducto));

        pedido.addDetallePedido(cantidad, producto);
        pedido = pedidoRepository.save(pedido);

        return PedidoDto.toDto(pedido);
    }

    @Override
    public PedidoDto eliminarDetalle(Long idPedido, Long idProducto) {
        Pedido pedido = pedidoRepository.findById(idPedido)
                .orElseThrow(() -> new NullPointerException("No se encontro pedido con el id " + idPedido));
        Producto producto = productoRepository.findById(idProducto)
                .orElseThrow(() -> new NullPointerException("No se encontro producto con el id " + idProducto));

        pedido.deleteDetallePedidoByProducto(producto);
        pedido = pedidoRepository.save(pedido);

        return PedidoDto.toDto(pedido);
    }
}