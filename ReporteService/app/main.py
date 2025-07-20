import asyncio
from fastapi import FastAPI
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import router as reporte_router
from app.polling import polling_periodico

app = FastAPI()

#frontend_path = Path(__file__).parent.parent.parent / "Frontend" / "static"
#app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

origins = [
    "http://frontend:80",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reporte_router)

@app.on_event("startup")
async def startup_event():
    # Lanza el polling en background task
    asyncio.create_task(polling_periodico(intervalo_segundos=30))
