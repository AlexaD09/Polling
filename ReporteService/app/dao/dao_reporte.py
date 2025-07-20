import httpx
from app.models.dto_reporte import QuejaCombinadaDTO, UsuarioDTO
from app.dao.dao_quejas_web import obtener_quejas_web
from app.dao.dao_quejas_oficina import obtener_quejas_oficina

#Realiza el dao acceso combinado a los mos microservicios QuejasOficinaService y QuejasWebService

async def obtener_quejas_combinadas() -> list[QuejaCombinadaDTO]:
    quejas_web = await obtener_quejas_web()
    quejas_oficina = await obtener_quejas_oficina()

    combinadas = []

    for q in quejas_web:
        combinadas.append(QuejaCombinadaDTO(
            origen="Web",
            nombre=q.nombre,
            correo=q.email,
            titulo=q.titulo,
            descripcion=q.descripcion,
            estado=q.estado,
            
        ))

    for q in quejas_oficina:
        combinadas.append(QuejaCombinadaDTO(
            origen="Oficina",
            nombre=q.nombre_cliente,
            correo=q.correo_cliente,
            titulo=q.titulo,
            descripcion=q.descripcion,
            estado=q.estado,
           
        ))

    return combinadas


#DAO obtener usuariosasync def obtener_usuarios() desde el microservicio UsuarioService:
async def obtener_usuarios() -> list[UsuarioDTO]:
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://usuarioservice:8000/usuarios/usuarios")  # URL local directa
        resp.raise_for_status()
        return [UsuarioDTO(**u) for u in resp.json()]
