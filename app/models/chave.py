from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class StatusChaveEnum(str, Enum):
    disponivel = "disponivel"
    em_uso = "em_uso"
    pendente = "pendente"

# Dados necessários para criar uma chave
class ChaveCreate(BaseModel):
    codigo: str
    categoria: Optional[str] = None
    localizacao: Optional[str] = None
    status: Optional[StatusChaveEnum] = StatusChaveEnum.disponivel
    observacao: Optional[str] = None

# Dados para atualizar uma chave
class ChaveUpdate(BaseModel):
    codigo: Optional[str] = None
    categoria: Optional[str] = None
    localizacao: Optional[str] = None
    status: Optional[StatusChaveEnum] = None
    observacao: Optional[str] = None

# Dados que a API devolve
class ChaveResponse(BaseModel):
    id: int
    codigo: str
    categoria: Optional[str] = None
    localizacao: Optional[str] = None
    status: StatusChaveEnum
    observacao: Optional[str] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None