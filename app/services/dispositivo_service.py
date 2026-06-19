from app.db.connection import get_connection, get_cursor
from fastapi import HTTPException

def listar_dispositivos():
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT * FROM dispositivos_iot ORDER BY id")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def buscar_dispositivo_por_id(dispositivo_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT * FROM dispositivos_iot WHERE id = %s", (dispositivo_id,))
        dispositivo = cursor.fetchone()
        if not dispositivo:
            raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
        return dispositivo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def criar_dispositivo(dados):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        # Verifica se MAC já existe
        if dados.mac_address:
            cursor.execute("SELECT id FROM dispositivos_iot WHERE mac_address = %s", (dados.mac_address,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="MAC Address já cadastrado")

        cursor.execute("""
            INSERT INTO dispositivos_iot (nome_dispositivo, ip_dispositivo, mac_address, local_instalacao, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        """, (dados.nome_dispositivo, dados.ip_dispositivo, dados.mac_address, dados.local_instalacao, dados.status))

        novo_dispositivo = cursor.fetchone()
        conn.commit()
        return novo_dispositivo
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def atualizar_dispositivo(dispositivo_id: int, dados):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT id FROM dispositivos_iot WHERE id = %s", (dispositivo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Dispositivo não encontrado")

        campos = []
        valores = []

        if dados.nome_dispositivo is not None:
            campos.append("nome_dispositivo = %s")
            valores.append(dados.nome_dispositivo)
        if dados.ip_dispositivo is not None:
            campos.append("ip_dispositivo = %s")
            valores.append(dados.ip_dispositivo)
        if dados.mac_address is not None:
            campos.append("mac_address = %s")
            valores.append(dados.mac_address)
        if dados.local_instalacao is not None:
            campos.append("local_instalacao = %s")
            valores.append(dados.local_instalacao)
        if dados.status is not None:
            campos.append("status = %s")
            valores.append(dados.status)
        if dados.ultima_conexao is not None:
            campos.append("ultima_conexao = %s")
            valores.append(dados.ultima_conexao)

        if not campos:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        valores.append(dispositivo_id)

        cursor.execute(f"""
            UPDATE dispositivos_iot SET {', '.join(campos)}
            WHERE id = %s
            RETURNING *
        """, valores)

        dispositivo_atualizado = cursor.fetchone()
        conn.commit()
        return dispositivo_atualizado
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def atualizar_ultima_conexao(dispositivo_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("""
            UPDATE dispositivos_iot 
            SET ultima_conexao = CURRENT_TIMESTAMP, status = 'online'
            WHERE id = %s
            RETURNING *
        """, (dispositivo_id,))
        dispositivo = cursor.fetchone()
        if not dispositivo:
            raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
        conn.commit()
        return dispositivo
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def deletar_dispositivo(dispositivo_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT id FROM dispositivos_iot WHERE id = %s", (dispositivo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Dispositivo não encontrado")

        cursor.execute("DELETE FROM dispositivos_iot WHERE id = %s RETURNING id, nome_dispositivo", (dispositivo_id,))
        dispositivo = cursor.fetchone()
        conn.commit()
        return {"message": "Dispositivo deletado com sucesso!", "dispositivo": dispositivo}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()