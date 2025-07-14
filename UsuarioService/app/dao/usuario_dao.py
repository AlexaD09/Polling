from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from UsuarioService.app.auth.auth_handler import get_password_hash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_usuario_por_correo(db: AsyncSession, correo: str):
    query = text("SELECT * FROM sp_get_usuario_por_correo(:correo)")
    result = await db.execute(query, {"correo": correo})
    row = result.first()
    if row:
        return {
            "id_usuario": row.id_usuario,
            "nombre": row.nombre,
            "correo": row.correo,
            "contraseña": row.contraseña,
            "rol": row.rol
        }
    return None

async def create_usuario(db: AsyncSession, usuario):
    hashed_password = get_password_hash(usuario.contraseña)

    # Validar rol para seguridad, evitar inserción de roles no permitidos
    rol_valido = usuario.rol if usuario.rol in ["cliente", "empleado"] else "cliente"

    query = text(
        "SELECT sp_create_usuario(:nombre, :correo, :contraseña, :rol)"
    )
    await db.execute(query, {
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "contraseña": hashed_password,
        "rol": rol_valido
    })
    await db.commit()
