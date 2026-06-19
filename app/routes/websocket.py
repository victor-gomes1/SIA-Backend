from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

router = APIRouter(tags=["WebSocket"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Cliente conectado. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Cliente desconectado. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Envia mensagem para todos os clientes conectados"""
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Manda mensagem de boas vindas
        await websocket.send_text(json.dumps({
            "tipo": "conexao",
            "message": "Conectado ao dashboard SIA em tempo real!"
        }))
        # Fica ouvindo mensagens do cliente
        while True:
            data = await websocket.receive_text()
            print(f"Mensagem recebida: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)