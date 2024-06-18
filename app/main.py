from fastapi import FastAPI, Depends, WebSocket, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, database, auth, websocket
from .routers import user, chat
from .websocket import ConnectionManager
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Include routers
app.include_router(user.router)
app.include_router(chat.router)

# WebSocket manager
manager = ConnectionManager()

@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room_name, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
