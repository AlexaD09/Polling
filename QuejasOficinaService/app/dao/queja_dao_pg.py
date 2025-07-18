from sqlalchemy import text
from sqlalchemy.orm import Session
from ..dto_queja_oficina import QuejaCreate

def crear_queja(db: Session, queja: QuejaCreate):
    query = text("""
        SELECT * FROM sp_crear_queja(
            :id_usuario, :nombre_cliente, :correo_cliente, :titulo, :descripcion, :estado
        )
    """)
    result = db.execute(query, {
        "id_usuario": queja.id_usuario,
        "nombre_cliente": queja.nombre_cliente,
        "correo_cliente": queja.correo_cliente,
        "titulo": queja.titulo,
        "descripcion": queja.descripcion,
        "estado": queja.estado
    })
    row = result.first()
    db.commit()
    return row

def obtener_quejas(db: Session):
    query = text("SELECT * FROM sp_obtener_quejas()")
    result = db.execute(query)
    return result.fetchall()

def obtener_queja_por_id(db: Session, id_queja: int):
    query = text("SELECT * FROM sp_obtener_queja_por_id(:id_queja)")
    result = db.execute(query, {"id_queja": id_queja})
    return result.first()

def actualizar_estado_queja(db: Session, id_queja: int, nuevo_estado: str):
    query = text("SELECT * FROM sp_actualizar_estado_queja(:id_queja, :nuevo_estado)")
    result = db.execute(query, {
        "id_queja": id_queja,
        "nuevo_estado": nuevo_estado
    })
    db.commit()
    return result.first()
