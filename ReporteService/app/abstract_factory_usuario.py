
from abc import ABC, abstractmethod
from typing import List
from ReporteService.app.dao.dao_reporte import obtener_usuarios
from ReporteService.app.models.dto_reporte import UsuarioDTO

class UsuarioFactoryBase(ABC):
    @abstractmethod
    async def obtener_usuarios(self) -> List[UsuarioDTO]:
        pass


class UsuarioFactory(UsuarioFactoryBase):
    async def obtener_usuarios(self) -> List[UsuarioDTO]:
        return await obtener_usuarios()
