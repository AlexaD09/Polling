from dotenv import load_dotenv
import os

load_dotenv()

PSSW_POSTGRE= os.getenv("PSSW_POSTGRE")
print("CONFIG PASSWORD POSTGRES",PSSW_POSTGRE)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv ("ALGORITHM")
