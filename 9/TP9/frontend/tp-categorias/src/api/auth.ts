import axios from 'axios';
import { api } from './axiosInstance';
import type { MensajeResponse, RegisterData, UsuarioAuth, UsuarioPublic } from '../types/auth.types';

export async function requestLogin(
    email: string,
    password: string,
): Promise<void> {
    try {
        // formulario OAuth2, no JSON
        await api.post<MensajeResponse>('/auth/token', new URLSearchParams({ username: email, password }));
    } catch (e) {
        // FastAPI responde {"detail": "..."}: 401 credenciales incorrectas, 400 cuenta desactivada
        const detail = axios.isAxiosError(e) ? (e.response?.data as { detail?: unknown })?.detail : undefined;
        throw new Error(typeof detail === 'string' ? detail : 'No se pudo iniciar sesión');
    }
}

export async function requestMe(): Promise<UsuarioAuth | null> {
    try {
        const { data } = await api.get<UsuarioPublic>('/auth/me');
        return { id: data.id, nombre: data.nombre, apellido: data.apellido, email: data.email, roles: data.roles };
    } catch {
        return null;   // 401: sin sesión válida; 400: cuenta desactivada
    }
}

export async function requestLogout(): Promise<void> {
    await api.post<MensajeResponse>('/auth/logout');
}

export async function requestRegister(datos: RegisterData): Promise<UsuarioPublic> {
    return (await api.post<UsuarioPublic>('/auth/register', datos)).data;
}