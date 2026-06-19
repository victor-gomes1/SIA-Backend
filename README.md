# SIA - Sistema Integrado Acadêmico
## Backend

Backend do sistema de gerenciamento de chaves da Faculdade Senac, desenvolvido com FastAPI e Python. O sistema permite o controle de retirada e devolução de chaves de salas de aula, integrado a dispositivos IoT (ESP32) via RFID.

---

## Tecnologias Utilizadas

- **Python 3.13**
- **FastAPI** — framework web
- **psycopg2** — driver de conexão com PostgreSQL
- **Supabase** — banco de dados PostgreSQL em nuvem
- **JWT** — autenticação por token
- **bcrypt** — criptografia de senhas
- **WebSocket** — comunicação em tempo real
- **pytest** — testes automatizados
- **Uvicorn** — servidor ASGI

---

## Estrutura do Projeto

```
SIA-Backend/
├── app/
│   ├── core/
│   │   ├── dependencies.py       # Middlewares de autenticação
│   │   └── security.py           # JWT e bcrypt
│   ├── db/
│   │   └── connection.py         # Conexão com o banco
│   ├── models/
│   │   ├── auth.py               # Schema de login e token
│   │   ├── chave.py              # Schema de chaves
│   │   ├── dispositivo.py        # Schema de dispositivos IoT
│   │   ├── log.py                # Schema de logs
│   │   ├── movimentacao.py       # Schema de movimentações
│   │   └── usuario.py            # Schema de usuários
│   ├── routes/
│   │   ├── auth.py               # Rotas de autenticação
│   │   ├── chaves.py             # Rotas de chaves
│   │   ├── dispositivos.py       # Rotas de dispositivos IoT
│   │   ├── logs.py               # Rotas de logs
│   │   ├── movimentacoes.py      # Rotas de movimentações
│   │   ├── usuarios.py           # Rotas de usuários
│   │   └── websocket.py          # WebSocket para dashboard
│   └── services/
│       ├── chave_service.py      # Lógica de negócio de chaves
│       ├── dispositivo_service.py # Lógica de dispositivos IoT
│       ├── log_service.py        # Lógica de logs
│       ├── movimentacao_service.py # Lógica de movimentações
│       └── usuario_service.py    # Lógica de usuários
├── tests/
│   ├── test_auth.py
│   ├── test_chaves.py
│   ├── test_movimentacoes.py
│   └── test_usuarios.py
├── main.py
├── .env                          # Variáveis de ambiente (não versionar)
├── .gitignore
└── requirements.txt
```

---

## Pré-requisitos

- Python 3.11 ou superior instalado
- Acesso ao projeto no Supabase com o banco de dados configurado
- Git instalado

---

## Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/sia-backend.git
cd sia-backend
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

A `DATABASE_URL` pode ser obtida no Supabase em **Settings > Database > Connection string > URI**.

### 5. Execute o servidor

```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`.

---

## Documentação da API

Com o servidor rodando, acesse a documentação interativa gerada automaticamente pelo FastAPI:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **Redoc:** `http://127.0.0.1:8000/redoc`

---

## Autenticação

A API utiliza autenticação via JWT. Para acessar as rotas protegidas:

1. Faça uma requisição `POST /auth/login` com email e senha
2. Copie o `access_token` retornado
3. Inclua o token no header de cada requisição: `Authorization: Bearer <token>`

No Swagger, clique no botão **Authorize** e cole o token para testar as rotas diretamente.

---

## Rotas Disponíveis

### Autenticação
| Método | Rota | Descricao |
|--------|------|-----------|
| POST | `/auth/login` | Realiza login e retorna o token JWT |
| POST | `/auth/registrar-admin` | Cria o primeiro administrador do sistema |

### Usuarios
| Método | Rota | Descricao |
|--------|------|-----------|
| GET | `/usuarios/` | Lista todos os usuários (admin) |
| GET | `/usuarios/{id}` | Busca usuário por ID |
| POST | `/usuarios/` | Cadastra novo usuário (admin) |
| PUT | `/usuarios/{id}` | Atualiza dados do usuário (admin) |
| DELETE | `/usuarios/{id}` | Inativa usuário (admin) |

### Chaves
| Método | Rota | Descricao |
|--------|------|-----------|
| GET | `/chaves/` | Lista todas as chaves |
| GET | `/chaves/{id}` | Busca chave por ID |
| GET | `/chaves/status/{status}` | Filtra chaves por status |
| POST | `/chaves/` | Cadastra nova chave (admin) |
| PUT | `/chaves/{id}` | Atualiza dados da chave (admin) |
| DELETE | `/chaves/{id}` | Remove chave (admin) |

### Movimentacoes
| Método | Rota | Descricao |
|--------|------|-----------|
| GET | `/movimentacoes/` | Lista todas as movimentações |
| GET | `/movimentacoes/ativas` | Lista movimentações em aberto |
| GET | `/movimentacoes/{id}` | Busca movimentação por ID |
| GET | `/movimentacoes/usuario/{id}` | Lista movimentações por usuário |
| POST | `/movimentacoes/retirar` | Registra retirada de chave |
| PUT | `/movimentacoes/devolver/{id}` | Registra devolução de chave |
| PUT | `/movimentacoes/verificar-atrasos` | Atualiza status de atrasos (admin) |

### Dispositivos IoT
| Método | Rota | Descricao |
|--------|------|-----------|
| GET | `/dispositivos/` | Lista todos os dispositivos |
| GET | `/dispositivos/{id}` | Busca dispositivo por ID |
| POST | `/dispositivos/` | Cadastra novo dispositivo (admin) |
| PUT | `/dispositivos/{id}` | Atualiza dispositivo (admin) |
| PUT | `/dispositivos/{id}/ping` | Atualiza última conexão do ESP32 |
| DELETE | `/dispositivos/{id}` | Remove dispositivo (admin) |

### Logs de Acesso
| Método | Rota | Descricao |
|--------|------|-----------|
| GET | `/logs/` | Lista logs recentes (admin) |
| GET | `/logs/{id}` | Busca log por ID (admin) |
| GET | `/logs/usuario/{id}` | Filtra logs por usuário (admin) |
| GET | `/logs/acao/{acao}` | Filtra logs por ação (admin) |
| GET | `/logs/periodo` | Filtra logs por período (admin) |

### WebSocket
| Tipo | Rota | Descricao |
|------|------|-----------|
| WS | `/ws/dashboard` | Canal em tempo real para o dashboard |

---

## Executando os Testes

```bash
pytest tests/ -v
```

---

## Observacoes

- Os logs de acesso são imutáveis — não podem ser editados ou excluídos após gerados.
- As senhas são armazenadas com hash bcrypt, nunca em texto puro.
- O token JWT expira em 60 minutos por padrão, configurável no `.env`.
- O arquivo `.env` não deve ser versionado no Git.
- A rota `/auth/registrar-admin` deve ser usada apenas para criar o primeiro administrador do sistema.

---

## Equipe

Agnes Ribeiro, Arthur Silveira, Joao Ricardo, Matheus Willian, Pedro , Vanessa Matias, Victor Gomes, Wedja Sousa.
