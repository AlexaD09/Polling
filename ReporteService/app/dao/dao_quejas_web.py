import httpx
from app.models.dto_quejas_web import QuejaWebDTO

#Obtiene las quejas desde el microservicio QuejasWebService
async def obtener_quejas_web() -> list[QuejaWebDTO]:
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8001/quejas-web/")
        resp.raise_for_status()
        quejas_raw = resp.json()
        quejas = []
        for q in quejas_raw:
            queja_dict = {
                "id": str(q.get("_id", "")),  # porque ya es string directo
                "id_usuario": q.get("id_usuario",""),
                "nombre": q.get("nombre", ""),               # nombre del usuario en Mongo
                "email": q.get("email", ""),                  # email en Mongo (añadido si quieres)
                "titulo": q.get("titulo", ""),
                "descripcion": q.get("descripcion", ""),
                "estado": q.get("estado", "")
                                 # si no tienes fecha, deja vacío
            }
            quejas.append(QuejaWebDTO(**queja_dict))
        return quejas

#Obtiene las quejas por id desde el microservisio de QuejasWebService
async def obtener_quejas_por_usuario(id_usuario: str, token: str) -> list[QuejaWebDTO]:
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://localhost:8001/quejas/usuario/{id_usuario}"
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        quejas_raw = resp.json()
        quejas = []
        for q in quejas_raw:
            queja_dict = {
                "titulo": q.get("titulo", ""),
                "descripcion": q.get("descripcion", ""),
                "estado": q.get("estado", "")
            }
            quejas.append(QuejaWebDTO(**queja_dict))
        return quejas