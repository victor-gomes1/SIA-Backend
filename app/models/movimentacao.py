from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class TipoMovimentacaoEnum(str, Enum):
    retirada = "retirada"
    devolucao = "devolucao"

class StatusMovimentacaoEnum(str, Enum):
    em_uso = "em_uso"
    finalizada = "finalizada"
    atrasada = "atrasada"

# Dados necessários para criar uma movimentação
class MovimentacaoCreate(BaseModel):
    usuario_id: int
    chave_id: int
    tipo_movimentacao: TipoMovimentacaoEnum
    previsao_devolucao: Optional[datetime] = None
    dispositivo_id: Optional[int] = None
    observacao: Optional[str] = None

# Dados para atualizar uma movimentação
class MovimentacaoUpdate(BaseModel):
    tipo_movimentacao: Optional[TipoMovimentacaoEnum] = None
    previsao_devolucao: Optional[datetime] = None
    data_devolucao: Optional[datetime] = None
    status: Optional[StatusMovimentacaoEnum] = None
    observacao: Optional[str] = None

# Dados que a API devolve
class MovimentacaoResponse(BaseModel):
    id: int
    usuario_id: int
    chave_id: int
    tipo_movimentacao: TipoMovimentacaoEnum
    data_hora: datetime
    previsao_devolucao: Optional[datetime] = None
    data_devolucao: Optional[datetime] = None
    status: StatusMovimentacaoEnum
    dispositivo_id: Optional[int] = None
    observacao: Optional[str] = None