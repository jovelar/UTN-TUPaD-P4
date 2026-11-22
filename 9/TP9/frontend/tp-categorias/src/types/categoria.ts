export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
}
export type CategoriaInput = Omit<Categoria, 'id'>;
// export type CategoriaFormData = {
//     nombre: string;
//     descripcion: string;
// }

// export type Categoria = CategoriaFormData & {
//     id: number;
// }