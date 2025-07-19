from pydantic import BaseModel

class QuejaOficinaDTO(BaseModel):
    id_queja: int
    id_usuario: int
    nombre_cliente: str
    correo_cliente: str
    titulo: str
    descripcion: str
    estado: str
    fecha_creacion: str  # Aquí está la fecha y deberías usarla si quieres mostrarla
