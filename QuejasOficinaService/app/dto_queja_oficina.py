from datetime import datetime
from pydantic import BaseModel
from typing import Optional

#DTO para crear una queja y tambien valida datos
class QuejaCreate(BaseModel):
    id_usuario: int
    nombre_cliente: str
    correo_cliente: Optional[str] = None
    titulo: str
    descripcion: str
    estado: Optional[str] = "Pendiente" 
#DTO que hereda los campos de queja create
class Queja(QuejaCreate):
    id_queja: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True