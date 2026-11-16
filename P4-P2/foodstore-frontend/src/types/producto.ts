import type { CategoriaDeProducto } from './categoria'
import type { UnidadMedida } from './unidadMedida'

export interface Producto {
  id: number
  nombre: string
  descripcion: string | null
  precio_base: number
  stock_cantidad: number
  disponible: boolean
  activo: boolean
  anulado_at: string | null
  unidad_venta_id: number
  unidad_venta: UnidadMedida
  categorias: CategoriaDeProducto[]
  hay_stock: boolean
}

// Datos que se envían en el body de POST y PUT
export interface ProductoFormData {
  nombre: string
  descripcion: string
  precio_base: number
  unidad_venta_id: number
  stock_cantidad: number
  disponible: boolean
}


// export type Producto = {
//     id: number;
//     nombre: string;
//     descripcion: string;
//     precio_base: number;
//     imagen_url: string[];
//     disponible:boolean;
// }

// // export type ProductoRead = {
// //     id: number;
// // }
