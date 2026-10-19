# Estado del TP Integrador Unidad 5

Última actualización: 19/10/2026.
**Borrar este archivo antes de armar el .zip de entrega.**

## Reglas de trabajo
- No inventar nada: todo sale del enunciado (`TP Integrador Unidad 5-1.pdf`) y de los PDF de la carpeta.
- Hacer lo que pide el TP y nada más.
- El asistente no modifica archivos del proyecto: indica los cambios y el usuario los aplica.
- Cada indicación: ruta del archivo, número de línea, función, y el código completo. Los bloques de código contienen solo lo que va en el archivo.

## Decisiones tomadas
| Tema | Decisión |
|---|---|
| Alcance de la migración | Se migraron los 3 módulos: producto, categoría y proveedor |
| Campo `descripcion` en Producto | Se agregó al backend (models y schemas) para cumplir RN-07 |
| DELETE (A2) | Se agregó `DELETE /{id}` y se borró `PUT /{id}/desactivar` en los 3 módulos |
| Categorías iniciales (B1) | Se borraron del código; se cargan con POST (pruebas 1.1 y 1.2 de `tests/test_api.http`) |
| Evento de arranque | `@app.on_event("startup")` en `app/main.py` (como dice el PDF; muestra un aviso de deprecated, funciona igual) |
| Herramienta de pruebas | REST Client de VS Code con `tests/test_api.http` (RN-11 acepta .http) |
| Linter del frontend | ESLint |
| Carpeta del frontend | `frontend/`, dentro de la carpeta del TP. El backend queda en la raíz |
| Instalar paquetes del frontend | Con `pnpm` (el PDF de React dice usar solo pnpm) |

## Parte A: backend (TERMINADA)
- PostgreSQL 18, usuario `postgres`, base `tp5`, puerto 5432. Conexión en `database.py` línea 8.
- Cada módulo (`app/modules/producto`, `categoria`, `proveedor`) tiene `models.py` (nuevo), `schemas.py`, `services.py` (usa `session`) y `routers.py` (usa `SessionDep`).
- `app/main.py` importa los 3 models y crea las tablas al arrancar.
- Todas las pruebas de `tests/test_api.http` dieron el código esperado.
- Persistencia verificada: los datos siguen después de reiniciar el servidor (HU-01).
- Swagger `/docs` y `/redoc` verificados (HU-03).

Para levantar el backend (en cmd, desde la carpeta del TP):
```
.venv\Scripts\activate.bat
fastapi dev app/main.py
```

## Parte B: frontend (EN CURSO)
Hecho:
- e) Proyecto creado con `pnpm create vite frontend --template react-ts --eslint --no-immediate --no-interactive`.
- f) Tailwind instalado (`pnpm add tailwindcss @tailwindcss/vite`), plugin en `frontend/vite.config.ts`, y `frontend/src/index.css` contiene solo `@import "tailwindcss";`.

Para levantar el frontend (en cmd, dentro de `frontend`):
```
pnpm install
pnpm dev
```

Falta, en este orden:
1. g) `frontend/src/types/producto.ts` con la interface `Producto` (id, nombre, descripcion, precio). Contenido:
   ```ts
   export interface Producto {
     id: number
     nombre: string
     descripcion: string
     precio: number
   }
   ```
2. h) Componentes en `frontend/src/components/`: `Navbar.tsx`, `ProductoCard.tsx`, `ProductoList.tsx`, `ProductoForm.tsx`, `Footer.tsx`. Props tipadas, sin `any`, sin hooks (sin useState ni useEffect), export nombrado, arrow functions.
3. i) `frontend/src/App.tsx` con al menos 3 productos hardcodeados, layout con grid/flex.
4. j) Verificar que `pnpm dev` corre sin errores de TypeScript ni en la consola.
5. README del frontend con la estructura del proyecto (HU-06).

## Entrega
1. Borrar `.venv`, `frontend/node_modules`, `__pycache__`, `pruebas_postman.md` y este archivo (`estado_tp.md`).
2. Comprimir todo en un único `.zip`.
