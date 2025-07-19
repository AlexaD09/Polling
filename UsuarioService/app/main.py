from fastapi import FastAPI
from pathlib import Path
from UsuarioService.app.routes import router 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="Usuario Service")

static_dir = Path(__file__).resolve().parents[2] / "Frontend" / "static"

app.mount("/static", StaticFiles(directory=static_dir), name="static")
# CORS
origins = [
    "http://localhost:8080",
    "http://localhost:8081",
    # Puedes agregar más orígenes si tienes otros frontends o ambientes
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Tu frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/usuarios", tags=["usuarios"])

@app.get("/")
def read_root():
    return {"message": "Usuario Service Running"}