from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token_admin():
    response = client.post("/auth/login", json={
        "email": "admin@senac.br",
        "senha": "admin123"
    })
    return response.json()["access_token"]

def test_listar_movimentacoes_sem_token():
    response = client.get("/movimentacoes/")
    assert response.status_code == 401

def test_listar_movimentacoes_com_token():
    token = get_token_admin()
    response = client.get("/movimentacoes/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_listar_movimentacoes_ativas():
    token = get_token_admin()
    response = client.get("/movimentacoes/ativas", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_retirar_chave_usuario_inexistente():
    token = get_token_admin()
    response = client.post("/movimentacoes/retirar", json={
        "usuario_id": 99999,
        "chave_id": 1,
        "tipo_movimentacao": "retirada"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_retirar_chave_inexistente():
    token = get_token_admin()
    response = client.post("/movimentacoes/retirar", json={
        "usuario_id": 1,
        "chave_id": 99999,
        "tipo_movimentacao": "retirada"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_devolver_movimentacao_inexistente():
    token = get_token_admin()
    response = client.put("/movimentacoes/devolver/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404