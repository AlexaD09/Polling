from fastapi import FastAPI
from UsuarioService.app.routes import router 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Usuario Service")

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Tu frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/usuarios", tags=["usuarios"])

@app.get("/")
def read_root():
    return {"message": "Usuario Service Running"}