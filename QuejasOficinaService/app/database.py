from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
PSSW_POSTGRE=os.getenv("PSSW_POSTGRE")

# Conexion a la base de datos
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{PSSW_POSTGRE}@localhost:5432/quejas_db"
#Crea el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#Crea una fabrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base para definir modelos
Base = declarative_base() 