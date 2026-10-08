# API Integradora - Unidad 1 (Trabajo Práctico 4)

API REST de gestión de catálogo desarrollada con **FastAPI** y **Pydantic**.
Administra **Categorías**, **Productos** y **Proveedores**. El módulo Proveedores es el que agrega este TP.
Los datos se guardan en memoria (listas) mientras corre el servidor y no se persisten.

## Estructura del proyecto

```
u1_ej_8_integrador/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── modules/
│       ├── __init__.py
│       ├── categoria/
│       │   ├── __init__.py
│       │   ├── routers.py
│       │   ├── schemas.py
│       │   └── services.py
│       ├── producto/
│       │   ├── __init__.py
│       │   ├── routers.py
│       │   ├── schemas.py
│       │   └── services.py
│       └── proveedor/
│           ├── __init__.py
│           ├── routers.py
│           ├── schemas.py
│           └── services.py
├── tests/
│   └── test_api.http
├── requirements.txt
└── README.md
```

Flujo: `main` → `routers` (endpoints) → `ser`schemas` (validación).

## Instalación y ejecución

```bash
# 1. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el servidor
fastapi dev app/main.py
```

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Módulo Proveedores

### Schemas

| Campo        | Tipo | Requerido | Default | Validación                    |
|--------------|------|-----------|------------|
| codigo       | str  | Sí        | —       | min_length=1                  |
| razon_social | str  | Sí        | —       | min_length=3                  |
| cuit         | str  | Sí        | —       | min_length=11, max_length=15  |
| email        | str  | No        | `""`    | —                             |
| telefono     | str  | No        | `""`       |
| activo       | bool | No        | `True`  | —                             |

- `ProveedorBase`: todos los campos anterior
| activo       | bool | No        | `True`  | —                             |

- `ProveedorBase`: todos los campos anterior
- `ProveedorCreate`: hereda de `ProveedorBase`.
- `ProveedorRead`: agrega `id` (lo genera el backend).
- `ProveedorUpdate`: todos los campos son op

### Endpoints

| Método | Endpoint                       |                           |
|--------|--------------------------------|--------|-----------------------------------------------|
| POST   | `/proveedores/`                | 201    | Crear un proveedor                            |
| GET    | `/proveedores/`                | con paginación y filtro)  |
| GET    | `/proveedores/{id}`            | 200    | Obtener un proveedor por ID                   |
| PUT    | `/proveedores/{id}`            | 200    | Reemplazo total de un proveedor               |
| PUT    | `/proveedores/{id}/desactivar` | dor (borrado lógico)      |

Query params de `GET /proveedores/`:

| Parámetro | Tipo           | Default | Validación / Descripción                         |
|-----------|----------------|---------|--------------------------------------------------|
| skip      | int            | 0       | ge=                 |
| limit     | int            | 10      | ge=1, le=50                                      |
| activo    | Optional[bool] | None    | true = activos, false = inactivos, omitido = todos |

### Reglas de negocio

| ID    | Regla                                                         | Respuesta |
|-------|---------------------------------------------------------------|-----------|
| RN-01 | El código es obligatorio (min_length=1)                       | 422       |
| RN-02 | El código es único                                            | 409       |
| RN-03 | La razón social es obligatoria (mi 422       |
| RN-04 | No se puede consultar/actualizar/desactivar un id inexistente | 404       |
| RN-05 | No se puede desactivar un proveedor ya desactivado            | 409       |

Los errores se devuelven con `HTTPException` en formato `{"detail": "..."}`.

## Pruebas

El archivo `tests/test_api.http` contiene la*REST Client** de VS Code.
Cubre todos los endpoints y escenarios de error: 200, 201, 404, 409 y 422.

1. Levantar el servidor con `fastapi dev app
2. Abrir `tests/test_api.http` y ejecutar las peticiones en orden ("Send Request").
