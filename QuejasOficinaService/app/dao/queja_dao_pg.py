from sqlalchemy.orm import Session
from ..models import QuejaOficina
from ..schemas import Queja, QuejaCreate

def crear_queja(db: Session, queja: QuejaCreate):
    db_queja = QuejaOficina(**queja.dict())
    db.add(db_queja)
    db.commit()
    db.refresh(db_queja)
    return db_queja

def obtener_quejas(db: Session):
    return db.query(QuejaOficina).all()

def obtener_queja_por_id(db: Session, id_queja: int):
    return db.query(QuejaOficina).filter(QuejaOficina.id_queja == id_queja).first()

def actualizar_estado_queja(db: Session, id_queja: int, nuevo_estado: str):
    db_queja = db.query(QuejaOficina).filter(QuejaOficina.id_queja == id_queja).first()
    if db_queja:
        db_queja.estado = nuevo_estado
        db.commit()
        db.refresh(db_queja)
    return db_queja