from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao import usuario_dao
from app.dto_usuario import UsuarioCreate, Usuario, LoginData, UsuarioDTO
from app.database import get_db
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import create_access_token


router = APIRouter()

@router.post("/registro", response_model=Usuario)
async def registrar_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    print("Datos recibidos:", usuario)  # <--- para ver qué llega
    db_usuario = await usuario_dao.get_usuario_por_correo(db, correo=usuario.correo)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    nuevo_usuario = await usuario_dao.create_usuario(db, usuario)
    return nuevo_usuario


@router.post("/login")
async def login(data: LoginData, db: AsyncSession = Depends(get_db)):
    usuario = await usuario_dao.get_usuario_por_correo(db, data.correo)
    if not usuario:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    if not usuario_dao.verify_password(data.pssw, usuario["pssw"]):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    
    token = create_access_token(
        id_usuario=usuario["id_usuario"],
        nombre=usuario["nombre"],
        email=usuario["correo"],
        role=usuario["rol"]
    )
    return {"access_token": token, "token_type": "bearer"}



@router.get("/protegida", dependencies=[Depends(JWTBearer())])
async def ruta_protegida():
    return {"mensaje": "Acceso permitido"}

@router.get("/usuarios", response_model=List[UsuarioDTO])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    return await usuario_dao.get_todos_los_usuarios(db)