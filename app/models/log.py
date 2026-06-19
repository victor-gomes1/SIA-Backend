from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Dados necessários para criar um log
class LogCreate(BaseModel):
    usuario_id: Optional[int] = None
    acao: str
    ip_acesso: Optional[str] = None

# Dados que a API devolve
class LogResponse(BaseModel):
    id: int
    usuario_id: Optional[int] = None
    acao: str
    ip_acesso: Optional[str] = None
    data_hora: Optional[datetime] = None