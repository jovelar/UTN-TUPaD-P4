# Frontend - Gestor de Productos

Pantalla de productos maquetada con React, TypeScript y Tailwind CSS. Solo maquetado: sin funcionalidad ni llamadas a la API.

## Estructura del proyecto

```
frontend/
├── index.html
├── package.json
├── vite.config.ts
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── index.css
    ├── types/
    │   └── producto.ts
    └── components/
        ├── Navbar.tsx
        ├── ProductoCard.tsx
        ├── ProductoList.tsx
        ├── ProductoForm.tsx
        └── Footer.tsx
```

| Archivo | Responsabilidad |
|---|---|
| `src/types/producto.ts` | Interface `Producto` (id, nombre, descripcion, precio) |
| `src/components/Navbar.tsx` | Barra de navegación con el nombre de la app |
| `src/components/ProductoCard.tsx` | Tarjeta con los datos de un producto |
| `src/components/ProductoList.tsx` | Recibe `Producto[]` y renderiza una `ProductoCard` por producto |
| `src/components/ProductoForm.tsx` | Formulario de alta (sin funcionalidad) |
| `src/components/Footer.tsx` | Pie de página |
| `src/App.tsx` | Arma la pantalla con 3 productos hardcodeados |

## Ejecución

```
pnpm install
pnpm dev
```

Disponible en http://localhost:5173
