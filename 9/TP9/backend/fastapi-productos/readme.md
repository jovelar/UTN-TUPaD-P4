# API Food Store - Trabajo Práctico Unidad 8

API REST desarrollada con **FastAPI**, **SQLModel** y **PostgreSQL**. Administra **Categorías**,
**Productos**, la relación muchos a muchos **ProductoCategoria**, **Ingredientes** y **Pedidos** con
sus **DetallePedido**.

Los CRUD de Categorías, Productos e Ingredientes se consumen desde el frontend (React + TypeScript +
TanStack Query/Form/Table + Tailwind CSS), que está en `frontend/tp-categorias`. Los CRUD de Pedido y
DetallePedido se demuestran con REST Client (`pedidos.http`).

## Estructura del proyecto

```
fastapi-productos/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── repository.py
│   │   └── unit_of_work.py
│   ├── categoria/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   └── service.py
│   ├── producto/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   └── service.py
│   ├── ingredientes/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   └── service.py
│   └── pedido/
│       ├── __init__.py
│       ├── model.py
│       ├── schema.py
│       ├── repository.py
│       ├── unit_of_work.py
│       ├── service.py
│       └── router.py
├── .env
├── .gitignore
├── productos.http
├── pedidos.http
├── ingredientes.http
├── requirements.txt
└── readme.md
```

### Categoría, Producto e Ingrediente

Mantienen la estructura del TP de la unidad 7:

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Router | `router.py` | Endpoints HTTP, parámetros de path/query y códigos de estado |
| Service | `service.py` | Operaciones con la sesión (`add`, `commit`, `rollback`) |
| Schema | `schema.py` | Validación Pydantic de request/response |
| Model | `model.py` | Tablas SQLModel (`table=True`) |

### Pedido (Models-Schemas-Repository-UoW-Service-Router)

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Model | `pedido/model.py` | Tablas `Pedido` y `DetallePedido` |
| Schema | `pedido/schema.py` | Validación de entrada y formato de salida |
| Repository | `core/repository.py`, `pedido/repository.py` | Consultas a la base. Usa `flush()`, nunca `commit()` |
| Unit of Work | `core/unit_of_work.py`, `pedido/unit_of_work.py` | Abre la transacción y expone los repositorios de pedidos, detalles y productos. Hace `commit` si no hubo errores o `rollback` si hubo una excepción |
| Service | `pedido/service.py` | Reglas de negocio. Ejecuta cada caso de uso dentro del Unit of Work y lanza `PedidoNoEncontrado` / `ProductoNoEncontrado` |
| Router | `pedido/router.py` | Endpoints HTTP. Traduce las excepciones del servicio a 404 |

El alta de un pedido es atómica: si un detalle referencia un producto inexistente, el `rollback`
descarta también el pedido.

### Base de datos

`core/database.py` define el `engine`, `create_db_and_tables()` y `SessionDep`.

## Instalación y ejecución

Requiere **Python** y **PostgreSQL** instalados, con PostgreSQL corriendo.

1. Crear la base de datos `TP-8` en PostgreSQL (con pgAdmin: clic derecho en Databases > Create >
   Database... > nombre: `TP-8`).

2. Crear el archivo `.env` en la carpeta `fastapi-productos/` con la conexión a la base:

   ```
   DATABASE_URL=postgresql+psycopg2://postgres:TU_CONTRASEÑA@localhost:5432/TP-8
   ```

   Si no existe el `.env` se usa `postgresql+psycopg2://postgres:1234@localhost:5432/TP-8`.

3. Crear el entorno virtual e instalar las dependencias:

   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Ejecutar el servidor desde la carpeta `fastapi-productos/`:

   ```
   python -m fastapi dev app/main.py
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

### Ingredientes (`/ingredientes`)

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| POST | `/ingredientes/` | 201 | Crear un ingrediente |
| GET | `/ingredientes/` | 200 | Listar ingredientes (`skip`, `limit`) |
| GET | `/ingredientes/{id}` | 200 | Obtener un ingrediente por ID |
| PUT | `/ingredientes/{id}` | 200 | Reemplazo total de un ingrediente |
| DELETE | `/ingredientes/{id}` | 204 | Eliminar un ingrediente |

### Pedidos (`/pedidos`)

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| POST | `/pedidos/` | 201 | Crear un pedido con sus detalles en una sola transacción |
| GET | `/pedidos/` | 200 | Listar los pedidos no eliminados |
| GET | `/pedidos/{id}` | 200 | Obtener un pedido con sus detalles |
| PUT | `/pedidos/{id}` | 200 | Actualizar el estado del pedido |
| DELETE | `/pedidos/{id}` | 204 | Borrado lógico (completa `deleted_at`) |

## Schemas

### Categoría

| Campo | Tipo | Requerido | Default | Validación |
|---|---|---|---|---|
| nombre | str | Sí | — | Se quitan los espacios de los extremos; al menos 1 carácter |
| descripcion | str | No | `""` | — |

### Producto

| Campo | Tipo | Requerido | Default | Validación |
|---|---|---|---|---|
| nombre | str | Sí | — | Se quitan los espacios de los extremos; al menos 1 carácter |
| descripcion | str | Sí | — | — |
| precio_base | float | Sí | — | ge=0 |
| imagenes_url | list[str] | No | `[]` | — |
| disponible | bool | No | `True` | — |

### ProductoCategoria

| Campo | Tipo | Descripción |
|---|---|---|
| producto_id | int | Clave foránea a `producto.id` (clave primaria compuesta) |
| categoria_id | int | Clave foránea a `categoria.id` (clave primaria compuesta) |

### Ingrediente

| Campo | Tipo | Requerido | Validación |
|---|---|---|---|
| nombre | str | Sí | Se quitan los espacios de los extremos; al menos 1 carácter |

### Pedido

| Campo | Tipo | Descripción |
|---|---|---|
| id | int | Autoincremental |
| fecha | datetime | Asignada por el backend al crear |
| estado | str | `PENDIENTE`, `CONFIRMADO`, `ENTREGADO` o `CANCELADO`. Al crear: `PENDIENTE` |
| total | float | Suma de `cantidad * precio_unitario` de los detalles |
| deleted_at | datetime \| null | Se completa en el borrado lógico. No se expone en las respuestas |

### DetallePedido

| Campo | Tipo | Descripción |
|---|---|---|
| pedido_id | int | Clave foránea a `pedido.id` (clave primaria compuesta) |
| producto_id | int | Clave foránea a `producto.id` (clave primaria compuesta) |
| cantidad | int | Mayor o igual a 1 |
| precio_unitario | float | `precio_base` del producto al crear el pedido |

### Cuerpos de Pedido

- `POST /pedidos/`: `{ "detalles": [ { "producto_id": 1, "cantidad": 2 } ] }`. Al menos un detalle,
  `cantidad >= 1` y sin `producto_id` repetidos.
- `PUT /pedidos/{id}`: `{ "estado": "CONFIRMADO" }`.

## Reglas de negocio

| Regla | Respuesta |
|---|---|
| Datos inválidos según los schemas | 422 |
| Nombre de categoría, producto o ingrediente vacío o solo espacios | 422 |
| `precio_base` negativo | 422 |
| El `id` del path debe ser mayor a 0 (Categoría, Producto, Ingrediente) | 422 |
| Consultar, actualizar o eliminar un `id` inexistente | 404 |
| Asignar una categoría o un producto inexistente | 404 |
| Asignar una categoría que el producto ya tiene | 409 |
| Quitar una categoría que el producto no tiene | 404 |
| Pedido sin detalles, con cantidad menor que 1 o con un producto repetido | 422 |
| Estado de pedido fuera de los permitidos | 422 |
| Pedido con un producto inexistente (no se guarda nada) | 404 |
| Operar sobre un pedido inexistente o eliminado | 404 |

## Pruebas

Los archivos `.http` contienen las peticiones para la extensión **REST Client** de VS Code, incluidos
los casos de error:

| Archivo | Cubre |
|---|---|
| `productos.http` | Categorías, Productos y ProductoCategoria |
| `pedidos.http` | Pedidos y DetallePedido (201, 200, 204, 422 y 404) |
| `ingredientes.http` | Ingredientes (201, 200, 204, 422 y 404) |

1. Levantar el servidor.
2. Abrir el archivo `.http` y ejecutar las peticiones en orden ("Send Request").
