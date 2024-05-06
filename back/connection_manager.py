class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, websocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def broadcast_to_game(self, game_id, message):
        for user_id, connection in self.active_connections.items():
            if user_id in self.game_sessions[game_id]:  # Assuming game_sessions tracks this
                await connection.send_text(message)
