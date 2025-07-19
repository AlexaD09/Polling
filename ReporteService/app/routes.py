from fastapi import APIRouter, HTTPException, Header
from app.abstract_factory_quejas import QuejaFactoryCombinada
from app.abstract_factory_usuario import UsuarioFactory
from app.ia.recomendaciones import generar_recomendaciones
from app.polling import obtener_cache_web_por_usuario

router = APIRouter()

# ReporteService/app/routes/routes.py

from fastapi import APIRouter
from app.abstract_factory_quejas import (
    QuejaFactoryCombinada, QuejaFactoryMongo, QuejaFactoryPostgre
)

router = APIRouter()
#Ruta para obtener los datos de ambas bd de datos
@router.get("/api/reporte/combinado")
async def obtener_reporte_combinado():
    factory = QuejaFactoryCombinada()
    return await factory.obtener_quejas()
#Ruta para obtener las quejas web
@router.get("/api/reporte/web")
async def obtener_reporte_mongo():
    factory = QuejaFactoryMongo()
    return await factory.obtener_quejas()
#Ruta para obtener las quejas oficina
@router.get("/api/reporte/oficina")
async def obtener_reporte_postgre():
    factory = QuejaFactoryPostgre()
    return await factory.obtener_quejas()

#Ruta para obtener la generacion de la recomendacion por la ia
@router.get("/api/recomendaciones")
async def get_recomendaciones():
    factory = QuejaFactoryCombinada()
    quejas = await factory.obtener_quejas()  # Esto devuelve list[QuejaCombinadaDTO]
    recomendacion = await generar_recomendaciones(quejas)
    return {"recomendacion": recomendacion}
#Ruta para obtener las quejas por id de usuario
@router.get("/api/reporte/web/usuario/{id_usuario}")
async def obtener_quejas_usuario(id_usuario: str, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de autorización no proporcionado")
    token = authorization.split(" ")[1]  # 'Bearer <token>'

    # Llamamos a la función del polling para obtener cache filtrado
    quejas = await obtener_cache_web_por_usuario(id_usuario)
    return {"quejas": quejas}
#Ruta que obtiene los usuarios
@router.get("/api/reporte/usuarios")
async def obtener_usuarios_para_admin():
    factory = UsuarioFactory()
    return await factory.obtener_usuarios()