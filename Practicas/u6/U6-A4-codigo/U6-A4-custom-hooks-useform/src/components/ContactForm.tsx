import type { FormEvent } from 'react'
import { useForm } from '../hooks/useForm'
import type { ContactFormData } from '../types'

// Ejemplo básico de uso del hook: el componente sólo describe la interfaz.
// No define useState ni manejadores propios: todo viene de useForm en una
// sola línea.
function ContactForm() {
  const { formState, handleChange, resetForm } = useForm<ContactFormData>({
    nombre: '',
    email: '',
  })

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    console.log(formState)
    resetForm()
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Nombre
        <input name="nombre" value={formState.nombre} onChange={handleChange} />
      </label>
      <label>
        Email
        <input
          type="email"
          name="email"
          value={formState.email}
          onChange={handleChange}
        />
      </label>
      <button type="submit">Enviar</button>
    </form>
  )
}

export default ContactForm
