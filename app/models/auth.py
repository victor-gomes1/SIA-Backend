from pydantic import BaseModel
from typing import Optional

# Dados de login
class LoginRequest(BaseModel):
    email: str
    senha: str

# Resposta do login com o token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    nome: str
    tipo_usuario: str