import { api } from '../api/axiosInstance';
import type { UsuarioPublic } from '../types/auth.types';

export const usuarioService = {
    listar: async () =>
        (await api.get<UsuarioPublic[]>('/auth/admin/usuarios')).data,

    activar: async (id: number) =>
        (await api.post<UsuarioPublic>(`/auth/admin/usuarios/${id}/activar`)).data,

    desactivar: async (id: number) =>
        (await api.post<UsuarioPublic>(`/auth/admin/usuarios/${id}/desactivar`)).data,
};