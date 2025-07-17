from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class QuejaCreate(BaseModel):
    id_usuario: int
    nombre_cliente: str
    correo_cliente: Optional[str] = None
    titulo: str
    descripcion: str
    estado: Optional[str] = "Pendiente"

class Queja(QuejaCreate):
    id_queja: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True