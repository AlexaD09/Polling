# ReporteService/app/factory/abstract_factory.py

from abc import ABC, abstractmethod
from typing import List
from ReporteService.app.models.dto_reporte import QuejaCombinadaDTO
from ReporteService.app.models.dto_quejas_web import QuejaWebDTO
from ReporteService.app.models.dto_quejas_oficina import QuejaOficinaDTO

class QuejaFactory(ABC):
    @abstractmethod
    async def obtener_quejas(self) -> list:
        pass

# =============================
# Fábrica de quejas combinadas
# =============================
class QuejaFactoryCombinada(QuejaFactory):
    async def obtener_quejas(self) -> List[QuejaCombinadaDTO]:
        from ReporteService.app.polling import obtener_cache_combinadas
        cache = await obtener_cache_combinadas()
        if cache:
            return cache
        from ReporteService.app.dao.dao_reporte import obtener_quejas_combinadas
        return await obtener_quejas_combinadas()

# =============================
# Fábrica de quejas Web (Mongo)
# =============================
class QuejaFactoryMongo(QuejaFactory):
    async def obtener_quejas(self) -> List[QuejaWebDTO]:
        from ReporteService.app.polling import obtener_cache_web
        cache = await obtener_cache_web()
        if cache:
            return cache
        from ReporteService.app.dao.dao_quejas_web import obtener_quejas_web
        return await obtener_quejas_web()

# =============================
# Fábrica de quejas Oficina (Postgre)
# =============================
class QuejaFactoryPostgre(QuejaFactory):
    async def obtener_quejas(self) -> List[QuejaOficinaDTO]:
        from ReporteService.app.polling import obtener_cache_oficina
        cache = await obtener_cache_oficina()
        if cache:
            return cache
        from ReporteService.app.dao.dao_quejas_oficina import obtener_quejas_oficina
        return await obtener_quejas_oficina()




class QuejaCombinadaDTO(QuejaCombinadaDTO):
 @staticmethod
 async def obtener_quejas() -> List[QuejaCombinadaDTO]:
        from ReporteService.app.polling import obtener_cache_combinadas
        cache = await obtener_cache_combinadas()
        if cache:
            return cache
        from ReporteService.app.dao.dao_reporte import obtener_quejas_combinadas
        return await obtener_quejas_combinadas()