import type { Categoria, CategoriaFormData } from '../types'

const BASE_URL = 'http://localhost:3000'

// Capa de servicios: todos los fetch de categorías en un solo lugar.
// La URL base queda escrita acá para simplificar el ejemplo; en un proyecto
// real conviene leerla de una variable de entorno.

export async function getCategorias(): Promise<Categoria[]> {
  const response = await fetch(`${BASE_URL}/categorias`)
  if (!response.ok) {
    throw new Error('Error al obtener las categorías')
  }
  return response.json()
}

export async function getCategoriaPorId(id: number): Promise<Categoria> {
  const response = await fetch(`${BASE_URL}/categorias/${id}`)
  if (!response.ok) {
    throw new Error('Error al obtener la categoría')
  }
  return response.json()
}

export async function createCategoria(
  data: CategoriaFormData,
): Promise<Categoria> {
  const response = await fetch(`${BASE_URL}/categorias`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!response.ok) {
    throw new Error('Error al crear la categoría')
  }
  return response.json()
}

// PUT: reemplaza la categoría completa. Es el método que usa la edición
// desde el modal.
export async function updateCategoria(
  id: number,
  data: CategoriaFormData,
): Promise<Categoria> {
  const response = await fetch(`${BASE_URL}/categorias/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!response.ok) {
    throw new Error('Error al actualizar la categoría')
  }
  return response.json()
}

// PATCH: modifica sólo los campos que se envían (acá, el nombre). Se usa
// desde el botón "Renombrar (PATCH)" de la tabla.
export async function patchCategoria(
  id: number,
  data: Partial<CategoriaFormData>,
): Promise<Categoria> {
  const response = await fetch(`${BASE_URL}/categorias/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!response.ok) {
    throw new Error('Error al actualizar parcialmente la categoría')
  }
  return response.json()
}

// DELETE: elimina la categoría.
export async function deleteCategoria(id: number): Promise<void> {
  const response = await fetch(`${BASE_URL}/categorias/${id}`, {
    method: 'DELETE',
  })
  if (!response.ok) {
    throw new Error('Error al eliminar la categoría')
  }
}
