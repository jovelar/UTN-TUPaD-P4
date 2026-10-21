import { useState } from 'react'
import CategoriaModal from './components/CategoriaModal'
import ContactForm from './components/ContactForm'
import type { Categoria, CategoriaFormData } from './types'

let siguienteId = 1

// Componente principal ("orquestador"): mantiene la lista de categorías,
// abre y cierra el modal, agrega categorías nuevas con un id generado y
// actualiza created_at/updated_at. Guarda todo en memoria, sin backend: la
// versión conectada a una API con JSON Server es la de la Actividad 5, que
// reutiliza este mismo hook y este mismo modal.
function App() {
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [modalAbierto, setModalAbierto] = useState(false)
  const [categoriaEditando, setCategoriaEditando] = useState<Categoria | null>(
    null,
  )

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

  const guardarCategoria = (data: CategoriaFormData) => {
    const ahora = new Date().toISOString()
    if (categoriaEditando) {
      setCategorias((prev) =>
        prev.map((c) =>
          c.id === categoriaEditando.id ? { ...c, ...data, updated_at: ahora } : c,
        ),
      )
    } else {
      setCategorias((prev) => [
        ...prev,
        { id: siguienteId++, ...data, created_at: ahora, updated_at: ahora },
      ])
    }
    cerrarModal()
  }

  return (
    <main>
      <h1>Custom Hooks: useForm</h1>

      <section>
        <h2>Ejemplo básico del hook</h2>
        <ContactForm />
      </section>

      <section>
        <h2>Especialización: useCategoriasForm + modal</h2>
        <button type="button" onClick={abrirParaCrear}>
          Nueva categoría
        </button>
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Descripción</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {categorias.length === 0 && (
              <tr>
                <td colSpan={3}>Todavía no hay categorías.</td>
              </tr>
            )}
            {categorias.map((c) => (
              <tr key={c.id}>
                <td>{c.nombre}</td>
                <td>{c.descripcion}</td>
                <td>
                  <button type="button" onClick={() => abrirParaEditar(c)}>
                    Editar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <CategoriaModal
          isOpen={modalAbierto}
          categoriaEditando={categoriaEditando}
          onSubmit={guardarCategoria}
          onCancel={cerrarModal}
        />
      </section>
    </main>
  )
}

export default App
