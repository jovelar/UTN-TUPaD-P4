import { useForm } from '@tanstack/react-form'
import { Link, Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { ErrorMensaje } from '../components/Estados'

const input =
    'mt-1 w-full rounded border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200'

function LoginPage() {
    const user = useAuthStore((s) => s.user)
    const login = useAuthStore((s) => s.login)
    const isSubmitting = useAuthStore((s) => s.isSubmitting)
    const error = useAuthStore((s) => s.error)

    const form = useForm({
        defaultValues: { email: '', password: '' },
        onSubmit: async ({ value }) => {
            await login(value.email, value.password)
        },
    })

    if (user) return <Navigate to="/categories" replace />

    return (
        <main className="mx-auto mt-16 max-w-sm p-6">
            <form
                onSubmit={(e) => {
                    e.preventDefault()
                    form.handleSubmit()
                }}
                className="flex flex-col gap-4 rounded-lg bg-white p-6 shadow"
            >
                <h2 className="text-xl font-bold">Iniciar sesión</h2>

                <form.Field name="email">
                    {(f) => (
                        <label className="block">
                            Email
                            <input
                                type="email"
                                required
                                className={input}
                                value={f.state.value}
                                onBlur={f.handleBlur}
                                onChange={(e) => f.handleChange(e.target.value)}
                            />
                        </label>
                    )}
                </form.Field>

                <form.Field name="password">
                    {(f) => (
                        <label className="block">
                            Contraseña
                            <input
                                type="password"
                                required
                                className={input}
                                value={f.state.value}
                                onBlur={f.handleBlur}
                                onChange={(e) => f.handleChange(e.target.value)}
                            />
                        </label>
                    )}
                </form.Field>

                {error && <ErrorMensaje mensaje={error} />}

                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
                >
                    {isSubmitting ? 'Ingresando...' : 'Ingresar'}
                </button>

                <p className="text-sm text-gray-600">
                    ¿No tenés cuenta?{' '}
                    <Link to="/register" className="text-blue-600 hover:underline">
                        Registrate
                    </Link>
                </p>
            </form>
        </main>
    )
}

export default LoginPage