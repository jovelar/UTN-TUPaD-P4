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
import IngredienteList from '../components/IngredienteList'
import IngredienteModal from '../components/IngredienteModal'
import { Cargando, ErrorMensaje, Vacio } from '../components/Estados'
import type { Ingrediente } from '../types/ingredientes'
import {
    actualizarIngrediente,
    crearIngrediente,
    eliminarIngrediente,
    getIngredientes,
    type IngredienteData,
} from '../services/ingrediente'

const valoresVacios: IngredienteData = { nombre: '' }
const sinIngredientes: Ingrediente[] = []

const input =
    'mt-1 w-full rounded border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200'

function IngredientesPage() {
    const queryClient = useQueryClient()
    const [modalAbierto, setModalAbierto] = useState(false)
    const [ingredienteEditando, setIngredienteEditando] = useState<Ingrediente | null>(null)
    const [sorting, setSorting] = useState<SortingState>([])
    const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 5 })

    // ── Datos: TanStack Query ─────────────────────────────
    const { data = sinIngredientes, isLoading, isError } = useQuery({
        queryKey: ['ingredientes'],
        queryFn: getIngredientes,
    })

    const invalidar = () => queryClient.invalidateQueries({ queryKey: ['ingredientes'] })

    const crearMutation = useMutation({
        mutationFn: crearIngrediente,
        onSuccess: invalidar,
    })

    const actualizarMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: IngredienteData }) => actualizarIngrediente(id, data),
        onSuccess: invalidar,
    })

    const eliminarMutation = useMutation({
        mutationFn: eliminarIngrediente,
        onSuccess: invalidar,
    })

    const cerrarModal = () => {
        setModalAbierto(false)
        setIngredienteEditando(null)
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
                if (ingredienteEditando) {
                    await actualizarMutation.mutateAsync({ id: ingredienteEditando.id, data: value })
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
        setIngredienteEditando(null)
        form.reset()
        crearMutation.reset()
        actualizarMutation.reset()
        setModalAbierto(true)
    }

    const abrirParaEditar = (ingrediente: Ingrediente) => {
        setIngredienteEditando(ingrediente)
        form.reset({ nombre: ingrediente.nombre }, { keepDefaultValues: true })
        crearMutation.reset()
        actualizarMutation.reset()
        setModalAbierto(true)
    }

    const eliminar = (ingrediente: Ingrediente) => {
        if (window.confirm(`¿Eliminar el ingrediente "${ingrediente.nombre}"?`)) {
            eliminarMutation.mutate(ingrediente.id)
        }
    }

    // ── Tabla: TanStack Table ─────────────────────────────
    const columns: ColumnDef<Ingrediente>[] = [
        { accessorKey: 'nombre', header: 'Nombre' },
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
    ]

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

    const errorApi = (crearMutation.error ?? actualizarMutation.error)?.message ?? null

    return (
        <main className="mx-auto max-w-5xl p-6">
            <button
                type="button"
                onClick={abrirParaCrear}
                className="mb-6 rounded bg-green-600 px-4 py-2 text-white hover:bg-green-700"
            >
                Nuevo ingrediente
            </button>

            {eliminarMutation.error && (
                <div className="mb-4">
                    <ErrorMensaje mensaje={eliminarMutation.error.message} />
                </div>
            )}

            {isLoading ? (
                <Cargando mensaje="Cargando ingredientes..." />
            ) : isError ? (
                <ErrorMensaje mensaje="Error al cargar los ingredientes." />
            ) : data.length === 0 ? (
                <Vacio mensaje="No hay ingredientes cargados." />
            ) : (
                <IngredienteList table={table} />
            )}

            <IngredienteModal
                isOpen={modalAbierto}
                titulo={ingredienteEditando ? 'Editar ingrediente' : 'Nuevo ingrediente'}
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
            </IngredienteModal>
        </main>
    )
}

export default IngredientesPage