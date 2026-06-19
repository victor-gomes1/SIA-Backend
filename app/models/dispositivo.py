from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class StatusDispositivoEnum(str, Enum):
    online = "online"
    offline = "offline"
    manutencao = "manutencao"

# Dados necessários para criar um dispositivo
class DispositivoCreate(BaseModel):
    nome_dispositivo: str
    ip_dispositivo: Optional[str] = None
    mac_address: Optional[str] = None
    local_instalacao: Optional[str] = None
    status: Optional[StatusDispositivoEnum] = StatusDispositivoEnum.online

# Dados para atualizar um dispositivo
class DispositivoUpdate(BaseModel):
    nome_dispositivo: Optional[str] = None
    ip_dispositivo: Optional[str] = None
    mac_address: Optional[str] = None
    local_instalacao: Optional[str] = None
    status: Optional[StatusDispositivoEnum] = None
    ultima_conexao: Optional[datetime] = None

# Dados que a API devolve
class DispositivoResponse(BaseModel):
    id: int
    nome_dispositivo: str
    ip_dispositivo: Optional[str] = None
    mac_address: Optional[str] = None
    local_instalacao: Optional[str] = None
    status: StatusDispositivoEnum
    ultima_conexao: Optional[datetime] = None
    criado_em: Optional[datetime] = None