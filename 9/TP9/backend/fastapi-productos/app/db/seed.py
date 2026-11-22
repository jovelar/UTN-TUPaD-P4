"""
Script de seed — carga roles y usuarios iniciales para pruebas.
Idempotente: se puede ejecutar múltiples veces sin duplicar datos.

Uso:
    python -m app.db.seed

Requiere PostgreSQL corriendo con las variables de .env configuradas.

Crea:
  - roles: admin, user
  - admin@example.com / Admin1234!  (rol=admin)
  - juan@example.com  / Juan1234!   (rol=user)
"""

from sqlmodel import Session, select
from app.core.database import engine, create_all_tables
from app.core.security import hash_password
from app.modules.usuarios.model import Usuario, Rol, UsuarioRol


ROLES_INICIALES = ["admin", "user"]

USUARIOS_INICIALES = [
    {
        "nombre":   "Administrador",
        "apellido": "del Sistema",
        "email":    "admin@example.com",
        "password": "Admin1234!",
        "rol":      "admin",
    },
    {
        "nombre":   "Juan",
        "apellido": "Pérez",
        "email":    "juan@example.com",
        "password": "Juan1234!",
        "rol":      "user",
    },
]


def run() -> None:
    print("=== Seed — Seguridad JWT (PostgreSQL) ===")
    create_all_tables()

    with Session(engine) as session:
        roles = {}
        for nombre in ROLES_INICIALES:
            rol = session.exec(select(Rol).where(Rol.nombre == nombre)).first()

            if rol:
                print(f"  [=] Ya existe rol: {nombre}")
            else:
                rol = Rol(nombre=nombre)
                session.add(rol)
                session.flush()
                print(f"  [+] Creado rol:    {nombre}")
            roles[nombre] = rol

        for data in USUARIOS_INICIALES:
            existing = session.exec(
                select(Usuario).where(Usuario.email == data["email"])
            ).first()

            if existing:
                print(f"  [=] Ya existe: {data['email']} ({data['rol']})")
            else:
                usuario = Usuario(
                    nombre        = data["nombre"],
                    apellido      = data["apellido"],
                    email         = data["email"],
                    password_hash = hash_password(data["password"]),
                )
                session.add(usuario)
                session.flush()
                session.add(UsuarioRol(usuario_id=usuario.id, rol_id=roles[data["rol"]].id))
                print(f"  [+] Creado:    {data['email']} / {data['password']}  (rol={data['rol']})")

        session.commit()

    print("\nUsuarios disponibles para pruebas:")
    print("  admin@example.com / Admin1234!  → rol=admin  (acceso total)")
    print("  juan@example.com  / Juan1234!   → rol=user   (acceso básico)")
    print()


if __name__ == "__main__":
    run()