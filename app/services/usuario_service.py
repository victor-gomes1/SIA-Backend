from app.db.connection import get_connection, get_cursor
from app.core.security import hash_senha
from fastapi import HTTPException

def listar_usuarios():
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT id, nome, email, matricula, cpf, telefone, departamento, funcao, tipo_usuario, status_acesso, criado_em, atualizado_em FROM usuarios")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def buscar_usuario_por_id(usuario_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT id, nome, email, matricula, cpf, telefone, departamento, funcao, tipo_usuario, status_acesso, criado_em, atualizado_em FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def criar_usuario(dados):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        # Verifica se email já existe
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (dados.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")

        # Verifica se CPF já existe
        if dados.cpf:
            cursor.execute("SELECT id FROM usuarios WHERE cpf = %s", (dados.cpf,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="CPF já cadastrado")

        # Verifica se matrícula já existe
        if dados.matricula:
            cursor.execute("SELECT id FROM usuarios WHERE matricula = %s", (dados.matricula,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Matrícula já cadastrada")

        senha_hash = hash_senha(dados.senha)

        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, matricula, cpf, telefone, departamento, funcao, tipo_usuario, status_acesso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'ativo')
            RETURNING id, nome, email, matricula, cpf, telefone, departamento, funcao, tipo_usuario, status_acesso, criado_em, atualizado_em
        """, (dados.nome, dados.email, senha_hash, dados.matricula, dados.cpf, dados.telefone, dados.departamento, dados.funcao, dados.tipo_usuario))

        novo_usuario = cursor.fetchone()
        conn.commit()
        return novo_usuario
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def atualizar_usuario(usuario_id: int, dados):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        # Verifica se usuário existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Monta os campos que foram enviados
        campos = []
        valores = []

        if dados.nome is not None:
            campos.append("nome = %s")
            valores.append(dados.nome)
        if dados.email is not None:
            campos.append("email = %s")
            valores.append(dados.email)
        if dados.telefone is not None:
            campos.append("telefone = %s")
            valores.append(dados.telefone)
        if dados.departamento is not None:
            campos.append("departamento = %s")
            valores.append(dados.departamento)
        if dados.funcao is not None:
            campos.append("funcao = %s")
            valores.append(dados.funcao)
        if dados.tipo_usuario is not None:
            campos.append("tipo_usuario = %s")
            valores.append(dados.tipo_usuario)
        if dados.status_acesso is not None:
            campos.append("status_acesso = %s")
            valores.append(dados.status_acesso)

        if not campos:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        campos.append("atualizado_em = CURRENT_TIMESTAMP")
        valores.append(usuario_id)

        cursor.execute(f"""
            UPDATE usuarios SET {', '.join(campos)}
            WHERE id = %s
            RETURNING id, nome, email, matricula, cpf, telefone, departamento, funcao, tipo_usuario, status_acesso, criado_em, atualizado_em
        """, valores)

        usuario_atualizado = cursor.fetchone()
        conn.commit()
        return usuario_atualizado
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def inativar_usuario(usuario_id: int):
    conn = get_connection()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        cursor.execute("""
            UPDATE usuarios SET status_acesso = 'inativo', atualizado_em = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, nome, status_acesso
        """, (usuario_id,))

        usuario = cursor.fetchone()
        conn.commit()
        return {"message": "Usuário inativado com sucesso!", "usuario": usuario}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()