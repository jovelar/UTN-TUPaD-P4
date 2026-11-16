# Food Store - Backend (Parcial 2 - Programación IV)

API REST desarrollada con **FastAPI**, **SQLModel** y **PostgreSQL**. Administra el catálogo de
Food Store: **Unidades de medida**, **Categorías**, **Productos** y la relación muchos a muchos
**ProductoCategoria**.


Se reutilizo codigo de trabajos anteriores. Basado en el backend del TP de la Unidad 6, adaptado a la consigna del parcial.

## Estructura del proyecto

```
foodstore-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── seed.py
│   └── modules/
│       ├── unidades_medida/   # model · router
│       ├── categorias/        # router · model · schema · service
│       └── productos/         # router · model · schema · service
├── tests/
│   ├── productos.http
│   └── relaciones.http
├── requirements.txt
└── README.md
```

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Router | `router.py` | Endpoints HTTP, parámetros de path/query y códigos de estado |
| Service | `service.py` | Reglas de negocio y operaciones con la sesión |
| Schema | `schema.py` | Validación Pydantic de request/response |
| Model | `model.py` | Tablas SQLModel (`table=True`) |
| Base de datos | `core/database.py` | `engine`, `create_db_and_tables()` y `SessionDep` |
| Seed | `core/seed.py` | Carga inicial de las unidades de medida |

## Instalación y ejecución

Requiere **Python 3.12 o superior** y **PostgreSQL 15 o superior** corriendo.

1. Crear la base de datos `P4-P2` en PostgreSQL (con pgAdmin: clic derecho en Databases > Create >
   Database... > nombre: `P4-P2`).

2. Configurar la cadena de conexión. Está definida en `app/core/database.py`:

   ```
   postgresql+psycopg://postgres:1234@localhost:5432/P4-P2
   ```

   Para usar otro usuario o contraseña se puede editar ese valor, o crear un archivo `.env` en la
   carpeta `foodstore-backend/` con:

   ```
   DATABASE_URL=postgresql+psycopg://postgres:TU_CONTRASEÑA@localhost:5432/P4-P2
   ```

3. Crear el entorno virtual e instalar las dependencias:

   ```
   python -m venv .venv
   .venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

4. Ejecutar el servidor desde la carpeta `foodstore-backend/`:

   ```
   fastapi dev app/main.py
   ```

Al iniciar se crean las tablas y se cargan las seis unidades de medida si la tabla está vacía.

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

CORS está habilitado para `http://localhost:5173`, el origen del frontend.

## Endpoints

Todos usan el prefijo `/api/v1`.

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| GET | `/unidades-medida` | 200 | Listar las unidades de medida |
| POST | `/categorias` | 201 | Crear una categoría |
| GET | `/categorias` | 200 | Listar categorías (`activo`, `search`) |
| GET | `/categorias/{id}` | 200 | Detalle de una categoría |
| PUT | `/categorias/{id}` | 200 | Actualizar una categoría |
| DELETE | `/categorias/{id}` | 204 | Anular una categoría (baja lógica) |
| POST | `/productos` | 201 | Crear un producto |
| GET | `/productos` | 200 | Listar productos (`skip`, `limit`, `activo`, `disponible`, `categoria_id`, `search`) |
| GET | `/productos/{id}` | 200 | Detalle de un producto |
| PUT | `/productos/{id}` | 200 | Actualizar un producto |
| DELETE | `/productos/{id}` | 204 | Anular un producto (baja lógica) |
| POST | `/productos/{id}/categorias` | 201 | Clasificar un producto en una categoría |
| GET | `/productos/{id}/categorias` | 200 | Listar las categorías de un producto |

## Pruebas

La carpeta `tests/` contiene las peticiones para la extensión **REST Client** de VS Code.

1. Levantar el servidor con las tablas `producto`, `categoria` y `productocategoria` vacías.
2. Ejecutar `tests/productos.http` en orden ("Send Request").
3. Ejecutar `tests/relaciones.http` en orden.

Para repetir las pruebas hay que vaciar las tablas antes:

```sql
TRUNCATE productocategoria, producto, categoria RESTART IDENTITY CASCADE;

