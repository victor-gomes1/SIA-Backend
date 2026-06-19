from fastapi import APIRouter, Depends
from app.models.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services import usuario_service
from app.core.dependencies import get_usuario_atual, require_admin
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(usuario_atual=Depends(require_admin)):
    return usuario_service.listar_usuarios()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int, usuario_atual=Depends(get_usuario_atual)):
    return usuario_service.buscar_usuario_por_id(usuario_id)

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(dados: UsuarioCreate, usuario_atual=Depends(require_admin)):
    return usuario_service.criar_usuario(dados)

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, usuario_atual=Depends(require_admin)):
    return usuario_service.atualizar_usuario(usuario_id, dados)

@router.delete("/{usuario_id}")
def inativar_usuario(usuario_id: int, usuario_atual=Depends(require_admin)):
    return usuario_service.inativar_usuario(usuario_id)