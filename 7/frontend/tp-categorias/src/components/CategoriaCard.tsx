import type { Categoria } from "../types/categoria";

type CategoriaCardProps = {
  categoria: Categoria
  onEdit: (categoria: Categoria) => void
  onDelete: (id: number) => void
}

function CategoriaCard({ categoria, onEdit, onDelete }: CategoriaCardProps) {
  return (
    <div className="rounded border bg-white p-4">
      <h3 className="text-lg font-semibold">{categoria.nombre}</h3>
      <p className="text-gray-600">{categoria.descripcion}</p>
      <div className="mt-4 flex gap-2">
        <button
          type="button"
          onClick={() => onEdit(categoria)}
          className="rounded bg-yellow-500 px-3 py-1 text-white"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onDelete(categoria.id)}
          className="rounded bg-red-600 px-3 py-1 text-white"
        >
          Eliminar
        </button>
      </div>
    </div>
  )
}

export default CategoriaCard