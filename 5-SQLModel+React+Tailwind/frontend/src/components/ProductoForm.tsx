interface ProductoFormProps {
  titulo: string
}

export const ProductoForm = ({ titulo }: ProductoFormProps) => {
  return (
    <form className="bg-white rounded-lg shadow p-6 flex flex-col gap-4">
      <h2 className="text-2xl font-bold text-gray-900">{titulo}</h2>
      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-gray-700">Nombre</label>
        <input type="text" className="border border-gray-300 rounded px-4 py-2" />
      </div>
      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-gray-700">Descripción</label>
        <input type="text" className="border border-gray-300 rounded px-4 py-2" />
      </div>
      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-gray-700">Precio</label>
        <input type="number" className="border border-gray-300 rounded px-4 py-2" />
      </div>
      <button type="button" className="bg-blue-500 text-white font-semibold rounded px-4 py-2">
        Guardar
      </button>
    </form>
  )
}