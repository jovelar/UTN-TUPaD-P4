import { useForm } from '@tanstack/react-form'
import type { Product } from '../types/Iproduct'

type ProductFormValues = Omit<Product, 'id' | 'rating'>

const input = 'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200'

export const FormProduct = ({ onSubmit }: { onSubmit?: (v: ProductFormValues) => void }) => {
  const form = useForm({
    defaultValues: { 
        title: '', 
        price: 0, 
        description: '', 
        category: '', 
        image: '' } as ProductFormValues,
    validators: {
      onSubmit: ({ value }) => {
        if (!value.title.trim()) {
          return { fields: { title: 'El título es obligatorio' } }
        }
        return undefined
      },
    },
    onSubmit: async ({ value }) => {
      onSubmit?.(value)
      console.log(value)
    },
  })

  return (
    <div className="mx-auto max-w-lg rounded-2xl bg-white p-8 shadow-lg">
      <h2 className="mb-6 text-2xl font-bold text-gray-800">Nuevo Producto</h2>
      <form 
      onSubmit={(e) => { e.preventDefault(); form.handleSubmit() }} 
      className="flex flex-col gap-4">

        <form.Field name="title">
          {(f) => (
            <>
              <input 
              placeholder="Título" 
              className={input} 
              value={f.state.value} 
              onChange={(e) => f.handleChange(e.target.value)} />
              {f.state.meta.errors.map((err) => (
                <p key={String(err)} className="mt-1 text-xs text-red-500">{err}</p>
              ))}
            </>
          )}
        </form.Field>

        <form.Field name="price">
          {(f) => 
          <input 
          type="number" 
          placeholder="Precio" 
          className={input} 
          value={f.state.value} 
          onChange={(e) => f.handleChange(Number(e.target.value))} />}
        </form.Field>

        <form.Field name="category">
          {(f) => 
          <input 
          placeholder="Categoría"
          className={input} 
          value={f.state.value} 
          onChange={(e) => f.handleChange(e.target.value)} />}
        </form.Field>

        <form.Field name="image">
          {(f) => 
          <input 
          placeholder="URL imagen" 
          className={input} 
          value={f.state.value} 
          onChange={(e) => f.handleChange(e.target.value)} />}
        </form.Field>

        <form.Field name="description">
          {(f) => 
          <textarea 
          rows={3}
          placeholder="Descripción"
          className={`${input} resize-none`} 
          value={f.state.value} 
          onChange={(e) => f.handleChange(e.target.value)} />}
        </form.Field>

        <button 
        type="submit" 
        className="rounded-lg bg-blue-600 py-2 text-sm font-semibold text-white hover:bg-blue-700 transition">
          Guardar
        </button>
      </form>
    </div>
  )
}
