from fastapi import WebSocket

class ConnectionManager:
    """
    for managing the connection
    """
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    @staticmethod
    async def send_message(message: str, ws: WebSocket):
        await ws.send_text(message)

    async def send_message_to_downstream(self, data: str, ws: WebSocket):
        for connection in self.active_connections:
            if connection != ws:
                await connection.send_text(data)