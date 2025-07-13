from pydantic import BaseModel

class LoginData(BaseModel):
    correo: str
    contraseña: str


class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    rol: str = "cliente"

class UsuarioCreate(UsuarioBase):
    contraseña: str

class Usuario(UsuarioBase):
    id_usuario: int

    class Config:
        orm_mode = True