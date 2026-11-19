import { flexRender, type Table } from '@tanstack/react-table'
import type { Producto } from '../types/producto'

type ProductoListProps = {
    table: Table<Producto>
}

const sortLabel: Record<string, string> = { asc: ' ↑', desc: ' ↓' }

function ProductoList({ table }: ProductoListProps) {
    return (
        <div className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
            <table className="w-full border-collapse text-left text-sm">
                <thead className="bg-gray-50">
                    {table.getHeaderGroups().map((headerGroup) => (
                        <tr key={headerGroup.id}>
                            {headerGroup.headers.map((header) => (
                                <th key={header.id} className="border-b border-gray-200 px-4 py-3 font-semibold text-gray-700">
                                    {header.isPlaceholder ? null : (
                                        <button
                                            type="button"
                                            onClick={header.column.getToggleSortingHandler()}
                                            disabled={!header.column.getCanSort()}
                                            className="inline-flex items-center gap-1 disabled:cursor-default"
                                        >
                                            {flexRender(header.column.columnDef.header, header.getContext())}
                                            {sortLabel[header.column.getIsSorted() as string] ?? null}
                                        </button>
                                    )}
                                </th>
                            ))}
                        </tr>
                    ))}
                </thead>
                <tbody>
                    {table.getRowModel().rows.map((row) => (
                        <tr key={row.id} className="hover:bg-gray-50">
                            {row.getVisibleCells().map((cell) => (
                                <td key={cell.id} className="border-b border-gray-100 px-4 py-3">
                                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>

            <nav
                aria-label="Paginación"
                className="flex items-center justify-center gap-4 border-t border-gray-200 bg-gray-50 px-4 py-3"
            >
                <button
                    type="button"
                    onClick={() => table.previousPage()}
                    disabled={!table.getCanPreviousPage()}
                    className="rounded border border-gray-300 bg-white px-3 py-1 disabled:opacity-40"
                >
                    Anterior
                </button>
                <span className="text-sm text-gray-600">
                    Página {table.getState().pagination.pageIndex + 1} de {table.getPageCount() || 1}
                </span>
                <button
                    type="button"
                    onClick={() => table.nextPage()}
                    disabled={!table.getCanNextPage()}
                    className="rounded border border-gray-300 bg-white px-3 py-1 disabled:opacity-40"
                >
                    Siguiente
                </button>
            </nav>
        </div>
    )
}

export default ProductoList