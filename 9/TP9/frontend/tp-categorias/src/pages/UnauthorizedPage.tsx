import { Link } from 'react-router-dom'

function UnauthorizedPage() {
    return (
        <main className="mx-auto mt-16 max-w-md p-6 text-center">
            <h2 className="text-2xl font-bold text-red-600">Acceso denegado</h2>
            <p className="mt-2 text-gray-600">No tenés permisos para ver esta página.</p>
            <Link to="/categories" className="mt-4 inline-block text-blue-600 hover:underline">
                Volver a categorías
            </Link>
        </main>
    )
}

export default UnauthorizedPage