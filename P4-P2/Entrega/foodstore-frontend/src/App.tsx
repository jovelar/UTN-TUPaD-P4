import { useEffect, useState } from 'react'
import Navbar from './components/Navbar'
import ProductoList from './components/ProductoList'
import ProductoModal from './components/ProductoModal'
import type { Producto, ProductoFormData } from './types/producto'
import type { UnidadMedida } from './types/unidadMedida'

const API_URL = 'http://localhost:8000/api/v1'

// Lee el mensaje de error que devuelve la API en {"detail": "..."}
const leerError = async (response: Response) => {
  const body: { detail: string | { msg: string }[] } = await response.json()
  if (typeof body.detail === 'string') {
    return body.detail
  }
  return body.detail.map((item) => item.msg).join('. ')
}

function App() {
  const [productos, setProductos] = useState<Producto[]>([])
  const [unidades, setUnidades] = useState<UnidadMedida[]>([])
  const [modalAbierto, setModalAbierto] = useState(false)
  const [productoEditando, setProductoEditando] = useState<Producto | null>(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [errorModal, setErrorModal] = useState<string | null>(null)
  const [guardando, setGuardando] = useState(false)

  const cargarProductos = async () => {
    const response = await fetch(`${API_URL}/productos?limit=50`)
    if (!response.ok) {
      throw new Error('No se pudieron cargar los productos')
    }
    const data: Producto[] = await response.json()
    setProductos(data)
  }

  const cargarUnidades = async () => {
    const response = await fetch(`${API_URL}/unidades-medida`)
    if (!response.ok) {
      throw new Error('No se pudieron cargar las unidades de medida')
    }
    const data: UnidadMedida[] = await response.json()
    setUnidades(data)
  }

  useEffect(() => {
    const cargarDatos = async () => {
      try {
        await cargarProductos()
        await cargarUnidades()
      } catch {
        setError('No se pudo conectar con la API')
      } finally {
        setCargando(false)
      }
    }
    cargarDatos()
  }, [])

  const handleCreate = async (data: ProductoFormData) => {
    return fetch(`${API_URL}/productos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
  }

  const handleUpdate = async (id: number, data: ProductoFormData) => {
    return fetch(`${API_URL}/productos/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
  }

  const handleToggleDisponible = async (producto: Producto) => {
    const response = await handleUpdate(producto.id, {
      nombre: producto.nombre,
      descripcion: producto.descripcion ?? '',
      precio_base: producto.precio_base,
      unidad_venta_id: producto.unidad_venta_id,
      stock_cantidad: producto.stock_cantidad,
      disponible: !producto.disponible,
    })
    if (!response.ok) {
      setError(await leerError(response))
      return
    }
    await cargarProductos()
  }

  const handleDelete = async (id: number) => {
    const response = await fetch(`${API_URL}/productos/${id}`, { method: 'DELETE' })
    if (!response.ok) {
      setError(await leerError(response))
      return
    }
    await cargarProductos()
  }

  const abrirParaCrear = () => {
    setProductoEditando(null)
    setErrorModal(null)
    setModalAbierto(true)
  }

  const abrirParaEditar = (producto: Producto) => {
    setProductoEditando(producto)
    setErrorModal(null)
    setModalAbierto(true)
  }

  const cerrarModal = () => {
    setModalAbierto(false)
    setProductoEditando(null)
    setErrorModal(null)
  }

  const handleSubmit = async (data: ProductoFormData) => {
    setGuardando(true)
    try {
      const response = productoEditando
        ? await handleUpdate(productoEditando.id, data)
        : await handleCreate(data)
      // Si la API rechaza (por ejemplo 409 por nombre repetido), el error se
      // muestra dentro del modal y el modal no se cierra.
      if (!response.ok) {
        setErrorModal(await leerError(response))
        return
      }
      await cargarProductos()
      cerrarModal()
    } catch {
      setErrorModal('No se pudo conectar con la API')
    } finally {
      setGuardando(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar titulo="Food Store - Catálogo de Productos" />
      <main className="mx-auto max-w-5xl p-6">
        <button
          type="button"
          onClick={abrirParaCrear}
          disabled={cargando}
          className="mb-6 rounded bg-green-600 px-4 py-2 text-white hover:bg-green-700 disabled:opacity-50"
        >
          Nuevo producto
        </button>
        {cargando && <p className="text-gray-600">Cargando productos...</p>}
        {error && (
          <p className="mb-4 rounded bg-red-100 px-3 py-2 text-red-800">{error}</p>
        )}
        {!cargando && !error && productos.length === 0 && (
          <p className="text-gray-600">No hay productos cargados.</p>
        )}
        <ProductoList
          productos={productos}
          onEdit={abrirParaEditar}
          onToggleDisponible={handleToggleDisponible}
          onDelete={handleDelete}
        />
      </main>
      {modalAbierto && (
        <ProductoModal
          productoEditando={productoEditando}
          unidades={unidades}
          error={errorModal}
          guardando={guardando}
          onSubmit={handleSubmit}
          onCancel={cerrarModal}
        />
      )}
    </div>
  )
}

export default App