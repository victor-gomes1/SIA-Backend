from fastapi import APIRouter, Depends
from app.models.movimentacao import MovimentacaoCreate, MovimentacaoResponse
from app.services import movimentacao_service
from app.core.dependencies import get_usuario_atual, require_admin
from typing import List, Optional

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])

@router.get("/", response_model=List[MovimentacaoResponse])
def listar_movimentacoes(usuario_atual=Depends(get_usuario_atual)):
    return movimentacao_service.listar_movimentacoes()

@router.get("/ativas", response_model=List[MovimentacaoResponse])
def listar_ativas(usuario_atual=Depends(get_usuario_atual)):
    return movimentacao_service.listar_movimentacoes_ativas()

@router.get("/usuario/{usuario_id}", response_model=List[MovimentacaoResponse])
def listar_por_usuario(usuario_id: int, usuario_atual=Depends(get_usuario_atual)):
    return movimentacao_service.listar_movimentacoes_por_usuario(usuario_id)

@router.get("/{movimentacao_id}", response_model=MovimentacaoResponse)
def buscar_movimentacao(movimentacao_id: int, usuario_atual=Depends(get_usuario_atual)):
    return movimentacao_service.buscar_movimentacao_por_id(movimentacao_id)

@router.post("/retirar", response_model=MovimentacaoResponse)
def retirar_chave(dados: MovimentacaoCreate, usuario_atual=Depends(get_usuario_atual)):
    return movimentacao_service.retirar_chave(dados)

@router.put("/devolver/{movimentacao_id}", response_model=MovimentacaoResponse)
def devolver_chave(movimentacao_id: int, observacao: Optional[str] = None, usuario_atual=Depends(get_usuario_atual)):
    return movimentacao_service.devolver_chave(movimentacao_id, observacao)

@router.put("/verificar-atrasos")
def verificar_atrasos(usuario_atual=Depends(require_admin)):
    return movimentacao_service.verificar_atrasos()