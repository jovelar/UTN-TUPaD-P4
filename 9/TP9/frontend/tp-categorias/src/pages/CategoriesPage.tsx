import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useForm } from '@tanstack/react-form'
import {
    getCoreRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable,
    type ColumnDef,
    type SortingState,
} from '@tanstack/react-table'
import CategoriaList from '../components/CategoriaList'
import CategoriaModal from '../components/CategoriaModal'
import { Cargando, ErrorMensaje, Vacio } from '../components/Estados'
import type { Categoria, CategoriaInput } from '../types/categoria'
import { categoriaService } from '../services/categoriaService'
import { handleApiError } from '../api/handleApiError'
import { useAuthStore } from '../store/authStore'

type CategoriaFormValues = CategoriaInput

const valoresVacios: CategoriaFormValues = { nombre: '', descripcion: '' }
const sinCategorias: Categoria[] = []

const input =
    'mt-1 w-full rounded border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200'

function CategoriesPage() {
    const queryClient = useQueryClient()
    const esAdmin = useAuthStore((s) => s.user?.roles.includes('admin') ?? false)
    const [modalAbierto, setModalAbierto] = useState(false)
    const [categoriaEditando, setCategoriaEditando] = useState<Categoria | null>(null)
    const [sorting, setSorting] = useState<SortingState>([])
    const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 5 })

    // ── Datos: TanStack Query ─────────────────────────────
    const { data = sinCategorias, isLoading, isError } = useQuery({
        queryKey: ['categorias'],
        queryFn: categoriaService.listar,
    })

    const invalidar = () => queryClient.invalidateQueries({ queryKey: ['categorias'] })

    const crearMutation = useMutation({
        mutationFn: categoriaService.crear,
        onSuccess: invalidar,
    })

    const actualizarMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: CategoriaFormValues }) => categoriaService.actualizar(id, data),
        onSuccess: invalidar,
    })

    const eliminarMutation = useMutation({
        mutationFn: categoriaService.eliminar,
        onSuccess: invalidar,
    })

    const cerrarModal = () => {
        setModalAbierto(false)
        setCategoriaEditando(null)
    }

    // ── Formulario: TanStack Form ─────────────────────────
    const form = useForm({
        defaultValues: valoresVacios,
        validators: {
            onSubmit: ({ value }) => {
                if (!value.nombre.trim()) {
                    return { fields: { nombre: 'El nombre es obligatorio' } }
                }
                return undefined
            },
        },
        onSubmit: async ({ value }) => {
            try {
                if (categoriaEditando) {
                    await actualizarMutation.mutateAsync({ id: categoriaEditando.id, data: value })
                } else {
                    await crearMutation.mutateAsync(value)
                }
                cerrarModal()
            } catch {
                // El error queda guardado en la mutación y se muestra en el modal sin cerrarlo
            }
        },
    })

    // ── Modal ─────────────────────────────────────────────
    const abrirParaCrear = () => {
        setCategoriaEditando(null)
        form.reset()
        crearMutation.reset()
        actualizarMutation.reset()
        setModalAbierto(true)
    }

    const abrirParaEditar = (categoria: Categoria) => {
        setCategoriaEditando(categoria)
        form.reset(
            { nombre: categoria.nombre, descripcion: categoria.descripcion },
            { keepDefaultValues: true },
        )
        crearMutation.reset()
        actualizarMutation.reset()
        setModalAbierto(true)
    }

    const eliminar = (categoria: Categoria) => {
        if (window.confirm(`¿Eliminar la categoría "${categoria.nombre}"?`)) {
            eliminarMutation.mutate(categoria.id)
        }
    }

    // ── Tabla: TanStack Table ─────────────────────────────
    const columns: ColumnDef<Categoria>[] = [
        { accessorKey: 'nombre', header: 'Nombre' },
        { accessorKey: 'descripcion', header: 'Descripción' },
    ]
    if (esAdmin) columns.push(
        {
            id: 'acciones',
            header: 'Acciones',
            enableSorting: false,
            cell: ({ row }) => (
                <div className="flex gap-2">
                    <button
                        type="button"
                        onClick={() => abrirParaEditar(row.original)}
                        className="rounded bg-yellow-500 px-3 py-1 text-white hover:bg-yellow-600"
                    >
                        Editar
                    </button>
                    <button
                        type="button"
                        onClick={() => eliminar(row.original)}
                        className="rounded bg-red-600 px-3 py-1 text-white hover:bg-red-700"
                    >
                        Eliminar
                    </button>
                </div>
            ),
        },
    )

    const table = useReactTable({
        data,
        columns,
        state: { sorting, pagination },
        onSortingChange: setSorting,
        onPaginationChange: setPagination,
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
    })

    const errorMutacion = crearMutation.error ?? actualizarMutation.error
    const errorApi = errorMutacion ? handleApiError(errorMutacion) : null

    return (
        <main className="mx-auto max-w-5xl p-6">
            {esAdmin && (
                <button
                    type="button"
                    onClick={abrirParaCrear}
                    className="mb-6 rounded bg-green-600 px-4 py-2 text-white hover:bg-green-700"
                >
                    Nueva categoría
                </button>
            )}

            {eliminarMutation.error && (
                <div className="mb-4">
                    <ErrorMensaje mensaje={handleApiError(eliminarMutation.error)} />
                </div>
            )}

            {isLoading ? (
                <Cargando mensaje="Cargando categorías..." />
            ) : isError ? (
                <ErrorMensaje mensaje="Error al cargar las categorías." />
            ) : data.length === 0 ? (
                <Vacio mensaje="No hay categorías cargadas." />
            ) : (
                <CategoriaList table={table} />
            )}

            <CategoriaModal
                isOpen={modalAbierto}
                titulo={categoriaEditando ? 'Editar categoría' : 'Nueva categoría'}
                errorApi={errorApi}
                onSubmit={form.handleSubmit}
                onCancel={cerrarModal}
            >
                <form.Field name="nombre">
                    {(f) => (
                        <label className="block">
                            Nombre
                            <input
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

                <form.Field name="descripcion">
                    {(f) => (
                        <label className="block">
                            Descripción
                            <input
                                className={input}
                                value={f.state.value}
                                onBlur={f.handleBlur}
                                onChange={(e) => f.handleChange(e.target.value)}
                            />
                        </label>
                    )}
                </form.Field>
            </CategoriaModal>
        </main>
    )
}

export default CategoriesPage