from pydantic import BaseModel

class QuejaCombinadaDTO(BaseModel):
    origen: str
    nombre: str
    correo: str
    titulo: str
    descripcion: str
    estado: str
    
class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    rol: str = "empleado"

class UsuarioDTO(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    rol: str
