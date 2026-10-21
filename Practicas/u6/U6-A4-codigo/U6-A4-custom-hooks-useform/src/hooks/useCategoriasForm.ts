import { useForm } from './useForm'
import type { CategoriaFormData } from '../types'

const vacio: CategoriaFormData = {
  nombre: '',
  descripcion: '',
}

// Especialización del hook genérico para el dominio de categorías. En lugar
// de usar useForm directamente en toda la aplicación, se separa la lógica
// genérica del dominio específico: el código queda más expresivo y el mismo
// patrón sirve para otros formularios (useProductoForm, useUsuarioForm...).
export function useCategoriasForm(initialState: CategoriaFormData = vacio) {
  return useForm<CategoriaFormData>(initialState)
}
