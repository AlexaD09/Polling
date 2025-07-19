from pydantic import BaseModel, Field

class QuejaWebDTO(BaseModel):
    id: str   # Alias para mapear _id a id, pero ojo que _id es dict
    id_usuario: str
    nombre: str
    email: str
    titulo: str
    descripcion: str
    estado: str
    
