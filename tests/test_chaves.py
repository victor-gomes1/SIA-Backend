from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token_admin():
    response = client.post("/auth/login", json={
        "email": "admin@senac.br",
        "senha": "admin123"
    })
    return response.json()["access_token"]

def test_listar_chaves_sem_token():
    response = client.get("/chaves/")
    assert response.status_code == 401

def test_listar_chaves_com_token():
    token = get_token_admin()
    response = client.get("/chaves/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_criar_chave():
    import time
    token = get_token_admin()
    codigo = f"SALA-TESTE-{int(time.time())}"
    response = client.post("/chaves/", json={
        "codigo": codigo,
        "categoria": "Sala de Aula",
        "localizacao": "Bloco A",
        "status": "disponivel"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["codigo"] == codigo

def test_criar_chave_codigo_duplicado():
    token = get_token_admin()
    client.post("/chaves/", json={
        "codigo": "SALA-DUPLICADA",
        "categoria": "Sala de Aula"
    }, headers={"Authorization": f"Bearer {token}"})

    response = client.post("/chaves/", json={
        "codigo": "SALA-DUPLICADA",
        "categoria": "Sala de Aula"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400

def test_buscar_chave_inexistente():
    token = get_token_admin()
    response = client.get("/chaves/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_buscar_chaves_por_status():
    token = get_token_admin()
    response = client.get("/chaves/status/disponivel", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)