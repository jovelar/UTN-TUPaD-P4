# Usuarios en Memoria

API REST con Spring Boot para gestión de usuarios en memoria.

## Tecnologías

- Java 17
- Spring Boot 3.5.6
- Spring Web
- Lombok
- Gradle

## Características

- CRUD completo de usuarios
- Almacenamiento en memoria (sin base de datos)
- API RESTful
- Entidad Usuario con campos: id, nombre, email

## Endpoints

- `GET /api/usuarios` - Listar todos los usuarios
- `GET /api/usuarios/{id}` - Obtener usuario por ID
- `POST /api/usuarios` - Crear nuevo usuario

## Ejecutar el proyecto

```bash
./gradlew bootRun
```

La aplicación se ejecutará en `http://localhost:8080`

## Compilar

```bash
./gradlew build
```
