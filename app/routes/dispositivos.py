from fastapi import APIRouter, Depends
from app.models.dispositivo import DispositivoCreate, DispositivoUpdate, DispositivoResponse
from app.services import dispositivo_service
from app.core.dependencies import get_usuario_atual, require_admin
from typing import List

router = APIRouter(prefix="/dispositivos", tags=["Dispositivos IoT"])

@router.get("/", response_model=List[DispositivoResponse])
def listar_dispositivos(usuario_atual=Depends(get_usuario_atual)):
    return dispositivo_service.listar_dispositivos()

@router.get("/{dispositivo_id}", response_model=DispositivoResponse)
def buscar_dispositivo(dispositivo_id: int, usuario_atual=Depends(get_usuario_atual)):
    return dispositivo_service.buscar_dispositivo_por_id(dispositivo_id)

@router.post("/", response_model=DispositivoResponse)
def criar_dispositivo(dados: DispositivoCreate, usuario_atual=Depends(require_admin)):
    return dispositivo_service.criar_dispositivo(dados)

@router.put("/{dispositivo_id}", response_model=DispositivoResponse)
def atualizar_dispositivo(dispositivo_id: int, dados: DispositivoUpdate, usuario_atual=Depends(require_admin)):
    return dispositivo_service.atualizar_dispositivo(dispositivo_id, dados)

@router.put("/{dispositivo_id}/ping")
def ping_dispositivo(dispositivo_id: int):
    """Rota chamada pelo ESP32 para atualizar última conexão"""
    return dispositivo_service.atualizar_ultima_conexao(dispositivo_id)

@router.delete("/{dispositivo_id}")
def deletar_dispositivo(dispositivo_id: int, usuario_atual=Depends(require_admin)):
    return dispositivo_service.deletar_dispositivo(dispositivo_id)