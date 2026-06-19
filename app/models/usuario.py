from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class TipoUsuarioEnum(str, Enum):
    funcionario = "funcionario"
    professor = "professor"
    administrador = "administrador"

class StatusAcessoEnum(str, Enum):
    ativo = "ativo"
    inativo = "inativo"

# Dados necessários para criar um usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    matricula: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    departamento: Optional[str] = None
    funcao: Optional[str] = None
    tipo_usuario: TipoUsuarioEnum

# Dados para atualizar um usuário
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    departamento: Optional[str] = None
    funcao: Optional[str] = None
    tipo_usuario: Optional[TipoUsuarioEnum] = None
    status_acesso: Optional[StatusAcessoEnum] = None

# Dados que a API devolve (nunca devolve a senha!)
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    matricula: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    departamento: Optional[str] = None
    funcao: Optional[str] = None
    tipo_usuario: TipoUsuarioEnum
    status_acesso: StatusAcessoEnum
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None