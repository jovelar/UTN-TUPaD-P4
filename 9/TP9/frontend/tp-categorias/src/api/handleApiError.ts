import axios from 'axios';

export function handleApiError(error: unknown): string {
    if (!axios.isAxiosError(error)) return 'Error inesperado.';
    if (error.code === 'ECONNABORTED') {
        return 'El servidor tardó demasiado en responder.';
    }
    if (!error.response) return 'No se pudo conectar con el servidor.';

    const { status, data } = error.response;
    const detail = (data as { detail?: unknown })?.detail;

    switch (status) {
        case 401: return 'La sesión venció. Es necesario iniciar sesión de nuevo.';
        case 403: return 'No tiene permisos para realizar esta acción.';
        case 422: return 'Los datos enviados no son válidos.';
    }
    if (typeof detail === 'string') return detail;   // 400, 404, 409: mensaje del backend
    if (status < 500) return 'No se pudo completar la operación.';
    return 'Error del servidor. Intente nuevamente más tarde.';
}