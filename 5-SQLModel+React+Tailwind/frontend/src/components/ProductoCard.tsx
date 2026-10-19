import type { Producto } from '../types/producto'

interface ProductoCardProps {
  producto: Producto
}

export const ProductoCard = ({ producto }: ProductoCardProps) => {
  return (
    <div className="bg-white rounded-lg shadow p-6 flex flex-col gap-2">
      <h3 className="text-xl font-semibold text-gray-900">{producto.nombre}</h3>
      <p className="text-sm text-gray-700">{producto.descripcion}</p>
      <p className="text-lg font-bold text-blue-700">$ {producto.precio}</p>
    </div>
  )
}