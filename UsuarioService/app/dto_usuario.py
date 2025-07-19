from pydantic import BaseModel

class LoginData(BaseModel):
    correo: str
    contraseña: str

# DTO de entrada para registro
class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    rol: str = "cliente"

# DTO solo para uso interno (validación en backend, incluye contraseña hasheada)
class UsuarioCreate(UsuarioBase):
    contraseña: str

class Usuario(UsuarioBase):
    id_usuario: int

    class Config:
        orm_mode = True


# DTO de salida (para el frontend, sin contraseña)
class UsuarioDTO(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    rol: str

    class Config:
        orm_mode = True        