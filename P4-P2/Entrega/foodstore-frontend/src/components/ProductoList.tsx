import type { Producto } from '../types/producto'
import ProductoCard from './ProductoCard'

interface ProductoListProps {
  productos: Producto[]
  onEdit: (producto: Producto) => void
  onToggleDisponible: (producto: Producto) => void
  onDelete: (id: number) => void
}

function ProductoList({ productos, onEdit, onToggleDisponible, onDelete }: ProductoListProps) {
  return (
    <div className="grid gap-4">
      {productos.map((producto) => (
        <ProductoCard
          key={producto.id}
          producto={producto}
          onEdit={onEdit}
          onToggleDisponible={onToggleDisponible}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}

export default ProductoList