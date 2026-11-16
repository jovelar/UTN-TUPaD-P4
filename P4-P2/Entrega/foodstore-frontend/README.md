# Food Store - Frontend (Parcial 2 - Programación IV)

Interfaz web para administrar el catálogo de productos de Food Store. Desarrollada con 

**React**,
**TypeScript**, **Vite** y **Tailwind CSS 4**. Consume la API del proyecto 
`foodstore-backend`.

Basado en el frontend `tp-categorias` de un TP anterior, adaptado a productos.

## Estructura del proyecto

```
foodstore-frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── ProductoList.tsx
│   │   ├── ProductoCard.tsx
│   │   └── ProductoModal.tsx
│   ├── types/
│   │   ├── producto.ts
│   │   ├── categoria.ts
│   │   └── unidadMedida.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── tsconfig.json
└── README.md
```

## Instalación y ejecución

Requiere **Node.js** y el backend corriendo en `http://localhost:8000`.

```
npm install
npm run dev
```

La aplicación queda disponible en http://localhost:5173.

## Funcionalidad

- Listado de productos con precio y stock expresados en su unidad de venta.
- Indicadores de disponibilidad y de stock en cada producto.
- Alta y edición desde un modal, con el selector de unidad cargado desde la API.
- Cambio de disponibilidad y anulación desde cada tarjeta.
- Estados de carga, de error y de lista vacía.

El estado vive en `App.tsx` (`useState` y `useEffect`). Los componentes reciben los datos y las
acciones por props, y las peticiones se hacen con `fetch`.
