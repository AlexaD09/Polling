from bson.objectid import ObjectId

class QuejaDAO:
    def __init__(self, db):
        self.collection = db['quejas']
#Crear queja en mongo o insterta nueva queja en la colecion de mongo
    async def crear_queja(self, queja_data):
        resultado = await self.collection.insert_one(queja_data)
        return str(resultado.inserted_id)
#Consulta queja especifica desde su id
    async def obtener_queja_por_id(self, id_queja):
        queja = await self.collection.find_one({"_id": ObjectId(id_queja)})
        return queja
#Cambia el estado de una queja
    async def actualizar_estado(self, id_queja, nuevo_estado):
        resultado = await self.collection.update_one(
            {"_id": ObjectId(id_queja)},
            {"$set": {"estado": nuevo_estado}}
        )
        return resultado.modified_count
#Devuelve todas las quejas registradas por usuario
    async def obtener_quejas_por_usuario(self, id_usuario: str):
        cursor = self.collection.find({"id_usuario": id_usuario})
        quejas = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])  # Convertimos el ObjectId a string
            quejas.append(doc)
        return quejas

    async def listar_todas(self):
        cursor = self.collection.find()
        quejas = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])  # Convertimos el ObjectId a string para el frontend
            quejas.append(doc)
        return quejas
