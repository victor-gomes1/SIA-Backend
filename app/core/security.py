from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from dotenv import load_dotenv
import bcrypt
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def hash_senha(senha: str) -> str:
    """Criptografa a senha com bcrypt"""
    senha_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha_bytes, salt).decode("utf-8")

def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """Verifica se a senha bate com o hash"""
    return bcrypt.checkpw(senha_pura.encode("utf-8"), senha_hash.encode("utf-8"))

def criar_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera o token JWT"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str) -> Optional[dict]:
    """Verifica e decodifica o token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None