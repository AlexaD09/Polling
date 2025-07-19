from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "quejas_db"
#Conexion a mongodb
client = AsyncIOMotorClient(MONGO_URL)#cliente asíncrono de mongo
db = client[DB_NAME]


