import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { Cargando } from './Estados'

type ProtectedRouteProps = {
    allowedRoles?: string[]
}

function ProtectedRoute({ allowedRoles }: ProtectedRouteProps) {
    const user = useAuthStore((s) => s.user)
    const isChecking = useAuthStore((s) => s.isChecking)

    if (isChecking && !user) return <Cargando mensaje="Restaurando sesión…" />
    if (!user) return <Navigate to="/login" replace />
    if (allowedRoles && !user.roles.some((rol) => allowedRoles.includes(rol))) {
        return <Navigate to="/unauthorized" replace />
    }
    return <Outlet />
}

export default ProtectedRoute