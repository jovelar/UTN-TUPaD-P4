import { useState } from 'react'
import type { ChangeEvent, FormEvent } from 'react'
import type { Producto, ProductoFormData } from '../types/producto'
import type { UnidadMedida } from '../types/unidadMedida'

interface ProductoModalProps {
  productoEditando: Producto | null
  unidades: UnidadMedida[]
  error: string | null
  guardando: boolean
  onSubmit: (data: ProductoFormData) => void
  onCancel: () => void
}

// Modal controlado: no sabe cómo se guardan los productos. Sólo recibe
// callbacks (onSubmit, onCancel) y los datos que necesita por props.
function ProductoModal({
  productoEditando,
  unidades,
  error,
  guardando,
  onSubmit,
  onCancel,
}: ProductoModalProps) {
  // Los campos numéricos se guardan como texto mientras se escriben y se
  // convierten a número recién al enviar.
  const [formState, setFormState] = useState({
    nombre: productoEditando?.nombre ?? '',
    descripcion: productoEditando?.descripcion ?? '',
    precio_base: productoEditando ? String(productoEditando.precio_base) : '',
    unidad_venta_id: productoEditando ? String(productoEditando.unidad_venta_id) : '',
    stock_cantidad: productoEditando ? String(productoEditando.stock_cantidad) : '0',
  })

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormState((prevState) => ({
      ...prevState,
      [name]: value,
    }))
  }

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    onSubmit({
      nombre: formState.nombre,
      descripcion: formState.descripcion,
      precio_base: Number(formState.precio_base),
      unidad_venta_id: Number(formState.unidad_venta_id),
      stock_cantidad: Number(formState.stock_cantidad),
      disponible: productoEditando ? productoEditando.disponible : true,
    })
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/50">
      <form className="w-full max-w-md rounded-lg bg-white p-6" onSubmit={handleSubmit}>
        <h3 className="mb-4 text-xl font-bold">
          {productoEditando ? 'Editar producto' : 'Nuevo producto'}
        </h3>
        {error && (
          <p className="mb-4 rounded bg-red-100 px-3 py-2 text-red-800">{error}</p>
        )}
        <label className="mb-4 block">
          Nombre
          <input
            name="nombre"
            value={formState.nombre}
            onChange={handleChange}
            required
            minLength={3}
            className="mt-1 w-full rounded border px-3 py-2"
          />
        </label>
        <label className="mb-4 block">
          Descripción
          <input
            name="descripcion"
            value={formState.descripcion}
            onChange={handleChange}
            className="mt-1 w-full rounded border px-3 py-2"
          />
        </label>
        <label className="mb-4 block">
          Precio
          <input
            name="precio_base"
            type="number"
            min="0"
            step="0.01"
            value={formState.precio_base}
            onChange={handleChange}
            required
            className="mt-1 w-full rounded border px-3 py-2"
          />
        </label>
        <label className="mb-4 block">
          Unidad de venta
          <select
            name="unidad_venta_id"
            value={formState.unidad_venta_id}
            onChange={handleChange}
            required
            className="mt-1 w-full rounded border px-3 py-2"
          >
            <option value="">Seleccionar...</option>
            {unidades.map((unidad) => (
              <option key={unidad.id} value={unidad.id}>
                {unidad.nombre} ({unidad.simbolo})
              </option>
            ))}
          </select>
        </label>
        <label className="mb-4 block">
          Stock
          <input
            name="stock_cantidad"
            type="number"
            min="0"
            step="0.001"
            value={formState.stock_cantidad}
            onChange={handleChange}
            required
            className="mt-1 w-full rounded border px-3 py-2"
          />
        </label>
        <div className="flex justify-end gap-2">
          <button
            type="submit"
            disabled={guardando}
            className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            Guardar
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="rounded border px-4 py-2 hover:bg-gray-100"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  )
}

export default ProductoModal
// export interface UnidadMedida {
//   id: number
//   nombre: string
//   simbolo: string
//   tipo: 'peso' | 'volumen' | 'contable'
// }