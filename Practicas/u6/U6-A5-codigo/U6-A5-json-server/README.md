# U6 · Actividad 5 — JSON Server y consumo de APIs REST

Código de apoyo de la Actividad 5 de la Unidad 6 de Programación IV (React + TypeScript).
Levanta una API REST simulada con JSON Server a partir de `db.json` y la consume desde React
con `fetch`, usando los cinco métodos: GET, POST, PUT, PATCH y DELETE.

## Qué muestra cada archivo

- `db.json`: la colección `categorias`, con los datos de ejemplo (Electrónica, Hogar).
- `src/services/categoriasApi.ts`: la capa de servicios, con una función por operación
  (`getCategorias`, `getCategoriaPorId`, `createCategoria`, `updateCategoria`,
  `patchCategoria` y `deleteCategoria`).
- `src/App.tsx`: carga las categorías al montar (`useEffect` con dependencias vacías), maneja
  los estados de carga y de error, y muestra una tabla con Editar, Renombrar (PATCH) y
  Eliminar.
- `src/hooks/useForm.ts`, `src/hooks/useCategoriasForm.ts` y
  `src/components/CategoriaModal.tsx`: el mismo hook y el mismo modal de la Actividad 4,
  reutilizados.

## Cómo ejecutarlo

Hacen falta **dos terminales**:

```bash
pnpm install

# Terminal 1: la API simulada (http://localhost:3000)
pnpm server

# Terminal 2: la aplicación React (http://localhost:5173)
pnpm dev
```

Para verificar que compila: `pnpm build`.

## Versión de JSON Server

`json-server` está fijado en la versión exacta `0.17.4`. Sin fijar la versión, `npm` o `pnpm`
instalan la `1.0.0-beta`, que trata todos los `id` como texto (`"id": "1"` en vez de
`"id": 1`) y rompe comparaciones como `categoria.id === 1`.
