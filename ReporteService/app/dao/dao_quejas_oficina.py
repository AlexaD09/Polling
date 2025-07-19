import httpx
from app.models.dto_quejas_oficina import QuejaOficinaDTO
# Obtiene los datos del mircroservicio de QuejasOficinaService
async def obtener_quejas_oficina() -> list[QuejaOficinaDTO]:
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8002/oficina/quejas-oficina/")  # Cambia URL según tu servicio
        resp.raise_for_status()
        return [QuejaOficinaDTO(**q) for q in resp.json()]
