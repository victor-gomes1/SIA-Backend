from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verificar_token
from app.db.connection import get_connection, get_cursor

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_usuario_atual(token: str = Depends(oauth2_scheme)):
    """Verifica se o token é válido e retorna os dados do usuário"""
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

def require_admin(usuario: dict = Depends(get_usuario_atual)):
    """Verifica se o usuário é administrador"""
    if usuario.get("tipo_usuario") != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return usuario