from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "quejas_db"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    try:
        # Ping para verificar conexión a Mongo
        await client.admin.command('ping')
        print("✅ Conectado a MongoDB correctamente")
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
