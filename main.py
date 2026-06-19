from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.connection import get_connection
from app.routes import auth, usuarios, chaves, movimentacoes, dispositivos, logs, websocket

app = FastAPI(
    title="SIA - Sistema Integrado Acadêmico",
    description="""
## Backend do Sistema de Gerenciamento de Chaves 🔑

O SIA é uma plataforma integrada de segurança e gestão de acesso para a Faculdade Senac.

### Funcionalidades:
- 🔐 **Autenticação** via JWT + bcrypt
- 👥 **Gestão de Usuários** com controle de perfis
- 🔑 **CRUD de Chaves** com controle de status
- 📋 **Movimentações** de retirada e devolução
- 📡 **Dispositivos IoT** ESP32
- 📝 **Logs de Acesso** imutáveis
- ⚡ **WebSocket** para dashboard em tempo real

### Como usar:
1. Faça login em **/auth/login** para obter o token JWT
2. Clique em **Authorize** e cole o token
3. Use as rotas normalmente
    """,
    version="1.0.0",
    contact={
        "name": "Equipe SIA",
        "email": "sia@senac.br"
    },
    license_info={
        "name": "MIT"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(chaves.router)
app.include_router(movimentacoes.router)
app.include_router(dispositivos.router)
app.include_router(logs.router)
app.include_router(websocket.router)

@app.get("/", tags=["Status"])
def root():
    return {"message": "SIA Backend rodando!", "versao": "1.0.0", "docs": "/docs"}

@app.get("/testar-banco", tags=["Status"])
def testar_banco():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "ok", "message": "Conexão com o banco bem sucedida!"}
    except Exception as e:
        return {"status": "erro", "message": str(e)}