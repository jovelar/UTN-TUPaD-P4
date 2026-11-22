import { api } from '../api/axiosInstance';
import type { Producto, ProductoInput } from '../types/producto';

export const productoService = {
    listar: async () =>
        (await api.get<Producto[]>('/productos/')).data,

    obtener: async (id: number) =>
        (await api.get<Producto>(`/productos/${id}`)).data,

    crear: async (datos: ProductoInput) =>
        (await api.post<Producto>('/productos/', datos)).data,

    actualizar: async (id: number, cambios: Partial<ProductoInput>) =>
        (await api.patch<Producto>(`/productos/${id}`, cambios)).data,

    eliminar: async (id: number) => {
        await api.delete(`/productos/${id}`);
    },
};