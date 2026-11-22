import { api } from '../api/axiosInstance';
import type { Categoria, CategoriaInput } from '../types/categoria';

export const categoriaService = {
    listar: async () =>
        (await api.get<Categoria[]>('/categorias/')).data,

    obtener: async (id: number) =>
        (await api.get<Categoria>(`/categorias/${id}`)).data,

    crear: async (datos: CategoriaInput) =>
        (await api.post<Categoria>('/categorias/', datos)).data,

    actualizar: async (id: number, cambios: Partial<CategoriaInput>) =>
        (await api.patch<Categoria>(`/categorias/${id}`, cambios)).data,

    eliminar: async (id: number) => {
        await api.delete(`/categorias/${id}`);
    },
};