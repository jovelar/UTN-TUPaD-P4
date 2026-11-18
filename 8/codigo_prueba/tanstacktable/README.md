# TanStack Table con React y TypeScript

Proyecto de ejemplo de la Unidad 8, Actividad 3 de Programación IV. Muestra una tabla de usuarios que obtiene los datos con TanStack Query y los ordena y pagina con TanStack Table v8.

## Requisitos

- Node.js 20.19 o posterior.
- npm o pnpm.

## Cómo ejecutarlo

```bash
npm install
npm run dev
```

Con pnpm: `pnpm install` y `pnpm dev`. La aplicación queda disponible en la dirección que muestra la consola (por defecto, http://localhost:5173).

Los datos se obtienen de la API pública https://jsonplaceholder.typicode.com/users, por lo que se necesita conexión a internet. Esa API no incluye la edad: el ejemplo la calcula a partir del `id` para tener una columna numérica que ordenar.

## Qué mirar en el código

Todo el ejemplo está en `src/App.tsx`:

- `fetchUsers` obtiene los usuarios y los transforma al tipo `User`.
- `columns` define las columnas con `ColumnDef<User>`.
- `useReactTable` recibe los datos, las columnas, el estado de ordenamiento y de paginación y los modelos de filas (`getCoreRowModel`, `getSortedRowModel` y `getPaginationRowModel`).
- `flexRender` dibuja los encabezados y las celdas.

`src/main.tsx` crea el `QueryClient` y envuelve la aplicación con `QueryClientProvider`.

## Versión de TanStack Table

El proyecto fija `@tanstack/react-table` en la versión 8, la que se usa en el video y en la lectura. La versión 9 cambia la API (por ejemplo, `useReactTable` pasa a llamarse `useTable`), así que no conviene actualizarla sin revisar la documentación.
