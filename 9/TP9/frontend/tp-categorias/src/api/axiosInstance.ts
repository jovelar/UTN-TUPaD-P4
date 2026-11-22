import axios from 'axios';
import type { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { useAuthStore } from '../store/authStore';

export const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1',
    timeout: 10000,          // 10 s; por defecto Axios no tiene límite (0)
    withCredentials: true,   // envía y recibe la cookie HttpOnly entre orígenes
});

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    config.headers.set('Accept-Language', 'es');   // ejemplo de encabezado común
    return config;
});

// Peticiones que responden 401 como parte de su funcionamiento normal
const RUTAS_DE_AUTH = ['/auth/token', '/auth/me'];

api.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
        const url = error.config?.url ?? '';
        const esDeAuth = RUTAS_DE_AUTH.some((r) => url.includes(r));

        if (error.response?.status === 401 && !esDeAuth) {
            // sesión vencida: la interfaz vuelve al login
            useAuthStore.setState({ user: null });
        }
        // el servicio o componente también se entera
        return Promise.reject(error);
    },
);