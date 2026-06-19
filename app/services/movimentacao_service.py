from app.db.connection import get_connection, get_cursor
from fastapi import HTTPException
from datetime import datetime
import json

# Importa o manager do websocket
from app.routes.websocket import manager
import asyncio

def listar_movimentacoes():
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT m.*, u.nome as nome_usuario, c.codigo as codigo_chave
            FROM movimentacoes_chaves m
            LEFT JOIN usuarios u ON m.usuario_id = u.id
            LEFT JOIN chaves c ON m.chave_id = c.id
            ORDER BY m.data_hora DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def buscar_movimentacao_por_id(movimentacao_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT m.*, u.nome as nome_usuario, c.codigo as codigo_chave
            FROM movimentacoes_chaves m
            LEFT JOIN usuarios u ON m.usuario_id = u.id
            LEFT JOIN chaves c ON m.chave_id = c.id
            WHERE m.id = %s
        """, (movimentacao_id,))
        movimentacao = cursor.fetchone()
        if not movimentacao:
            raise HTTPException(status_code=404, detail="Movimentação não encontrada")
        return movimentacao
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def retirar_chave(dados):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT id FROM usuarios WHERE id = %s AND status_acesso = 'ativo'", (dados.usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuário não encontrado ou inativo")

        cursor.execute("SELECT id, status FROM chaves WHERE id = %s", (dados.chave_id,))
        chave = cursor.fetchone()
        if not chave:
            raise HTTPException(status_code=404, detail="Chave não encontrada")
        if chave["status"] != "disponivel":
            raise HTTPException(status_code=400, detail="Chave não está disponível para retirada")

        cursor.execute("""
            INSERT INTO movimentacoes_chaves 
            (usuario_id, chave_id, tipo_movimentacao, previsao_devolucao, dispositivo_id, observacao, status)
            VALUES (%s, %s, 'retirada', %s, %s, %s, 'em_uso')
            RETURNING *
        """, (dados.usuario_id, dados.chave_id, dados.previsao_devolucao, dados.dispositivo_id, dados.observacao))
        movimentacao = cursor.fetchone()

        cursor.execute("""
            UPDATE chaves SET status = 'em_uso', atualizado_em = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (dados.chave_id,))

        cursor.execute("""
            INSERT INTO logs_acesso (usuario_id, acao, ip_acesso)
            VALUES (%s, %s, %s)
        """, (dados.usuario_id, f"retirada_chave_{dados.chave_id}", "sistema"))

        conn.commit()

        # Notifica o dashboard via WebSocket
        asyncio.create_task(manager.broadcast({
            "tipo": "retirada",
            "chave_id": dados.chave_id,
            "usuario_id": dados.usuario_id,
            "message": f"Chave {dados.chave_id} retirada pelo usuário {dados.usuario_id}"
        }))

        return movimentacao
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def devolver_chave(movimentacao_id: int, observacao: str = None):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT * FROM movimentacoes_chaves 
            WHERE id = %s AND tipo_movimentacao = 'retirada' AND status = 'em_uso'
        """, (movimentacao_id,))
        movimentacao = cursor.fetchone()
        if not movimentacao:
            raise HTTPException(status_code=404, detail="Movimentação ativa não encontrada")

        agora = datetime.utcnow()
        status_novo = "finalizada"
        if movimentacao["previsao_devolucao"] and agora > movimentacao["previsao_devolucao"]:
            status_novo = "atrasada"

        cursor.execute("""
            UPDATE movimentacoes_chaves 
            SET status = %s, data_devolucao = CURRENT_TIMESTAMP, observacao = COALESCE(%s, observacao)
            WHERE id = %s
            RETURNING *
        """, (status_novo, observacao, movimentacao_id))
        movimentacao_atualizada = cursor.fetchone()

        cursor.execute("""
            UPDATE chaves SET status = 'disponivel', atualizado_em = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (movimentacao["chave_id"],))

        cursor.execute("""
            INSERT INTO logs_acesso (usuario_id, acao, ip_acesso)
            VALUES (%s, %s, %s)
        """, (movimentacao["usuario_id"], f"devolucao_chave_{movimentacao['chave_id']}", "sistema"))

        conn.commit()

        # Notifica o dashboard via WebSocket
        asyncio.create_task(manager.broadcast({
            "tipo": "devolucao",
            "chave_id": movimentacao["chave_id"],
            "usuario_id": movimentacao["usuario_id"],
            "status": status_novo,
            "message": f"Chave {movimentacao['chave_id']} devolvida!"
        }))

        return movimentacao_atualizada
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def listar_movimentacoes_por_usuario(usuario_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT m.*, u.nome as nome_usuario, c.codigo as codigo_chave
            FROM movimentacoes_chaves m
            LEFT JOIN usuarios u ON m.usuario_id = u.id
            LEFT JOIN chaves c ON m.chave_id = c.id
            WHERE m.usuario_id = %s
            ORDER BY m.data_hora DESC
        """, (usuario_id,))
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def listar_movimentacoes_ativas():
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT m.*, u.nome as nome_usuario, c.codigo as codigo_chave
            FROM movimentacoes_chaves m
            LEFT JOIN usuarios u ON m.usuario_id = u.id
            LEFT JOIN chaves c ON m.chave_id = c.id
            WHERE m.status = 'em_uso'
            ORDER BY m.data_hora DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def verificar_atrasos():
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            UPDATE movimentacoes_chaves
            SET status = 'atrasada'
            WHERE status = 'em_uso'
            AND previsao_devolucao IS NOT NULL
            AND previsao_devolucao < CURRENT_TIMESTAMP
            RETURNING *
        """)
        atrasadas = cursor.fetchall()
        conn.commit()
        return {"message": f"{len(atrasadas)} movimentação(ões) marcada(s) como atrasada(s)", "atrasadas": atrasadas}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()