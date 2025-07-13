from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from UsuarioService.app.dao import usuario_dao
from UsuarioService.app.schemas import UsuarioCreate, Usuario, LoginData
from UsuarioService.app.database import get_db
from UsuarioService.app.auth.auth_bearer import JWTBearer
from UsuarioService.app.auth.auth_handler import create_access_token


router = APIRouter()

@router.post("/registro", response_model=Usuario)
async def registrar_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    db_usuario = await usuario_dao.get_usuario_por_correo(db, correo=usuario.correo)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    return await usuario_dao.create_usuario(db, usuario)

@router.post("/login")
async def login(data: LoginData, db: AsyncSession = Depends(get_db)):
    db_usuario = await usuario_dao.get_usuario_por_correo(db, correo=data.correo)
    if not db_usuario or not usuario_dao.verify_password(data.contraseña, db_usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_access_token(subject=db_usuario.correo)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/protegida", dependencies=[Depends(JWTBearer())])
async def ruta_protegida():
    return {"mensaje": "Acceso permitido"}