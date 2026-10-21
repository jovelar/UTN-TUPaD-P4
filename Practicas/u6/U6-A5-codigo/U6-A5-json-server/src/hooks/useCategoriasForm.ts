import { useForm } from './useForm'
import type { CategoriaFormData } from '../types'

const vacio: CategoriaFormData = {
  nombre: '',
  descripcion: '',
}

// Especialización del hook genérico para categorías, igual que en la
// Actividad 4.
export function useCategoriasForm(initialState: CategoriaFormData = vacio) {
  return useForm<CategoriaFormData>(initialState)
}
