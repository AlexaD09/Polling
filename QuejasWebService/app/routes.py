from typing import List
from fastapi import APIRouter, Body, Depends, Path, Query
from app.dao.queja_dao_mongo import QuejaDAO
from app.dto_queja_web import  QuejaCreate
from app.database import db
from fastapi import HTTPException


router = APIRouter()

def get_queja_dao() -> QuejaDAO:
    return QuejaDAO(db)
#Ruta para insertar quejas en mongodb
@router.post("/quejas/")
async def crear_queja(queja: QuejaCreate = Body(...), dao: QuejaDAO = Depends(get_queja_dao)):
    inserted_id = await dao.crear_queja(queja.dict())
    return {"mensaje": "Queja creada", "id": str(inserted_id)}
#Obtener usuarios por id
@router.get("/quejas/usuario/{usuario_id}")
async def obtener_quejas_usuario(usuario_id: str, dao: QuejaDAO = Depends(get_queja_dao)):
    quejas = await dao.obtener_quejas_por_usuario(usuario_id)
    if not quejas:
        raise HTTPException(status_code=404, detail="No se encontraron quejas para este usuario")
    return quejas
#Obtener todas las quejas de mongo
@router.get("/quejas-web/")
async def obtener_todas_quejas(dao: QuejaDAO = Depends(get_queja_dao)):
    return await dao.listar_todas() 
#Ruta para actualizar el estado de las quejas
@router.put("/quejas-web/{id_queja}/estado")
async def actualizar_estado_queja_web(
    id_queja: str = Path(...),
    nuevo_estado: str = Query(...),
    dao: QuejaDAO = Depends(get_queja_dao)
):
    actualizado = await dao.actualizar_estado(id_queja, nuevo_estado)
    if actualizado == 0:
        raise HTTPException(status_code=404, detail="Queja no encontrada o no actualizada")
    return {"mensaje": "Estado actualizado correctamente"}