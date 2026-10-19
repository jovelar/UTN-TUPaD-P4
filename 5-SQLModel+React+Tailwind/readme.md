# Gestor de Productos - Trabajo Práctico Unidad 5

API REST de gestión de catálogo desarrollada con **FastAPI**, **SQLModel** y **PostgreSQL**.
Administra **Categorías**, **Productos** y **Proveedores**. Los datos se persisten en PostgreSQL
mediante sesiones SQLModel (migración del TP de la Unidad 4, que guardaba los datos en memoria).

El frontend (React + TypeScript + Tailwind CSS) está en la carpeta `frontend/` y tiene su propio
`README.md`.

## Estructura del proyecto

```
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── modules/
│       ├── __init__.py
│       ├── categoria/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── routers.py
│       │   ├── schemas.py
│       │   └── services.py
│       ├── producto/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── routers.py
│       │   ├── schemas.py
│       │   └── services.py
│       └── proveedor/
│           ├── __init__.py
│           ├── models.py
│           ├── routers.py
│           ├── schemas.py
│           └── services.py
├── frontend/
├── tests/
│   ├── test_api.http
│   └── TP5 - Productos.postman_collection.json
├── database.py
├── requirements.txt
└── readme.md
```

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Router | `routers.py` | Endpoints HTTP, parámetros de path/query y códigos de estado |
| Service | `services.py` | Reglas de negocio y operaciones con la sesión (`add`, `commit`, `rollback`) |
| Schema | `schemas.py` | Validación Pydantic de request/response |
| Model | `models.py` | Tablas SQLModel (`table=True`) |
| Base de datos | `database.py` | `engine`, `create_db_and_tables()` y `SessionDep` |

Flujo: `main` → `routers` → `services` → `models` (PostgreSQL), con `schemas` validando la entrada y la salida.

## Instalación y ejecución

El proyecto tiene dos partes que se instalan y ejecutan por separado, cada una en su propia terminal.
Al descomprimir el `.zip` **no** vienen `node_modules` ni `.venv`, así que antes de ejecutar hay que
instalar las dependencias de cada parte (pasos completos más abajo):

| Parte | Carpeta | Instalar (solo la primera vez) | Ejecutar | URL |
|---|---|---|---|---|
| Backend (API) | raíz del proyecto | crear la base `tp5` + `python -m venv .venv` + activar + `pip install -r requirements.txt` | `fastapi dev app/main.py` | http://localhost:8000/docs |
| Frontend (pantalla de productos) | `frontend/` | `pnpm install` | `pnpm dev` | http://localhost:5173 |

> Si se ejecuta `pnpm dev` sin haber hecho `pnpm install` aparece el error
> `"vite" no se reconoce como un comando interno o externo`.

> La pantalla de productos **no** la sirve FastAPI. Si abrís http://localhost:8000 solo vas a ver
> una respuesta casi vacía (`{"detail":"Not Found"}`), porque la API no tiene página en `/`.
> Para ver la API usá http://localhost:8000/docs y para ver la pantalla usá http://localhost:5173.

### Backend

Requiere **Python** y **PostgreSQL** instalados, con PostgreSQL corriendo.

```bash
# 1. Crear la base de datos en PostgreSQL
#    (por defecto: usuario postgres, contraseña 1234, base tp5, puerto 5432)
#    Con pgAdmin: clic derecho en Databases > Create > Database... > nombre: tp5
#    O por consola (si psql está en el PATH):
psql -U postgres -c "CREATE DATABASE tp5;"

# 2. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el servidor (desde la raíz del proyecto)
fastapi dev app/main.py
```

La conexión se configura con la variable de entorno `DATABASE_URL`. Si no está definida se usa
`postgresql+psycopg://postgres:1234@localhost:5432/tp5`. Las tablas se crean automáticamente al
iniciar el servidor.

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend

Requiere **Node.js** y **pnpm** instalados (si no tenés pnpm: `npm install -g pnpm`).

```bash
# 1. Entrar a la carpeta del frontend (en otra terminal)
cd frontend

# 2. Instalar dependencias (crea node_modules)
pnpm install

# 3. Levantar el servidor de desarrollo de Vite
pnpm dev
```

Abrir en el navegador: http://localhost:5173

Se muestra la pantalla "Gestor de Productos" con 3 productos hardcodeados y el formulario de alta.
Es solo maquetado: el frontend no llama a la API, así que la pantalla se ve aunque el backend no
esté corriendo.

## Endpoints

### Productos (`/productos`)

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| POST | `/productos/` | 201 | Crear un producto |
| GET | `/productos/` | 200 | Listar productos (`skip`, `limit`) |
| GET | `/productos/{id}` | 200 | Obtener un producto por ID |
| PUT | `/productos/{id}` | 200 | Reemplazo total de un producto |
| DELETE | `/productos/{id}` | 200 | Eliminar un producto |
| GET | `/productos/{id}/stock` | 200 | Consultar stock y alerta de stock mínimo |

### Categorías (`/categorias`)

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| POST | `/categorias/` | 201 | Crear una categoría |
| GET | `/categorias/` | 200 | Listar categorías (`skip`, `limit`) |
| GET | `/categorias/{id}` | 200 | Obtener una categoría por ID |
| PUT | `/categorias/{id}` | 200 | Reemplazo total de una categoría |
| DELETE | `/categorias/{id}` | 200 | Eliminar una categoría |

### Proveedores (`/proveedores`)

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| POST | `/proveedores/` | 201 | Crear un proveedor |
| GET | `/proveedores/` | 200 | Listar proveedores (`skip`, `limit`, `activo`) |
| GET | `/proveedores/{id}` | 200 | Obtener un proveedor por ID |
| PUT | `/proveedores/{id}` | 200 | Reemplazo total de un proveedor |
| DELETE | `/proveedores/{id}` | 200 | Eliminar un proveedor |

Query params de los listados:

| Parámetro | Tipo | Default | Validación / Descripción |
|---|---|---|---|
| skip | int | 0 | ge=0 |
| limit | int | 10 | le=50 (en proveedores además ge=1) |
| activo | Optional[bool] | None | Solo proveedores: true = activos, false = inactivos, omitido = todos |

## Schemas

### Producto

| Campo | Tipo | Requerido | Default | Validación |
|---|---|---|---|---|
| nombre | str | Sí | — | min_length=1, no puede contener solo espacios |
| descripcion | str | Sí | — | — |
| categoria | str | Sí | — | formato `AAA-00` (ej: `MUE-01`) |
| precio | float | Sí | — | ge=0 |
| stock | int | Sí | — | ge=0 |
| stock_minimo | int | Sí | — | ge=0 |
| activo | bool | No | `True` | — |

### Categoría

| Campo | Tipo | Requerido | Default | Validación |
|---|---|---|---|---|
| codigo | str | Sí | — | formato `AAA-00` (ej: `MUE-01`) |
| descripcion | str | Sí | — | min_length=3 |
| activo | bool | No | `True` | — |

### Proveedor

| Campo | Tipo | Requerido | Default | Validación |
|---|---|---|---|---|
| codigo | str | Sí | — | min_length=1 |
| razon_social | str | Sí | — | min_length=3 |
| cuit | str | Sí | — | min_length=11, max_length=15 |
| email | str | No | `""` | — |
| telefono | str | No | `""` | — |
| activo | bool | No | `True` | — |

En cada módulo: `XxxBase` define los campos, `XxxCreate` hereda de `XxxBase`, `XxxRead` agrega `id`
(lo genera la base de datos) y `XxxUpdate` tiene todos los campos opcionales.

## Reglas de negocio

| Regla | Respuesta |
|---|---|
| Datos inválidos según los schemas (tipos, mínimos, obligatoriedad, formato) | 422 |
| El nombre del producto no puede quedar vacío ni contener solo espacios | 422 |
| El precio del producto debe ser mayor o igual a 0 | 422 |
| El `id` del path debe ser mayor a 0 | 422 |
| No se puede repetir el nombre de un producto | 409 |
| No se puede repetir el código de un proveedor | 409 |
| No se puede consultar, actualizar ni eliminar un `id` inexistente | 404 |
| Toda escritura (POST, PUT, DELETE) se persiste en PostgreSQL mediante la sesión SQLModel | — |

Las reglas de negocio (duplicados, alerta de stock) se implementan en `services.py`. Los errores se
devuelven con `HTTPException` en formato `{"detail": "..."}`.

## Pruebas

El archivo `tests/test_api.http` contiene las peticiones para la extensión **REST Client** de VS Code.
Cubre todos los endpoints y escenarios de error: 200, 201, 404, 409 y 422.

1. Levantar el servidor con `fastapi dev app/main.py`.
2. Abrir `tests/test_api.http` y ejecutar las peticiones en orden ("Send Request").

Para Postman, el archivo `tests/TP5 - Productos.postman_collection.json` contiene las mismas peticiones. Se carga en Postman con **Import**.
