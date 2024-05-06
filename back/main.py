from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
import connection_manager 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@app.post("/create_user")
async def create_user(user_data: schemas.UserData, db: Session = Depends(get_db)):
    try:
        new_user = models.User(username=user_data.user_name)
        user=db.query(models.User).filter(models.User.username==user_data.user_name).first()
        if user is None:
            db.add(new_user)

            db.commit()
       
        return {"success": True, "id": user.id, "username": user.username}
    except:
        
        return {"success": True, "id": user.id, "username": user.username}

@app.websocket("/ws/game/{game_id}/{user_id}")
async def game_socket(websocket: WebSocket, game_id: int, user_id: int, db: Session = Depends(get_db)):
    await connection_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = models.Message(user_id=user_id, game_id=game_id, content=data)
            db.add(message)
            db.commit()
            await connection_manager.broadcast_to_game(game_id, data)
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)
        await connection_manager.broadcast_to_game(game_id, f"User {user_id} left the game")

@app.websocket("/ws/{user_id}")
async def chat_socket(websocket: WebSocket, user_id: int):
    await connection_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast(f"User {user_id}: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)
        await connection_manager.broadcast(f"User {user_id} left the chat")

@app.get("/")
def read_root():
    return {"Hello": "World"}
