
from abc import ABC, abstractmethod
from typing import List
from app.dao.dao_reporte import obtener_usuarios
from app.models.dto_reporte import UsuarioDTO

#Clase abstracta para obtener usuarios

class UsuarioFactoryBase(ABC):
    @abstractmethod
    async def obtener_usuarios(self) -> List[UsuarioDTO]:
        pass

#Clase concreta para obtener usuarios
class UsuarioFactory(UsuarioFactoryBase):
    async def obtener_usuarios(self) -> List[UsuarioDTO]:
        return await obtener_usuarios()
