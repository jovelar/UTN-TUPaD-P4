import { useEffect, useState } from 'react'
import CategoriaModal from './components/CategoriaModal'
import {
  createCategoria,
  deleteCategoria,
  getCategorias,
  patchCategoria,
  updateCategoria,
} from './services/categoriasApi'
import type { Categoria, CategoriaFormData } from './types'

// Componente principal: carga las categorías al montar, muestra los estados
// de carga y error, y decide entre crear o actualizar según haya o no una
// categoría en edición.
function App() {
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [modalAbierto, setModalAbierto] = useState(false)
  const [categoriaEditando, setCategoriaEditando] = useState<Categoria | null>(
    null,
  )

  const cargarCategorias = async () => {
    setLoading(true)
    try {
      const data = await getCategorias()
      setCategorias(data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
    } finally {
      setLoading(false)
    }
  }

  // Efecto con array de dependencias vacío: se ejecuta una sola vez, al
  // montar el componente, para traer las categorías de la API.
  useEffect(() => {
    cargarCategorias()
  }, [])

  const abrirParaCrear = () => {
    setCategoriaEditando(null)
    setModalAbierto(true)
  }

  const abrirParaEditar = (categoria: Categoria) => {
    setCategoriaEditando(categoria)
    setModalAbierto(true)
  }

  const cerrarModal = () => {
    setModalAbierto(false)
    setCategoriaEditando(null)
  }

  const handleSubmitCategoria = async (data: CategoriaFormData) => {
    try {
      if (categoriaEditando) {
        await updateCategoria(categoriaEditando.id, data)
      } else {
        await createCategoria(data)
      }
      await cargarCategorias()
      cerrarModal()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
    }
  }

  const handleEliminarCategoria = async (categoria: Categoria) => {
    const confirma = window.confirm(`¿Eliminar "${categoria.nombre}"?`)
    if (!confirma) return
    try {
      await deleteCategoria(categoria.id)
      await cargarCategorias()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
    }
  }

  const handleRenombrarRapido = async (categoria: Categoria) => {
    const nuevoNombre = window.prompt('Nuevo nombre:', categoria.nombre)
    if (!nuevoNombre || nuevoNombre === categoria.nombre) return
    try {
      await patchCategoria(categoria.id, { nombre: nuevoNombre })
      await cargarCategorias()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
    }
  }

  return (
    <main>
      <h1>Categorías (JSON Server)</h1>
      <p>
        Requiere <code>pnpm server</code> en ejecución en otra terminal
        (levanta JSON Server en <code>http://localhost:3000</code>).
      </p>

      <button type="button" onClick={abrirParaCrear}>
        Nueva categoría
      </button>

      {loading && <p>Cargando categorías...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <table>
          <thead>
            <tr>
              <th>Id</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {categorias.length === 0 && (
              <tr>
                <td colSpan={4}>Todavía no hay categorías.</td>
              </tr>
            )}
            {categorias.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.nombre}</td>
                <td>{c.descripcion}</td>
                <td>
                  <button type="button" onClick={() => abrirParaEditar(c)}>
                    Editar
                  </button>
                  <button type="button" onClick={() => handleRenombrarRapido(c)}>
                    Renombrar (PATCH)
                  </button>
                  <button type="button" onClick={() => handleEliminarCategoria(c)}>
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <CategoriaModal
        isOpen={modalAbierto}
        categoriaEditando={categoriaEditando}
        onSubmit={handleSubmitCategoria}
        onCancel={cerrarModal}
      />
    </main>
  )
}

export default App
