type MensajeProps = {
    mensaje: string
}

export function Cargando({ mensaje }: MensajeProps) {
    return (
        <div className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white p-6 text-gray-600">
            <span className="h-5 w-5 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />
            {mensaje}
        </div>
    )
}

export function Vacio({ mensaje }: MensajeProps) {
    return (
        <div className="rounded-lg border border-dashed border-gray-300 bg-white p-6 text-center text-gray-500">
            {mensaje}
        </div>
    )
}

export function ErrorMensaje({ mensaje }: MensajeProps) {
    return (
        <div role="alert" className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
            {mensaje}
        </div>
    )
}