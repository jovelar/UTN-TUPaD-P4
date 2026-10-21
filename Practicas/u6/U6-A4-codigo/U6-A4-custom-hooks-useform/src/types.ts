// Los tipos de formulario se declaran con `type`, no con `interface`.
// useForm<T> exige `T extends Record<string, unknown>`, y TypeScript no
// considera que una interface cumpla esa restricción aunque tenga las mismas
// propiedades: `useForm<MiInterface>(...)` no compila.

export type ContactFormData = {
  nombre: string
  email: string
}

export type CategoriaFormData = {
  nombre: string
  descripcion: string
}

export type Categoria = CategoriaFormData & {
  id: number
  created_at: string
  updated_at: string
}
