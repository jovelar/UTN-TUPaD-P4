import type { Producto } from '../types/producto'

interface ProductoCardProps {
  producto: Producto
  onEdit: (producto: Producto) => void
  onToggleDisponible: (producto: Producto) => void
  onDelete: (id: number) => void
}

function ProductoCard({ producto, onEdit, onToggleDisponible, onDelete }: ProductoCardProps) {
    const simbolo = producto.unidad_venta.simbolo
    const precio = producto.precio_base.toLocaleString('es-AR', { minimumFractionDigits: 2 })
    const stock = producto.stock_cantidad.toLocaleString('es-AR', { maximumFractionDigits: 3 })

    return (
        <div className="rounded border bg-white p-4">
        <h3 className="text-lg font-semibold">{producto.nombre}</h3>
        <p className="text-gray-600">{producto.descripcion}</p>
        <p className="mt-2 font-medium">
            $ {precio} / {simbolo}
      </p>
      <p className="text-sm text-gray-700">
        stock: {stock} {simbolo}
      </p>
      <div className="mt-2 flex gap-2 text-sm">
        <span
          className={
            producto.disponible
              ? 'rounded bg-green-100 px-2 py-1 text-green-800'
              : 'rounded bg-gray-200 px-2 py-1 text-gray-700'
          }
        >
          {producto.disponible ? 'Disponible' : 'Venta pausada'}
        </span>
        <span
          className={
            producto.hay_stock
              ? 'rounded bg-green-100 px-2 py-1 text-green-800'
              : 'rounded bg-red-100 px-2 py-1 text-red-800'
          }
        >
          {producto.hay_stock ? 'Hay stock' : 'Sin stock'}
        </span>
      </div>
      <div className="mt-4 flex gap-2">
        <button
          type="button"
          onClick={() => onEdit(producto)}
          className="rounded bg-yellow-500 px-3 py-1 text-white hover:bg-yellow-600"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onToggleDisponible(producto)}
          className="rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-700"
        >
          Disponibilidad
        </button>
        <button
          type="button"
          onClick={() => onDelete(producto.id)}
          className="rounded bg-red-600 px-3 py-1 text-white hover:bg-red-700"
        >
          Anular
        </button>
      </div>
    </div>
  )
}

export default ProductoCard