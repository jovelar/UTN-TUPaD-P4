"""
Repositorio de Usuario.

Acceso a BD: queries sin lógica de negocio.
Hereda de BaseRepository[Usuario] y agrega queries específicas.

Capa: Repository
Conoce a: Model (Usuario), Session
NO conoce a: Service, Router
"""

from datetime import datetime, timezone

from sqlmodel import Session, select, or_

from app.core.base_repository import BaseRepository
from app.modules.usuarios.model import Usuario, Rol, UsuarioRol


class UsuarioRepository(BaseRepository[Usuario]):

    def __init__(self, session: Session):
        super().__init__(Usuario, session)

    def get_by_email(self, email: str) -> Usuario | None:
        return self.session.exec(
            select(Usuario).where(Usuario.email == email)
        ).first()

    def list_all(self) -> list[Usuario]:
        return list(self.session.exec(select(Usuario).order_by(Usuario.id)).all())

    def get_rol_by_nombre(self, nombre: str) -> Rol | None:
        return self.session.exec(
            select(Rol).where(Rol.nombre == nombre)
        ).first()

    def asignar_rol(
        self, usuario_id: int, rol_id: int, asignado_por_id: int | None = None
    ) -> UsuarioRol:
        vinculo = UsuarioRol(
            usuario_id=usuario_id,
            rol_id=rol_id,
            asignado_por_id=asignado_por_id,
        )
        self.session.add(vinculo)
        self.session.flush()
        return vinculo

    # Solo roles sin vencimiento o con expires_at futuro (RN-14)
    def get_roles_vigentes(self, usuario_id: int) -> list[str]:
        ahora = datetime.now(timezone.utc)
        consulta = (
            select(Rol.nombre)
            .join(UsuarioRol, UsuarioRol.rol_id == Rol.id)
            .where(
                UsuarioRol.usuario_id == usuario_id,
                or_(UsuarioRol.expires_at == None, UsuarioRol.expires_at > ahora),  # noqa: E711
            )
            .order_by(Rol.nombre)
        )
        return list(self.session.exec(consulta).all())
    
    
    def list_roles(self) -> list[Rol]:
        return list(self.session.exec(select(Rol).order_by(Rol.id)).all())