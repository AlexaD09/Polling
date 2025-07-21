from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.database import client

app = FastAPI()

# Configuración CORS para permitir peticiones desde tu frontend (localhost:8080)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # ✅ Importante: especificar bien los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("✅ Microservicio de quejas iniciado")

@app.on_event("shutdown")
async def shutdown_event():
    client.close()
    print("🛑 Conexión a Mongo cerrada")

app.include_router(router)
