# API Productos y Categorías - Trabajo Práctico Unidad 7

API REST desarrollada con **FastAPI**, **SQLModel** y **PostgreSQL**. Administra **Categorías**,
**Productos** y la relación muchos a muchos **ProductoCategoria**.

El CRUD de Categorías se consume desde el frontend (React + TypeScript + Tailwind CSS), que está en
`frontend/tp-categorias`. Los endpoints de Productos y ProductoCategoria se demuestran con el archivo
`productos.http` (REST Client).

## Estructura del proyecto

```
fastapi-productos/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── categoria/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   └── service.py
│   └── producto/
│       ├── __init__.py
│       ├── model.py
│       ├── router.py
│       ├── schema.py
│       └── service.py
├── .env
├── .gitignore
├── productos.http
├── requirements.txt
└── readme.md
```

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Router | `router.py` | Endpoints HTTP, parámetros de path/query y códigos de estado |
| Service | `service.py` | Reglas de negocio y operaciones con la sesión (`add`, `commit`, `rollback`) |
| Schema | `schema.py` | Validación Pydantic de request/response |
| Model | `model.py` | Tablas SQLModel (`table=True`) |
| Base de datos | `core/database.py` | `engine`, `create_db_and_tables()` y `SessionDep` |

## Instalación y ejecución

Requiere **Python** y **PostgreSQL** instalados, con PostgreSQL corriendo.

1. Crear la base de datos `TP-7` en PostgreSQL (con pgAdmin: clic derecho en Databases > Create >
   Database... > nombre: `TP-7`).

2. Crear el archivo `.env` en la carpeta `fastapi-productos/` con la conexión a la base:

   ```
   DATABASE_URL=postgresql+psycopg2://postgres:TU_CONTRASEÑA@localhost:5432/TP-7
   ```

   Si no existe el `.env` se usa `postgresql+psycopg2://postgres:1234@localhost:5432/TP-7`.

3. Crear el entorno virtual e instalar las dependencias:

   ```
   python -m venv .venv
   .venv\Scripts\python -m pip install -r requirements.txt
   ```

4. Ejecutar el servidor desde la carpeta `fastapi-productos/`:

   ```
   .venv\Scripts\python -m fastapi dev app/main.py
   ```

Las tablas se crean automáticamente al iniciar el servidor.

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

CORS está habilitado para `http://localhost:5173`, el origen del frontend.

## Endpoints

### Categorías (`/categorias`)

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| POST | `/categorias/` | 201 | Crear una categoría |
| GET | `/categorias/` | 200 | Listar categorías (`skip`, `limit`) |
| GET | `/categorias/{id}` | 200 | Obtener una categoría por ID |
| PUT | `/categorias/{id}` | 200 | Reemplazo total de una categoría |
| DELETE | `/categorias/{id}` | 204 | Eliminar una categoría |

### Productos (`/productos`)

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| POST | `/productos/` | 201 | Crear un producto |
| GET | `/productos/` | 200 | Listar productos (`skip`, `limit`) |
| GET | `/productos/{id}` | 200 | Obtener un producto por ID |
| PUT | `/productos/{id}` | 200 | Reemplazo total de un producto |
| DELETE | `/productos/{id}` | 204 | Eliminar un producto |

### ProductoCategoria (`/productos/{id}/categorias`)

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| POST | `/productos/{id}/categorias` | 201 | Asignar a un producto la categoría indicada en el cuerpo (`categoria_id`) |
| GET | `/productos/{id}/categorias` | 200 | Listar las categorías de un producto |
| DELETE | `/productos/{id}/categorias/{categoria_id}` | 200 | Quitar una categoría de un producto |

## Schemas

### Categoría

| Campo | Tipo | Requerido | Default | Validación |
|---|---|---|---|---|
| nombre | str | Sí | — | min_length=1 |
| descripcion | str | Sí | — | min_length=3 |

### Producto

| Campo | Tipo | Requerido | Default | Validación |
|---|---|---|---|---|
| nombre | str | Sí | — | min_length=1 |
| descripcion | str | Sí | — | — |
| precio_base | float | Sí | — | ge=0 |
| imagenes_url | list[str] | No | `[]` | — |
| disponible | bool | No | `True` | — |

### ProductoCategoria

| Campo | Tipo | Descripción |
|---|---|---|
| producto_id | int | Clave foránea a `producto.id` (clave primaria compuesta) |
| categoria_id | int | Clave foránea a `categoria.id` (clave primaria compuesta) |

## Reglas de negocio

| Regla | Respuesta |
|---|---|
| Datos inválidos según los schemas | 422 |
| El `id` del path debe ser mayor a 0 | 422 |
| Consultar, actualizar o eliminar un `id` inexistente | 404 |
| Asignar una categoría o un producto inexistente | 404 |
| Asignar una categoría que el producto ya tiene | 409 |
| Quitar una categoría que el producto no tiene | 404 |

## Pruebas

El archivo `productos.http` contiene las peticiones para la extensión **REST Client** de VS Code. Cubre
Categorías, Productos y ProductoCategoria, incluidos los casos de error.

1. Levantar el servidor.
2. Abrir `productos.http` y ejecutar las peticiones en orden ("Send Request").
