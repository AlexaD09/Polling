from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
#DTO para crear la queja con todos los campos necesarios
class QuejaCreate(BaseModel):
    id_usuario: str
    nombre: str
    email: str
    titulo: str
    descripcion: str
    estado: Optional[str] = "Pendiente"


class Queja(QuejaCreate):
    id: Optional[str] = Field(alias="_id")
    fecha_creacion: Optional[datetime]
