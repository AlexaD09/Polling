from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dto_queja_oficina import Queja, QuejaCreate
from app.dao.queja_dao_pg import crear_queja, obtener_quejas, obtener_queja_por_id, actualizar_estado_queja
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Ruta para agregar o crear la queja
@router.post("/quejas-oficina/", response_model=Queja)
def registrar_queja(queja: QuejaCreate, db: Session = Depends(get_db)):
    return crear_queja(db=db, queja=queja)

#esta ruta es para obtener las quejas oficina
@router.get("/quejas-oficina/", response_model=list[Queja])
def listar_quejas(db: Session = Depends(get_db)):
    return obtener_quejas(db=db)
#Obtener quejas de oficina mediante el id
@router.get("/quejas-oficina/{id_queja}", response_model=Queja)
def ver_queja(id_queja: int, db: Session = Depends(get_db)):
    db_queja = obtener_queja_por_id(db, id_queja=id_queja)
    if not db_queja:
        raise HTTPException(status_code=404, detail="Queja no encontrada")
    return db_queja

#Ruta para actualizar el estado de las quejas.
@router.put("/quejas-oficina/{id_queja}/estado", response_model=Queja)
def cambiar_estado(id_queja: int, nuevo_estado: str, db: Session = Depends(get_db)):
    return actualizar_estado_queja(db=db, id_queja=id_queja, nuevo_estado=nuevo_estado)