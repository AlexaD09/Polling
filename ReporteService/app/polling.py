# ReporteService/app/polling.py

import asyncio
import traceback
from typing import List

from ReporteService.app.dao.dao_reporte import obtener_quejas_combinadas, obtener_usuarios
from ReporteService.app.dao.dao_quejas_web import obtener_quejas_web
from ReporteService.app.dao.dao_quejas_oficina import obtener_quejas_oficina

from ReporteService.app.models.dto_reporte import QuejaCombinadaDTO, UsuarioDTO
from ReporteService.app.models.dto_quejas_web import QuejaWebDTO
from ReporteService.app.models.dto_quejas_oficina import QuejaOficinaDTO

# ===================
# Cachés y Locks
# ===================

cache_combinadas: List[QuejaCombinadaDTO] = []
cache_web: List[QuejaWebDTO] = []
cache_oficina: List[QuejaOficinaDTO] = []
cache_usuarios: List[UsuarioDTO] = []

_lock_combinadas = asyncio.Lock()
_lock_web = asyncio.Lock()
_lock_oficina = asyncio.Lock()
_lock_usuarios = asyncio.Lock()

# ===================
# Actualizar cachés
# ===================

async def actualizar_cache_combinadas():
    global cache_combinadas
    try:
        #print("[Polling] Obteniendo quejas combinadas")
        quejas = await obtener_quejas_combinadas()
        async with _lock_combinadas:
            cache_combinadas = quejas
        print(f"[Polling] Cache Combinadas actualizada con {len(quejas)} quejas")
    except Exception as e:
        print(f"[Polling] Error al actualizar cache Combinadas: {e}")
        traceback.print_exc()

async def actualizar_cache_web():
    global cache_web
    try:
        #print("[Polling] Obteniendo quejas Web")
        quejas = await obtener_quejas_web()
        async with _lock_web:
            cache_web = quejas
        print(f"[Polling] Cache Web actualizada con {len(quejas)} quejas")
    except Exception as e:
        print(f"[Polling] Error al actualizar cache Web: {e}")
        traceback.print_exc()

async def actualizar_cache_oficina():
    global cache_oficina
    try:
        #print("[Polling] Obteniendo quejas Oficina")
        quejas = await obtener_quejas_oficina()
        async with _lock_oficina:
            cache_oficina = quejas
        print(f"[Polling] Cache Oficina actualizada con {len(quejas)} quejas")
    except Exception as e:
        print(f"[Polling] Error al actualizar cache Oficina: {e}")
        traceback.print_exc()

async def obtener_cache_web_por_usuario(id_usuario: str) -> list[QuejaWebDTO]:
    async with _lock_web:
        quejas_usuario = [q for q in cache_web if q.id_usuario == id_usuario]
    print(f"[Polling] Quejas encontradas para usuario {id_usuario}: {len(quejas_usuario)}")
    return quejas_usuario

async def actualizar_cache_usuarios():
    global cache_usuarios
    try:
        usuarios = await obtener_usuarios()
        async with _lock_usuarios:
            cache_usuarios = usuarios
        print(f"[Polling] Cache Usuarios actualizada con {len(usuarios)} usuarios")
    except Exception as e:
        print(f"[Polling] Error al actualizar cache Usuarios: {e}")
        traceback.print_exc()

async def obtener_cache_usuarios() -> List[UsuarioDTO]:
    async with _lock_usuarios:
        return cache_usuarios.copy()


# ===================
# Obtener desde cachés
# ===================

async def obtener_cache_combinadas() -> List[QuejaCombinadaDTO]:
    async with _lock_combinadas:
        return cache_combinadas.copy()

async def obtener_cache_web() -> List[QuejaWebDTO]:
    async with _lock_web:
        return cache_web.copy()

async def obtener_cache_oficina() -> List[QuejaOficinaDTO]:
    async with _lock_oficina:
        return cache_oficina.copy()

# ===================
# Polling general
# ===================

async def polling_periodico(intervalo_segundos: int = 30):
    while True:
        print("[Polling] Ejecutando ciclo de actualización de caches...")
        await actualizar_cache_combinadas()
        await actualizar_cache_web()
        await actualizar_cache_oficina()
        await actualizar_cache_usuarios()
        await asyncio.sleep(intervalo_segundos)
