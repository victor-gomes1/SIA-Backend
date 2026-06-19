from app.db.connection import get_connection, get_cursor
from fastapi import HTTPException

def listar_chaves():
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT * FROM chaves ORDER BY id")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def buscar_chave_por_id(chave_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT * FROM chaves WHERE id = %s", (chave_id,))
        chave = cursor.fetchone()
        if not chave:
            raise HTTPException(status_code=404, detail="Chave não encontrada")
        return chave
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def buscar_chaves_por_status(status: str):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT * FROM chaves WHERE status = %s ORDER BY id", (status,))
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def criar_chave(dados):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT id FROM chaves WHERE codigo = %s", (dados.codigo,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Código de chave já cadastrado")

        cursor.execute("""
            INSERT INTO chaves (codigo, categoria, localizacao, status, observacao)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        """, (dados.codigo, dados.categoria, dados.localizacao, dados.status, dados.observacao))

        nova_chave = cursor.fetchone()
        conn.commit()
        return nova_chave
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def atualizar_chave(chave_id: int, dados):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT id FROM chaves WHERE id = %s", (chave_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Chave não encontrada")

        campos = []
        valores = []

        if dados.codigo is not None:
            campos.append("codigo = %s")
            valores.append(dados.codigo)
        if dados.categoria is not None:
            campos.append("categoria = %s")
            valores.append(dados.categoria)
        if dados.localizacao is not None:
            campos.append("localizacao = %s")
            valores.append(dados.localizacao)
        if dados.status is not None:
            campos.append("status = %s")
            valores.append(dados.status)
        if dados.observacao is not None:
            campos.append("observacao = %s")
            valores.append(dados.observacao)

        if not campos:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        campos.append("atualizado_em = CURRENT_TIMESTAMP")
        valores.append(chave_id)

        cursor.execute(f"""
            UPDATE chaves SET {', '.join(campos)}
            WHERE id = %s
            RETURNING *
        """, valores)

        chave_atualizada = cursor.fetchone()
        conn.commit()
        return chave_atualizada
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def deletar_chave(chave_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT id FROM chaves WHERE id = %s", (chave_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Chave não encontrada")

        cursor.execute("DELETE FROM chaves WHERE id = %s RETURNING id, codigo", (chave_id,))
        chave = cursor.fetchone()
        conn.commit()
        return {"message": "Chave deletada com sucesso!", "chave": chave}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()