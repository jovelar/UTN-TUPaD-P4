// Los tipos de formulario se declaran con `type`, no con `interface`:
// useForm<T> exige `T extends Record<string, unknown>` y una interface no
// cumple esa restricción (ver la nota en el README).

export type CategoriaFormData = {
  nombre: string
  descripcion: string
}

export type Categoria = CategoriaFormData & {
  id: number
  created_at: string
  updated_at: string
}
