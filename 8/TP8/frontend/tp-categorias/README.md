# Food Store - Frontend - Trabajo Práctico Unidad 8

Aplicación **React + TypeScript + Vite** que implementa el CRUD completo de **Categorías**,
**Productos** e **Ingredientes** consumiendo la API FastAPI de `backend/fastapi-productos`.

## Tecnologías

| Librería | Uso |
|---|---|
| React + TypeScript + Vite | Interfaz, tipado y servidor de desarrollo |
| TanStack Query | Lectura (`useQuery`) y escritura (`useMutation`) de datos; invalida el listado tras cada mutación |
| TanStack Form | Formularios tipados con validación (`useForm`, `form.Field`, `validators`) |
| TanStack Table v8 | Tablas con ordenamiento (`getSortedRowModel`) y paginación (`getPaginationRowModel`) |
| React Router | Rutas `/`, `/categorias`, `/productos` e `/ingredientes` |
| Tailwind CSS | Estilos |

Las peticiones HTTP se hacen con `fetch` nativo, dentro de las funciones de `src/services/`.

## Estructura

```
src/
├── main.tsx              QueryClientProvider + BrowserRouter
├── App.tsx               Solo define las rutas y renderiza el Navbar
├── components/
│   ├── Navbar.tsx
│   ├── Estados.tsx       Estados reutilizables: Cargando, Vacio, ErrorMensaje
│   ├── CategoriaList.tsx     CategoriaModal.tsx
│   ├── ProductoList.tsx      ProductoModal.tsx
│   └── IngredienteList.tsx   IngredienteModal.tsx
├── pages/
│   ├── CategoriasPage.tsx
│   ├── ProductsPage.tsx
│   └── IngredientesPage.tsx
├── services/
│   ├── categoria.ts
│   ├── producto.ts
│   └── ingrediente.ts
└── types/
    ├── categoria.ts      interface Categoria
    ├── producto.ts       interface Producto
    └── ingredientes.ts   interface Ingrediente
```

Cada página contiene toda su lógica: `useQuery`, `useMutation`, el estado del modal (`useState`),
`useForm` (TanStack Form) y `useReactTable` (TanStack Table). Los componentes `*List` reciben la tabla
por props y los `*Modal` reciben el título, el error de la API y los callbacks; los campos del
formulario los define la página.

## Funcionalidades

En cada página (Categorías, Productos e Ingredientes):

- Tabla con ordenamiento por columna (clic en el encabezado) y paginación de 5 filas con los botones
  Anterior y Siguiente.
- Estados de carga, vacío y error.
- Botón de alta que abre el modal vacío; botón **Editar** que abre el modal precargado. El título
  distingue alta de edición.
- Validación del formulario: nombre obligatorio (no solo espacios); en Productos, precio no negativo.
- Si la API responde con un error, el mensaje se muestra en el modal sin cerrarlo.
- Botón **Eliminar** con confirmación; los errores se informan arriba de la tabla.
- Tras crear, editar o eliminar, la tabla se actualiza sin recargar la página.

## Instalación y ejecución

Requiere **Node.js** y **pnpm**, y el backend corriendo en `http://127.0.0.1:8000`.

Desde la carpeta `tp-categorias/`:

```
pnpm install
pnpm dev
```

La aplicación queda en http://localhost:5173 y arranca en `/` (Categorías).

Para compilar y verificar que no haya errores de TypeScript:

```
pnpm build
```
