# Estado del TP 9

Enunciado: `H:\UTNFRSN2026\UTN-TUPaD-P4\8\TP_Unidad9_v2.pdf`
Lecturas y código de ejemplo: `H:\UTNFRSN2026\UTN-TUPaD-P4\9` (`U9_A1` a `U9_A5`, `codigo_ejemplo\seguridad_jwt_pg`, `codigo_ejemplo\frontend-axios`, `codigo_ejemplo\zustand-demo`)

## Decisiones tomadas

- Se parte del TP8 (`H:\UTNFRSN2026\UTN-TUPaD-P4\8\TP8`), copiado a `TP9\backend` y `TP9\frontend`.
- Pedidos e Ingredientes quedan afuera del TP 9. Aclararlo en el README.
- Orden de trabajo: primero backend (Ejercicio 1), después frontend (Ejercicio 2).

## Hecho

- Copia de backend y frontend a `TP9`, sin `.venv` ni `node_modules`.
- Backend: borradas las carpetas `app\pedido` y `app\ingredientes`, y los archivos `pedidos.http` e `ingredientes.http`.
- Frontend: borrados `IngredientesPage.tsx`, `IngredienteList.tsx`, `IngredienteModal.tsx`, `services\ingrediente.ts` y `types\ingredientes.ts`.
- Frontend: `App.tsx` ya no tiene la ruta ni el import de Ingredientes.

## Pendiente de la limpieza

- `backend\fastapi-productos\app\main.py`:
  - Borrar `from app.pedido.model import Pedido, DetallePedido`.
  - Borrar las dos líneas que quedaron al principio de `create_app` (`app.include_router(pedido_router)` y `app.include_router(ingrediente_router)`).
  - Borrar también `app.include_router(pedido_router)` y `app.include_router(ingrediente_router)` debajo del `add_middleware`.
  - Tiene que quedar solo `producto_router` y `categoria_router`.
- `frontend\tp-categorias\src\components\Navbar.tsx`: borrar `<Link to="/ingredientes">Ingredientes</Link>`.
- Frontend: correr `pnpm install` en `frontend\tp-categorias` (todavía no existe `node_modules`; por eso aparecen imports en rojo).
- Backend: crear el entorno virtual e instalar dependencias en `backend\fastapi-productos`:
  - `python -m venv .venv`
  - `.venv\Scripts\activate`
  - `pip install -r requirements.txt`
- Base de datos: crear una base nueva (por ejemplo `TP-9`) y cambiar el `DATABASE_URL` del `.env`, que hoy apunta a `TP-8`.

## Próximo paso: backend

1. Módulo `app\modules\usuarios\` con `Usuario`, `Rol` y `UsuarioRol` (punto a).
2. Endpoints `/api/v1/auth`: register, token, logout, me y admin de usuarios (punto b).
3. Proteger categorías y productos con `require_role(["admin"])` en escrituras y sesión en lecturas (punto c).
4. CORS con `allow_credentials=True` (punto d).
5. Borrado lógico con `deleted_at` en `Categoria` y `Producto` (punto e).
6. `.env` con `SECRET_KEY`, `.env.example` y `seed.py` con los roles `admin` y `user` (puntos c y f).

## Para modificar más adelante

- Backend: `ProductoCategoria` no tiene `es_principal` (punto c). `requirements.txt` no tiene las dependencias de seguridad.
- Frontend: los servicios usan `fetch`; hay que pasarlos a `axiosInstance`. `ProductsPage` no muestra las categorías de cada producto. Las rutas son `/categorias` y `/productos`; el TP pide `/categories` y `/products`.
- Frontend a crear: `api\axiosInstance.ts`, `store\authStore.ts`, `types\auth.types.ts`, `ProtectedRoute.tsx`, `LoginPage`, `RegisterPage`, `UnauthorizedPage` y `AdminUsersPage`. Instalar `axios` y `zustand`.
