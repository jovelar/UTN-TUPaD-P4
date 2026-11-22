"""
Service de Usuario — lógica de negocio.

Stateless, orquesta operaciones sobre los repositorios a través del UoW.
Lanza HTTPException. No hace commit/rollback directamente.

Capa: Service
Conoce a: UoW, Repository (indirectamente vía UoW)
NO conoce a: Router

Regla de imports:
    Router → Service → UoW → Repository → Model
"""

from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token
from app.core.uow import UnitOfWork
from app.modules.usuarios.model import Usuario, Rol, UserCreate, Token, UserPublic


class UsuarioService:
    """Lógica de negocio para autenticación y gestión de usuarios."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def _to_public(self, user: Usuario) -> UserPublic:
        return UserPublic.model_validate(
            user,
            update={
                "roles": self.uow.usuarios.get_roles_vigentes(user.id),
                "activo": user.deleted_at is None,
            },
        )

    def register(self, user_in: UserCreate):
        """Registra un nuevo usuario. El rol siempre es 'user'."""
        if self.uow.usuarios.get_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado",
            )

        rol_user = self.uow.usuarios.get_rol_by_nombre("user")
        if rol_user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Rol 'user' no cargado: ejecutar seed.py",
            )

        usuario = Usuario(
            nombre=user_in.nombre,
            apellido=user_in.apellido,
            email=user_in.email,
            celular=user_in.celular,
            password_hash=hash_password(user_in.password),
        )

        usuario = self.uow.usuarios.add(usuario)
        self.uow.usuarios.asignar_rol(usuario.id, rol_user.id)

        rta = self._to_public(usuario)
        return rta

    def authenticate(self, email: str, password: str) -> Token:
        """Autentica con email + password y retorna un Token con JWT."""
        user = self.uow.usuarios.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cuenta de usuario desactivada",
            )

        access_token = create_access_token(
            data={"sub": user.email}
        )
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def list_all(self) -> list[UserPublic]:
        """Lista todos los usuarios."""
        return [self._to_public(u) for u in self.uow.usuarios.list_all()]

    def set_disabled(self, user_id: int, disabled: bool) -> UserPublic:
        """Activa o desactiva la cuenta de un usuario."""
        user = self.uow.usuarios.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        user.deleted_at = datetime.now(timezone.utc) if disabled else None
        return self._to_public(self.uow.usuarios.update(user))
    
    def list_roles(self) -> list[Rol]:
        """Lista el catálogo de roles."""
        return self.uow.usuarios.list_roles()