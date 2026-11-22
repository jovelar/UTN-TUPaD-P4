export interface CategoriaAsignada {
    id: number;
    nombre: string;
    es_principal: boolean;
}

export interface Producto {
    id: number;
    nombre: string;
    descripcion: string | null;
    precio_base: number;
    imagenes_url: string[];
    disponible: boolean;
    categorias: CategoriaAsignada[];
}
export type ProductoInput = Omit<Producto, 'id' | 'categorias'>;


// export interface Producto  {
//     id: number;
//     nombre: string;
//     descripcion: string;
//     precio_base: number;
//     imagenes_url: string[];
//     disponible:boolean;
// }

// export type ProductoRead = {
//     id: number;
// }
