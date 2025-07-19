import httpx
from ReporteService.app.models.dto_quejas_oficina import QuejaOficinaDTO

async def obtener_quejas_oficina() -> list[QuejaOficinaDTO]:
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8002/oficina/quejas-oficina/")  # Cambia URL según tu servicio
        resp.raise_for_status()
        return [QuejaOficinaDTO(**q) for q in resp.json()]
