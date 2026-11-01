import type { Categoria } from "../types/categoria";
import CategoriaCard from "./CategoriaCard"
type CategoriaListProps = {
  categorias: Categoria[]
  onEdit: (categoria: Categoria) => void
  onDelete: (id: number) => void
}

function CategoriaList({ categorias, onEdit, onDelete }: CategoriaListProps) {
  return (
    <div className="grid gap-4">
      {categorias.map((categoria) => (
        <CategoriaCard
          key={categoria.id}
          categoria={categoria}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}

export default CategoriaList