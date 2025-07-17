from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from QuejasOficinaService.app.database import Base

class QuejaOficina(Base):
    __tablename__ = 'quejas_oficina'

    id_queja = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, nullable=False)
    nombre_cliente = Column(String(100), nullable=False)
    correo_cliente = Column(String(100))
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=False)
    estado = Column(String(20), default='Pendiente')
    fecha_creacion = Column(TIMESTAMP, default="now()")