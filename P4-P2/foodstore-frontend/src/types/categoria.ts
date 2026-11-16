export interface Categoria {
  id: number
  nombre: string
  descripcion: string | null
  activo: boolean
  anulado_at: string | null
}

// Categoría tal como viene dentro de un producto: suma es_principal
export interface CategoriaDeProducto {
  id: number
  nombre: string
  descripcion: string | null
  activo: boolean
  es_principal: boolean
}
// export type CategoriaFormData = {
//     nombre: string;
//     descripcion: string;
// }

// export type Categoria = CategoriaFormData & {
//     id: number;
// }