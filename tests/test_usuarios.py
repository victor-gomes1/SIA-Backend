from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token_admin():
    response = client.post("/auth/login", json={
        "email": "admin@senac.br",
        "senha": "admin123"
    })
    return response.json()["access_token"]

def test_listar_usuarios_sem_token():
    response = client.get("/usuarios/")
    assert response.status_code == 401

def test_listar_usuarios_com_token():
    token = get_token_admin()
    response = client.get("/usuarios/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_criar_usuario():
    import time
    token = get_token_admin()
    email = f"professor.{int(time.time())}@senac.br"
    response = client.post("/usuarios/", json={
        "nome": "Professor Teste",
        "email": email,
        "senha": "senha123",
        "tipo_usuario": "professor"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == email

def test_criar_usuario_email_duplicado():
    token = get_token_admin()
    client.post("/usuarios/", json={
        "nome": "Usuario Duplicado",
        "email": "duplicado@senac.br",
        "senha": "senha123",
        "tipo_usuario": "funcionario"
    }, headers={"Authorization": f"Bearer {token}"})

    response = client.post("/usuarios/", json={
        "nome": "Usuario Duplicado 2",
        "email": "duplicado@senac.br",
        "senha": "senha123",
        "tipo_usuario": "funcionario"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400

def test_buscar_usuario_inexistente():
    token = get_token_admin()
    response = client.get("/usuarios/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404