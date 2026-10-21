import { useEffect, type FormEvent } from 'react'
import { useCategoriasForm } from '../hooks/useCategoriasForm'
import type { Categoria, CategoriaFormData } from '../types'

type CategoriaModalProps = {
  isOpen: boolean
  categoriaEditando: Categoria | null
  onSubmit: (data: CategoriaFormData) => void
  onCancel: () => void
}

// Modal controlado: no sabe cómo se guardan las categorías. Sólo recibe
// callbacks (onSubmit, onCancel) y no tiene lógica de negocio propia. Su
// estado interno lo maneja useCategoriasForm.
function CategoriaModal({
  isOpen,
  categoriaEditando,
  onSubmit,
  onCancel,
}: CategoriaModalProps) {
  const { formState, handleChange, resetForm, setFormValues } = useCategoriasForm()

  // Al abrir el modal: si hay una categoría para editar, precarga sus datos
  // con setFormValues; si no, deja el formulario vacío para crear una nueva.
  useEffect(() => {
    if (categoriaEditando) {
      setFormValues({
        nombre: categoriaEditando.nombre,
        descripcion: categoriaEditando.descripcion,
      })
    } else {
      resetForm()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [categoriaEditando, isOpen])

  if (!isOpen) return null

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    onSubmit(formState)
  }

  return (
    <div className="modal-backdrop">
      <form className="modal" onSubmit={handleSubmit}>
        <h3>{categoriaEditando ? 'Editar categoría' : 'Nueva categoría'}</h3>
        <label>
          Nombre
          <input
            name="nombre"
            value={formState.nombre}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Descripción
          <input
            name="descripcion"
            value={formState.descripcion}
            onChange={handleChange}
          />
        </label>
        <div className="modal-actions">
          <button type="submit">Guardar</button>
          <button type="button" onClick={onCancel}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  )
}

export default CategoriaModal
