import type { Producto } from '../types/producto'
import { ProductoCard } from './ProductoCard'

interface ProductoListProps {
  productos: Producto[]
}

export const ProductoList = ({ productos }: ProductoListProps) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {productos.map((producto) => (
        <ProductoCard key={producto.id} producto={producto} />
      ))}
    </div>
  )
}