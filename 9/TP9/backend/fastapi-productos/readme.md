# API Food Store - Trabajo Práctico Unidad 9

API REST con **FastAPI**, **SQLModel** y **PostgreSQL**. Extiende el CRUD de **Categorías** y **Productos**
de la Unidad 8 con autenticación JWT en cookie HttpOnly, gestión de usuarios y autorización por roles
(`Usuario`, `Rol` y `UsuarioRol`), según el diagrama `UML_FOOD_STORE`. Se basa en el proyecto de
referencia `seguridad_jwt_pg` de la cátedra.

El frontend (React + TypeScript) está en `frontend/tp-categorias`.

**Fuera del alcance de este TP:** Pedidos e Ingredientes, que formaban parte del TP de la Unidad 8,
no se incluyen.

## Requisitos

- Python 3.11, 3.12 o 3.13 (`sqlmodel` 0.0.22 no es compatible con Python 3.14)
- PostgreSQL
- pip

## Instalación

Desde la carpeta `fastapi-productos/`:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno

1. Crear la base de datos `TP-9` en PostgreSQL.
2. Copiar `.env.example` como `.env` y completar `POSTGRES_PASSWORD` y `SECRET_KEY`.

`SECRET_KEY` es obligatoria (al menos 32 caracteres): sin ella la aplicación no arranca. Para generarla:

```
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

El archivo `.env` contiene secretos: no se entrega ni se sube al repositorio.

## Carga inicial de datos (seed)

El script `app/db/seed.py` crea las tablas si no existen y carga los roles `admin` y `user` y dos
usuarios de prueba. Puede ejecutarse varias veces sin duplicar registros.

```
python -m app.db.seed
```

| Email | Contraseña | Rol |
|---|---|---|
| admin@example.com | Admin1234! | admin |
| juan@example.com | Juan1234! | user |

## Ejecución

```
uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

CORS acepta `http://localhost:5173` con credenciales (`allow_credentials=True`), para que el navegador
envíe la cookie desde el frontend.

## Cómo viaja el token

El login (`POST /api/v1/auth/token`) recibe un formulario OAuth2 cuyo campo `username` lleva el email.
No devuelve el token en el cuerpo: lo guarda en la cookie HttpOnly `access_token`. Las rutas protegidas
leen el token solo de esa cookie.

## Endpoints

### Autenticación y usuarios (`/api/v1/auth`)

| Método | Ruta | Acceso |
|---|---|---|
| POST | `/register` | Público. Asigna el rol `user` |
| POST | `/token` | Público (formulario OAuth2) |
| POST | `/logout` | Público. Borra la cookie |
| GET | `/me` | Usuario autenticado |
| GET | `/privado` | Usuario autenticado |
| GET | `/admin/usuarios` | Rol `admin`. Incluye a los desactivados e indica su estado |
| POST | `/admin/usuarios/{id}/desactivar` | Rol `admin`. Completa `deleted_at` |
| POST | `/admin/usuarios/{id}/activar` | Rol `admin`. Vuelve `deleted_at` a nulo |

### Categorías (`/api/v1/categorias`)

| Método | Ruta | Acceso |
|---|---|---|
| GET | `/`, `/{id}` | Usuario autenticado |
| POST | `/` | Rol `admin` |
| PATCH | `/{id}` | Rol `admin` |
| DELETE | `/{id}` | Rol `admin`. Borrado lógico |

### Productos (`/api/v1/productos`)

| Método | Ruta | Acceso |
|---|---|---|
| GET | `/`, `/{id}` | Usuario autenticado. Cada producto incluye sus categorías |
| POST | `/` | Rol `admin` |
| PATCH | `/{id}` | Rol `admin` |
| DELETE | `/{id}` | Rol `admin`. Borrado lógico |
| POST | `/{id}/categorias` | Rol `admin`. Cuerpo: `categoria_id` y `es_principal` |
| DELETE | `/{id}/categorias/{categoria_id}` | Rol `admin`. Borra la fila de `ProductoCategoria` |
### Roles (`/api/v1/roles`)

| Método | Ruta | Acceso |
|---|---|---|
| GET | `/` | Usuario autenticado. Catálogo cargado con `seed.py`; las escrituras responden 405 |

## Reglas implementadas

| Regla | Respuesta |
|---|---|
| Sin sesión o token inválido | 401 |
| Usuario sin el rol requerido (roles vigentes en `UsuarioRol`) | 403 |
| Cuenta desactivada (login y rutas protegidas) | 400 «Cuenta de usuario desactivada» |
| Email de usuario o nombre de categoría repetido | 409 |
| Email inválido, contraseña de menos de 8 caracteres, precio negativo | 422 |
| Recurso inexistente o eliminado | 404 |
| DELETE de categoría o producto | Completa `deleted_at`; los listados lo excluyen |

`require_role` solo considera los roles vigentes: las filas de `UsuarioRol` sin `expires_at` o con
`expires_at` posterior a la fecha actual.

## Pruebas con REST Client

Con la extensión **REST Client** de VS Code y el servidor corriendo:

| Archivo | Cubre |
|---|---|
| `seguridad_jwt.http` | Registro, login, `/me`, roles, activar/desactivar y logout |
| `productos.http` | Categorías, productos y `ProductoCategoria`, con los casos 401, 403, 404, 409 y 422 y el borrado lógico |

## Estructura del proyecto

```
fastapi-productos/
├── app/
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── core/
│   │   ├── config.py        # Configuración (pydantic-settings)
│   │   ├── database.py      # Engine de PostgreSQL
│   │   ├── security.py      # JWT y bcrypt
│   │   ├── deps.py          # get_current_user, get_current_active_user y require_role
│   │   ├── uow.py           # Unit of Work
│   │   └── base_repository.py
│   ├── modules/
│   │   ├── usuarios/        # Usuario, Rol, UsuarioRol: registro, login y administración
│   │   ├── categorias/      # CRUD de categorías
│   │   └── productos/       # CRUD de productos y ProductoCategoria
│   └── db/
│       └── seed.py          # Roles y usuarios iniciales
├── seguridad_jwt.http       # REST Client (VS Code)
├── productos.http           # REST Client (VS Code)
├── requirements.txt
└── .env.example             # Plantilla de variables de entorno
```