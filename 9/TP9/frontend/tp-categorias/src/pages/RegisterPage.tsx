import { useState } from 'react'
import { useForm } from '@tanstack/react-form'
import { Link, useNavigate } from 'react-router-dom'
import { requestRegister } from '../api/auth'
import { handleApiError } from '../api/handleApiError'
import { ErrorMensaje } from '../components/Estados'
import type { RegisterData } from '../types/auth.types'

const input =
    'mt-1 w-full rounded border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200'

type RegisterFormValues = Required<RegisterData>

const valoresVacios: RegisterFormValues = {
    nombre: '',
    apellido: '',
    email: '',
    celular: '',
    password: '',
}

const campos: { name: keyof RegisterFormValues; label: string; type: string; required: boolean }[] = [
    { name: 'nombre', label: 'Nombre', type: 'text', required: true },
    { name: 'apellido', label: 'Apellido', type: 'text', required: true },
    { name: 'email', label: 'Email', type: 'email', required: true },
    { name: 'celular', label: 'Celular (opcional)', type: 'tel', required: false },
    { name: 'password', label: 'Contraseña', type: 'password', required: true },
]

function RegisterPage() {
    const navigate = useNavigate()
    const [errorApi, setErrorApi] = useState<string | null>(null)

    const form = useForm({
        defaultValues: valoresVacios,
        validators: {
            onSubmit: ({ value }) => {
                if (value.password.length < 8) {
                    return { fields: { password: 'La contraseña debe tener al menos 8 caracteres' } }
                }
                return undefined
            },
        },
        onSubmit: async ({ value }) => {
            setErrorApi(null)
            try {
                await requestRegister({ ...value, celular: value.celular.trim() || undefined })
                navigate('/login')
            } catch (e) {
                setErrorApi(handleApiError(e))
            }
        },
    })

    return (
        <main className="mx-auto mt-16 max-w-sm p-6">
            <form
                onSubmit={(e) => {
                    e.preventDefault()
                    form.handleSubmit()
                }}
                className="flex flex-col gap-4 rounded-lg bg-white p-6 shadow"
            >
                <h2 className="text-xl font-bold">Crear cuenta</h2>

                {campos.map((campo) => (
                    <form.Field key={campo.name} name={campo.name}>
                        {(f) => (
                            <label className="block">
                                {campo.label}
                                <input
                                    type={campo.type}
                                    required={campo.required}
                                    className={input}
                                    value={f.state.value}
                                    onBlur={f.handleBlur}
                                    onChange={(e) => f.handleChange(e.target.value)}
                                />
                                {f.state.meta.errors.map((err) => (
                                    <p key={String(err)} className="mt-1 text-xs text-red-500">{err}</p>
                                ))}
                            </label>
                        )}
                    </form.Field>
                ))}

                {errorApi && <ErrorMensaje mensaje={errorApi} />}

                <form.Subscribe selector={(s) => s.isSubmitting}>
                    {(isSubmitting) => (
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
                        >
                            {isSubmitting ? 'Registrando...' : 'Registrarse'}
                        </button>
                    )}
                </form.Subscribe>

                <p className="text-sm text-gray-600">
                    ¿Ya tenés cuenta?{' '}
                    <Link to="/login" className="text-blue-600 hover:underline">
                        Iniciá sesión
                    </Link>
                </p>
            </form>
        </main>
    )
}

export default RegisterPage