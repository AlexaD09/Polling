from sqlalchemy import text
from sqlalchemy.orm import Session
from ..dto_queja_oficina import QuejaCreate

#Funcion para crear la queja oficina
def crear_queja(db: Session, queja: QuejaCreate):
    # Llamamos al procedimiento almacenado `sp_crear_queja` usando SQL en bruto
    query = text("""
        SELECT * FROM sp_crear_queja(
            :id_usuario, :nombre_cliente, :correo_cliente, :titulo, :descripcion, :estado
        )
    """)

    # Ejecutamos la consulta con los parámetros del DTO `QuejaCreate`
    result = db.execute(query, {
        "id_usuario": queja.id_usuario,
        "nombre_cliente": queja.nombre_cliente,
        "correo_cliente": queja.correo_cliente,
        "titulo": queja.titulo,
        "descripcion": queja.descripcion,
        "estado": queja.estado
    })
    row = result.first()# Obtenemos el primer resultado (si lo hay)
    db.commit() # Confirmamos los cambios en la base de datos
    return row  # Confirmamos los cambios en la base de datos

#Obtener quejas de oficina
def obtener_quejas(db: Session):
    # Llamamos al procedimiento almacenado `sp_obtener_quejas`
    query = text("SELECT * FROM sp_obtener_quejas()")
    # Ejecutamos la consulta
    result = db.execute(query)
     # Devolvemos todas las filas obtenidas
    return result.fetchall()

#Obtener la queja por el id del usuario
def obtener_queja_por_id(db: Session, id_queja: int):
    # Llamamos al procedimiento almacenado `sp_obtener_queja_por_id` con el ID de la queja
    query = text("SELECT * FROM sp_obtener_queja_por_id(:id_queja)")
     # Ejecutamos la consulta pasando el parámetro `id_queja`
    result = db.execute(query, {"id_queja": id_queja})
    # Devolvemos la primera fila (la queja buscada)
    return result.first()

#Funcion de actualizar el estado de la queja de oficina
def actualizar_estado_queja(db: Session, id_queja: int, nuevo_estado: str):
     # Llamamos al procedimiento almacenado `sp_actualizar_estado_queja`
    query = text("SELECT * FROM sp_actualizar_estado_queja(:id_queja, :nuevo_estado)")
    # Ejecutamos la consulta con los parámetros
    result = db.execute(query, {
        "id_queja": id_queja,
        "nuevo_estado": nuevo_estado
    })
    db.commit()
    return result.first()
