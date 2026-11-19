import type { FormEvent, ReactNode } from 'react'
import { ErrorMensaje } from './Estados'

type IngredienteModalProps = {
    isOpen: boolean
    titulo: string
    errorApi: string | null
    onSubmit: () => void
    onCancel: () => void
    children: ReactNode
}

function IngredienteModal({ isOpen, titulo, errorApi, onSubmit, onCancel, children }: IngredienteModalProps) {
    if (!isOpen) return null

    const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        onSubmit()
    }

    return (
        <div className="fixed inset-0 z-10 flex items-center justify-center bg-black/50">
            <form
                onSubmit={handleSubmit}
                className="flex w-full max-w-md flex-col gap-4 rounded-lg bg-white p-6 shadow-lg"
            >
                <h3 className="text-xl font-bold">{titulo}</h3>
                {children}
                {errorApi && <ErrorMensaje mensaje={errorApi} />}
                <div className="flex justify-end gap-2">
                    <button type="button" onClick={onCancel} className="rounded border px-4 py-2">
                        Cancelar
                    </button>
                    <button type="submit" className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
                        Guardar
                    </button>
                </div>
            </form>
        </div>
    )
}

export default IngredienteModal