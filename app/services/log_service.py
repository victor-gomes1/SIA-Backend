from app.db.connection import get_connection, get_cursor
from fastapi import HTTPException

def listar_logs(limit: int = 100):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT l.*, u.nome as nome_usuario
            FROM logs_acesso l
            LEFT JOIN usuarios u ON l.usuario_id = u.id
            ORDER BY l.data_hora DESC
            LIMIT %s
        """, (limit,))
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def listar_logs_por_usuario(usuario_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT l.*, u.nome as nome_usuario
            FROM logs_acesso l
            LEFT JOIN usuarios u ON l.usuario_id = u.id
            WHERE l.usuario_id = %s
            ORDER BY l.data_hora DESC
        """, (usuario_id,))
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def listar_logs_por_acao(acao: str):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT l.*, u.nome as nome_usuario
            FROM logs_acesso l
            LEFT JOIN usuarios u ON l.usuario_id = u.id
            WHERE l.acao ILIKE %s
            ORDER BY l.data_hora DESC
        """, (f"%{acao}%",))
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def listar_logs_por_periodo(data_inicio: str, data_fim: str):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT l.*, u.nome as nome_usuario
            FROM logs_acesso l
            LEFT JOIN usuarios u ON l.usuario_id = u.id
            WHERE l.data_hora BETWEEN %s AND %s
            ORDER BY l.data_hora DESC
        """, (data_inicio, data_fim))
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def buscar_log_por_id(log_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            SELECT l.*, u.nome as nome_usuario
            FROM logs_acesso l
            LEFT JOIN usuarios u ON l.usuario_id = u.id
            WHERE l.id = %s
        """, (log_id,))
        log = cursor.fetchone()
        if not log:
            raise HTTPException(status_code=404, detail="Log não encontrado")
        return log
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()