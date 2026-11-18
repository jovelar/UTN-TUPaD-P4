import { useState } from 'react'
import CategoriaList from '../components/CategoriaList'
import CategoriaModal from '../components/CategoriaModal'
import type { Categoria } from '../types/categoria'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { actualizarCategoria, crearCategoria, eliminarCategoria, getCategorias } from '../services/categoria'

function CategoriasPage() {
    const [modalAbierto, setModalAbierto] = useState(false)
    const [categoriaEditando, setCategoriaEditando] = useState<Categoria | null>(
        null,
    )

    const { data, isLoading, isError } = useQuery({
        queryKey: ['categorias'],
        queryFn: getCategorias,
    })
    const queryClient = useQueryClient()

    const invalidar = () => queryClient.invalidateQueries({ queryKey: ['categorias'] })

    const crearMutation = useMutation({
        mutationFn: crearCategoria,
        onSuccess: invalidar,
    })

    const actualizarMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: { nombre: string; descripcion: string } }) =>
            actualizarCategoria(id, data),
        onSuccess: invalidar,
    })

    const eliminarMutation = useMutation({
        mutationFn: eliminarCategoria,
        onSuccess: invalidar,
    })
    const abrirParaCrear = () => {
        setCategoriaEditando(null)
        setModalAbierto(true)
    }

    const abrirParaEditar = (categoria: Categoria) => {
        setCategoriaEditando(categoria)
        setModalAbierto(true)
    }

    const cerrarModal = () => {
        setModalAbierto(false)
        setCategoriaEditando(null)
    }

    const handleSubmit = async (data: { nombre: string; descripcion: string }) => {
        if (categoriaEditando) {
            await actualizarMutation.mutateAsync({ id: categoriaEditando.id, data })
        } else {
            await crearMutation.mutateAsync(data)
        }
        cerrarModal()
    }
    if (isLoading) return <p className="p-6">Cargando categorías...</p>
    if (isError) return <p className="p-6 text-red-600">Error al cargar las categorías.</p>
    return (

        <main className="mx-auto max-w-5xl p-6">
            <button
                type="button"
                onClick={abrirParaCrear}
                className="mb-6 rounded bg-green-600 px-4 py-2 text-white"
            >
                Nueva categoría
            </button>
            <CategoriaList
                categorias={data ?? []}
                onEdit={abrirParaEditar}
                onDelete={(id) => eliminarMutation.mutate(id)}
            />
            <CategoriaModal
                isOpen={modalAbierto}
                categoriaEditando={categoriaEditando}
                onSubmit={handleSubmit}
                onCancel={cerrarModal}
            />
        </main>
    )
}

export default CategoriasPage