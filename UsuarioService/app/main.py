from fastapi import FastAPI
from pathlib import Path
from app.routes import router 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="Usuario Service")

#frontend_path = Path(__file__).parent.parent.parent / "Frontend" / "static"
#app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# CORS
origins = [
    "http://frontend:80",
    "http://localhost:8081",
    "http://localhost:8080",
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