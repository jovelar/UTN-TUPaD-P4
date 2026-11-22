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
import ProductoList from '../components/ProductoList'
import ProductoModal from '../components/ProductoModal'
import { Cargando, ErrorMensaje, Vacio } from '../components/Estados'
import type { Producto, ProductoInput } from '../types/producto'
import { productoService } from '../services/productoService'
import { handleApiError } from '../api/handleApiError'
import { useAuthStore } from '../store/authStore'

const valoresVacios: ProductoInput = {
    nombre: '',
    descripcion: '',
    precio_base: 0,
    imagenes_url: [],
    disponible: true,
}
const sinProductos: Producto[] = []

const input =
    'mt-1 w-full rounded border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200'

function ProductsPage() {
    const queryClient = useQueryClient()
    const esAdmin = useAuthStore((s) => s.user?.roles.includes('admin') ?? false)
    const [modalAbierto, setModalAbierto] = useState(false)
    const [productoEditando, setProductoEditando] = useState<Producto | null>(null)
    const [sorting, setSorting] = useState<SortingState>([])
    const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 5 })

    // ── Datos: TanStack Query ─────────────────────────────
    const { data = sinProductos, isLoading, isError } = useQuery({
        queryKey: ['productos'],
        queryFn: productoService.listar,
    })

    const invalidar = () => queryClient.invalidateQueries({ queryKey: ['productos'] })

    const crearMutation = useMutation({
        mutationFn: productoService.crear,
        onSuccess: invalidar,
    })

    const actualizarMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: ProductoInput }) => productoService.actualizar(id, data),
        onSuccess: invalidar,
    })

    const eliminarMutation = useMutation({
        mutationFn: productoService.eliminar,
        onSuccess: invalidar,
    })

    const cerrarModal = () => {
        setModalAbierto(false)
        setProductoEditando(null)
    }

    // ── Formulario: TanStack Form ─────────────────────────
    const form = useForm({
        defaultValues: valoresVacios,
        validators: {
            onSubmit: ({ value }) => {
                if (!value.nombre.trim()) {
                    return { fields: { nombre: 'El nombre es obligatorio' } }
                }
                if (value.precio_base < 0) {
                    return { fields: { precio_base: 'El precio no puede ser negativo' } }
                }
                return undefined
            },
        },
        onSubmit: async ({ value }) => {
            try {
                if (productoEditando) {
                    await actualizarMutation.mutateAsync({ id: productoEditando.id, data: value })
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
        setProductoEditando(null)
        form.reset()
        crearMutation.reset()
        actualizarMutation.reset()
        setModalAbierto(true)
    }

    const abrirParaEditar = (producto: Producto) => {
        setProductoEditando(producto)
        form.reset(
            {
                nombre: producto.nombre,
                descripcion: producto.descripcion ?? '',
                precio_base: producto.precio_base,
                imagenes_url: producto.imagenes_url,
                disponible: producto.disponible,
            },
            { keepDefaultValues: true },
        )
        crearMutation.reset()
        actualizarMutation.reset()
        setModalAbierto(true)
    }

    const eliminar = (producto: Producto) => {
        if (window.confirm(`¿Eliminar el producto "${producto.nombre}"?`)) {
            eliminarMutation.mutate(producto.id)
        }
    }

    // ── Tabla: TanStack Table ─────────────────────────────
    const columns: ColumnDef<Producto>[] = [
        { accessorKey: 'nombre', header: 'Nombre' },
        { accessorKey: 'descripcion', header: 'Descripción' },
        {
            accessorKey: 'precio_base',
            header: 'Precio',
            cell: ({ getValue }) => `$ ${getValue<number>().toFixed(2)}`,
        },
        {
            accessorKey: 'disponible',
            header: 'Disponible',
            cell: ({ getValue }) => (getValue<boolean>() ? 'Sí' : 'No'),
        },
        {
            id: 'categorias',
            header: 'Categorías',
            enableSorting: false,
            cell: ({ row }) =>
                row.original.categorias
                    .map((c) => (c.es_principal ? `${c.nombre} (principal)` : c.nombre))
                    .join(', ') || '—',
        },
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
                    Nuevo producto
                </button>
            )}

            {eliminarMutation.error && (
                <div className="mb-4">
                    <ErrorMensaje mensaje={handleApiError(eliminarMutation.error)} />
                </div>
            )}

            {isLoading ? (
                <Cargando mensaje="Cargando productos..." />
            ) : isError ? (
                <ErrorMensaje mensaje="Error al cargar los productos." />
            ) : data.length === 0 ? (
                <Vacio mensaje="No hay productos cargados." />
            ) : (
                <ProductoList table={table} />
            )}

            <ProductoModal
                isOpen={modalAbierto}
                titulo={productoEditando ? 'Editar producto' : 'Nuevo producto'}
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
                                value={f.state.value ?? ''}
                                onBlur={f.handleBlur}
                                onChange={(e) => f.handleChange(e.target.value)}
                            />
                        </label>
                    )}
                </form.Field>

                <form.Field name="precio_base">
                    {(f) => (
                        <label className="block">
                            Precio
                            <input
                                type="number"
                                min={0}
                                step="0.01"
                                className={input}
                                value={f.state.value}
                                onBlur={f.handleBlur}
                                onChange={(e) => f.handleChange(Number(e.target.value))}
                            />
                            {f.state.meta.errors.map((err) => (
                                <p key={String(err)} className="mt-1 text-xs text-red-500">{err}</p>
                            ))}
                        </label>
                    )}
                </form.Field>

                <form.Field name="disponible">
                    {(f) => (
                        <label className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                checked={f.state.value}
                                onBlur={f.handleBlur}
                                onChange={(e) => f.handleChange(e.target.checked)}
                            />
                            Disponible
                        </label>
                    )}
                </form.Field>
            </ProductoModal>
        </main>
    )
}

export default ProductsPage