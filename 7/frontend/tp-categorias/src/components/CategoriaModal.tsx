import type { FormEvent } from 'react'
import { useForm } from '../hooks/useForm'
import type { Categoria } from '../types/categoria'

type CategoriaModalProps = {
  categoriaEditando: Categoria | null
  onSubmit: (data: { nombre: string; descripcion: string }) => void
  onCancel: () => void
}

// Modal controlado: no sabe cómo se guardan las categorías. Sólo recibe
// callbacks (onSubmit, onCancel) y no tiene lógica de negocio propia. Su
// estado interno lo maneja useCategoriasForm.
function CategoriaModal({

  categoriaEditando,
  onSubmit,
  onCancel,
}: CategoriaModalProps) {
   const { formState, handleChange } = useForm({
    nombre: categoriaEditando?.nombre ?? '',
    descripcion: categoriaEditando?.descripcion ?? '',
  })

//   // Al abrir el modal: si hay una categoría para editar, precarga sus datos
//   // con setFormValues; si no, deja el formulario vacío para crear una nueva.
//   useEffect(() => {
//     if (categoriaEditando) {
//       setFormValues({
//         nombre: categoriaEditando.nombre,
//         descripcion: categoriaEditando.descripcion,
//       })
//     } else {
//       resetForm()
//     }
//     // eslint-disable-next-line react-hooks/exhaustive-deps
//   }, [categoriaEditando, isOpen])

//   if (!isOpen) return null

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    onSubmit(formState)
  }

 return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/50">
      <form className="w-full max-w-md rounded-lg bg-white p-6" onSubmit={handleSubmit}>
        <h3 className="mb-4 text-xl font-bold">
          {categoriaEditando ? 'Editar categoría' : 'Nueva categoría'}
        </h3>
        <label className="mb-4 block">
          Nombre
          <input
            name="nombre"
            value={formState.nombre}
            onChange={handleChange}
            required
            className="mt-1 w-full rounded border px-3 py-2"
          />
        </label>
        <label className="mb-4 block">
          Descripción
          <input
            name="descripcion"
            value={formState.descripcion}
            onChange={handleChange}
            required
            minLength={3}
            className="mt-1 w-full rounded border px-3 py-2"
          />
        </label>
        <div className="flex justify-end gap-2">
          <button type="submit" className="rounded bg-blue-600 px-4 py-2 text-white">
            Guardar
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="rounded border px-4 py-2"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  )
}

export default CategoriaModal
