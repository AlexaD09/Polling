from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext
from app.config_usuario import SECRET_KEY,ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(id_usuario: Union[str, Any],nombre:str,email: str,role:str, expires_delta: int = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {
        "exp": expire, 
        "sub": str(id_usuario),
        "nombre": nombre,
        "email": email,
        "rol":role}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt