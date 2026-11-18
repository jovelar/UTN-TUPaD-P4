import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  type ColumnDef,
  type SortingState,
} from "@tanstack/react-table";

export type User = {
  id: number;
  name: string;
  email: string;
  age: number;
};

type ApiUser = {
  id: number;
  name: string;
  email: string;
};

async function fetchUsers(): Promise<User[]> {
  const res = await fetch("https://jsonplaceholder.typicode.com/users");
  if (!res.ok) throw new Error("No se pudieron cargar los usuarios");
  const data: ApiUser[] = await res.json();
  return data.map((u) => ({
    id: u.id,
    name: u.name,
    email: u.email,
    age: ((u.id * 7) % 43) + 18,
  }));
}

const columns: ColumnDef<User>[] = [
  { accessorKey: "id", header: "ID" },
  { accessorKey: "name", header: "Nombre" },
  { accessorKey: "email", header: "Email" },
  { accessorKey: "age", header: "Edad" },
];

/** Arreglo vacío fijo: mientras no hay datos, la tabla recibe siempre la misma referencia */
const sinUsuarios: User[] = [];

const sortLabel: Record<string, string> = { asc: " ↑", desc: " ↓" };

/** Anchos fijos por columna (evita que cambien al paginar) */
const colWidth: Record<string, string> = {
  id: "w-[9%]",
  name: "w-[26%]",
  email: "w-[55%] break-words [overflow-wrap:anywhere]",
  age: "w-[10%]",
};

const btnClass =
  "cursor-pointer rounded-md border border-[var(--border)] bg-[var(--social-bg)] px-4 py-2 text-[15px] text-[var(--text-h)] transition-[box-shadow,border-color] hover:border-[var(--accent-border)] hover:shadow-[var(--shadow)] disabled:cursor-not-allowed disabled:opacity-45";

const cellBase =
  "border-b border-[var(--border)] px-4 py-3 text-left align-top";

function App() {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 5 });

  const {
    data = sinUsuarios,
    isPending,
    isError,
    error,
  } = useQuery({
    queryKey: ["users"],
    queryFn: fetchUsers,
  });

  const table = useReactTable({
    data,
    columns,
    state: { sorting, pagination },
    onSortingChange: setSorting,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <main className="max-w-full px-6 pb-12 pt-8 text-left">
      <header className="mb-6">
        <h1 className="mb-2 mt-0 !text-3xl font-medium tracking-tight text-[var(--text-h)] lg:!text-4xl">
          Usuarios
        </h1>
        <p className="mb-6 text-base text-[var(--text)]">
          TanStack Query (datos) + TanStack Table (ordenación y paginación)
        </p>
      </header>

      {isPending && (
        <p className="m-0 text-[var(--text)]">Cargando usuarios…</p>
      )}
      {isError && (
        <p className="m-0 text-rose-500" role="alert">
          {(error as Error).message}
        </p>
      )}

      {!isPending && !isError && (
        <div className="overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--bg)] shadow-[var(--shadow)]">
          <table className="w-full table-fixed border-collapse text-[15px]">
            <thead>
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => {
                    const w = colWidth[header.column.id] ?? "";
                    return (
                      <th
                        key={header.id}
                        className={`bg-[var(--code-bg)] font-semibold text-[var(--text-h)] ${cellBase} ${w}`}
                      >
                        {header.isPlaceholder ? null : (
                          <button
                            type="button"
                            className="inline-flex w-full items-center gap-1 border-0 bg-transparent p-0 text-left font-inherit text-inherit cursor-pointer disabled:cursor-default"
                            onClick={header.column.getToggleSortingHandler()}
                            disabled={!header.column.getCanSort()}
                          >
                            {flexRender(
                              header.column.columnDef.header,
                              header.getContext(),
                            )}
                            {header.column.getIsSorted()
                              ? sortLabel[header.column.getIsSorted() as string]
                              : null}
                          </button>
                        )}
                      </th>
                    );
                  })}
                </tr>
              ))}
            </thead>
            <tbody>
              {table.getRowModel().rows.map((row) => (
                <tr
                  key={row.id}
                  className="hover:bg-[var(--social-bg)] last:[&>td]:border-b-0"
                >
                  {row.getVisibleCells().map((cell) => {
                    const w = colWidth[cell.column.id] ?? "";
                    return (
                      <td key={cell.id} className={`${cellBase} ${w}`}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext(),
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>

          <nav
            className="flex items-center justify-center gap-4 border-t border-[var(--border)] bg-[var(--code-bg)] px-4 py-4"
            aria-label="Paginación"
          >
            <button
              type="button"
              className={btnClass}
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              Anterior
            </button>
            <span className="min-w-[140px] text-center text-sm text-[var(--text)]">
              Página {table.getState().pagination.pageIndex + 1} de{" "}
              {table.getPageCount() || 1}
            </span>
            <button
              type="button"
              className={btnClass}
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              Siguiente
            </button>
          </nav>
        </div>
      )}
    </main>
  );
}

export default App;
