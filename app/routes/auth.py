from fastapi import APIRouter, HTTPException, status, Request
from app.models.auth import LoginRequest, TokenResponse
from app.core.security import verificar_senha, criar_token, hash_senha
from app.db.connection import get_connection, get_cursor

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=TokenResponse)
def login(request: Request, dados: LoginRequest):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        # Busca o usuário pelo email
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s AND status_acesso = 'ativo'",
            (dados.email,)
        )
        usuario = cursor.fetchone()

        # Verifica se o usuário existe e a senha está correta
        if not usuario or not verificar_senha(dados.senha, usuario["senha"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos"
            )

        # Gera o token JWT
        token = criar_token({
            "sub": str(usuario["id"]),
            "nome": usuario["nome"],
            "tipo_usuario": usuario["tipo_usuario"]
        })

        # Registra o log de acesso
        ip = request.client.host
        cursor.execute(
            "INSERT INTO logs_acesso (usuario_id, acao, ip_acesso) VALUES (%s, %s, %s)",
            (usuario["id"], "login", ip)
        )
        conn.commit()

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            usuario_id=usuario["id"],
            nome=usuario["nome"],
            tipo_usuario=usuario["tipo_usuario"]
        )
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/registrar-admin")
def registrar_admin(dados: dict):
    """Rota temporária para criar o primeiro admin do sistema"""
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        senha_hash = hash_senha(dados["senha"])
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, tipo_usuario, status_acesso)
            VALUES (%s, %s, %s, 'administrador', 'ativo')
            RETURNING id, nome, email, tipo_usuario
        """, (dados["nome"], dados["email"], senha_hash))
        novo_usuario = cursor.fetchone()
        conn.commit()
        return {"message": "Admin criado com sucesso!", "usuario": novo_usuario}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()