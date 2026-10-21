import { useState, type ChangeEvent } from 'react'

// Custom hook genérico para formularios.
//
// `T extends Record<string, unknown>` permite usar el mismo hook con
// cualquier forma de formulario, manteniendo el tipado. Importante: el tipo
// que se le pasa tiene que declararse con `type`, no con `interface`
// (ver la nota en src/types.ts).
export function useForm<T extends Record<string, unknown>>(initialState: T) {
  const [formState, setFormState] = useState<T>(initialState)

  // Un único manejador para todos los campos: toma `name` y `value` del
  // elemento que cambió y actualiza sólo esa propiedad, conservando el resto
  // con el spread operator. Acepta inputs, textareas y selects.
  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target
    setFormState((prevState) => ({
      ...prevState,
      [name]: value,
    }))
  }

  // Vuelve el formulario a sus valores iniciales.
  const resetForm = () => {
    setFormState(initialState)
  }

  // Extensión del hook: reemplaza todo el estado desde afuera. Se usa para
  // precargar los datos de un registro cuando se abre el formulario para
  // editarlo.
  const setFormValues = (values: T) => {
    setFormState(values)
  }

  return {
    ...formState,
    formState,
    handleChange,
    resetForm,
    setFormValues,
  }
}
