from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from UsuarioService.app.models import Usuario
from UsuarioService.app.schemas import UsuarioCreate
from UsuarioService.app.auth.auth_handler import get_password_hash

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_usuario_por_correo(db: AsyncSession, correo: str):
    result = await db.execute(select(Usuario).where(Usuario.correo == correo))
    return result.scalars().first()

async def create_usuario(db: AsyncSession, usuario: UsuarioCreate):
    hashed_password = get_password_hash(usuario.contraseña)
    db_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contraseña=hashed_password,
        rol=usuario.rol
    )
    db.add(db_usuario)
    await db.commit()
    await db.refresh(db_usuario)
    return db_usuario