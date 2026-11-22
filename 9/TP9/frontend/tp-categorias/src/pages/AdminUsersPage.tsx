import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Cargando, ErrorMensaje, Vacio } from '../components/Estados'
import { usuarioService } from '../services/usuarioService'
import { handleApiError } from '../api/handleApiError'
import type { UsuarioPublic } from '../types/auth.types'

const sinUsuarios: UsuarioPublic[] = []

function AdminUsersPage() {
    const queryClient = useQueryClient()

    const { data = sinUsuarios, isLoading, error } = useQuery({
        queryKey: ['usuarios'],
        queryFn: usuarioService.listar,
    })

    const cambiarEstado = useMutation({
        mutationFn: (u: UsuarioPublic) =>
            u.activo ? usuarioService.desactivar(u.id) : usuarioService.activar(u.id),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['usuarios'] }),
    })

    return (
        <main className="mx-auto max-w-5xl p-6">
            <h2 className="mb-6 text-2xl font-bold">Usuarios</h2>

            {cambiarEstado.error && (
                <div className="mb-4">
                    <ErrorMensaje mensaje={handleApiError(cambiarEstado.error)} />
                </div>
            )}

            {isLoading ? (
                <Cargando mensaje="Cargando usuarios..." />
            ) : error ? (
                <ErrorMensaje mensaje={handleApiError(error)} />
            ) : data.length === 0 ? (
                <Vacio mensaje="No hay usuarios." />
            ) : (
                <div className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
                    <table className="w-full border-collapse text-left text-sm">
                        <thead className="bg-gray-50">
                            <tr>
                                {['Nombre', 'Email', 'Roles', 'Estado', 'Acciones'].map((h) => (
                                    <th key={h} className="border-b border-gray-200 px-4 py-3 font-semibold text-gray-700">
                                        {h}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((u) => (
                                <tr key={u.id} className="hover:bg-gray-50">
                                    <td className="border-b border-gray-100 px-4 py-3">{u.nombre} {u.apellido}</td>
                                    <td className="border-b border-gray-100 px-4 py-3">{u.email}</td>
                                    <td className="border-b border-gray-100 px-4 py-3">{u.roles.join(', ')}</td>
                                    <td className="border-b border-gray-100 px-4 py-3">
                                        <span className={u.activo ? 'text-green-700' : 'text-red-600'}>
                                            {u.activo ? 'Activo' : 'Desactivado'}
                                        </span>
                                    </td>
                                    <td className="border-b border-gray-100 px-4 py-3">
                                        <button
                                            type="button"
                                            disabled={cambiarEstado.isPending}
                                            onClick={() => cambiarEstado.mutate(u)}
                                            className={`rounded px-3 py-1 text-white disabled:opacity-50 ${u.activo ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'
                                              }`}
                                        >
                                            {u.activo ? 'Desactivar' : 'Activar'}
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </main>
    )
}

export default AdminUsersPage