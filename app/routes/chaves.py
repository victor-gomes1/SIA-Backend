from fastapi import APIRouter, Depends
from app.models.chave import ChaveCreate, ChaveUpdate, ChaveResponse
from app.services import chave_service
from app.core.dependencies import get_usuario_atual, require_admin
from typing import List

router = APIRouter(prefix="/chaves", tags=["Chaves"])

@router.get("/", response_model=List[ChaveResponse])
def listar_chaves(usuario_atual=Depends(get_usuario_atual)):
    return chave_service.listar_chaves()

@router.get("/status/{status}", response_model=List[ChaveResponse])
def buscar_por_status(status: str, usuario_atual=Depends(get_usuario_atual)):
    return chave_service.buscar_chaves_por_status(status)

@router.get("/{chave_id}", response_model=ChaveResponse)
def buscar_chave(chave_id: int, usuario_atual=Depends(get_usuario_atual)):
    return chave_service.buscar_chave_por_id(chave_id)

@router.post("/", response_model=ChaveResponse)
def criar_chave(dados: ChaveCreate, usuario_atual=Depends(require_admin)):
    return chave_service.criar_chave(dados)

@router.put("/{chave_id}", response_model=ChaveResponse)
def atualizar_chave(chave_id: int, dados: ChaveUpdate, usuario_atual=Depends(require_admin)):
    return chave_service.atualizar_chave(chave_id, dados)

@router.delete("/{chave_id}")
def deletar_chave(chave_id: int, usuario_atual=Depends(require_admin)):
    return chave_service.deletar_chave(chave_id)