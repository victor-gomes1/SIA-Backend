from fastapi import APIRouter, Depends
from app.models.log import LogResponse
from app.services import log_service
from app.core.dependencies import require_admin
from typing import List, Optional

router = APIRouter(prefix="/logs", tags=["Logs de Acesso"])

@router.get("/", response_model=List[LogResponse])
def listar_logs(limit: int = 100, usuario_atual=Depends(require_admin)):
    return log_service.listar_logs(limit)

@router.get("/usuario/{usuario_id}", response_model=List[LogResponse])
def listar_por_usuario(usuario_id: int, usuario_atual=Depends(require_admin)):
    return log_service.listar_logs_por_usuario(usuario_id)

@router.get("/acao/{acao}", response_model=List[LogResponse])
def listar_por_acao(acao: str, usuario_atual=Depends(require_admin)):
    return log_service.listar_logs_por_acao(acao)

@router.get("/periodo", response_model=List[LogResponse])
def listar_por_periodo(data_inicio: str, data_fim: str, usuario_atual=Depends(require_admin)):
    return log_service.listar_logs_por_periodo(data_inicio, data_fim)

@router.get("/{log_id}", response_model=LogResponse)
def buscar_log(log_id: int, usuario_atual=Depends(require_admin)):
    return log_service.buscar_log_por_id(log_id)