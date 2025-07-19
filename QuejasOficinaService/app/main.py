from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
import uvicorn
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
#Intsancia de fastapi 
app = FastAPI() 

frontend_path = Path(__file__).parent.parent.parent / "Frontend" / "static"
app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
# CORS permite al backend responder solicitudes desde otros dominios
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8081",
    "http://localhost:8082",
    # Puedes agregar más orígenes si tienes otros frontends o ambientes
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Tu frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router, prefix="/oficina")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)