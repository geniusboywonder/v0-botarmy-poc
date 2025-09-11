import asyncio
import json
import logging
import uuid
from typing import Dict, Set

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

class SimpleConnectionManager:
    """
    A simple WebSocket connection manager that adheres to the Single Responsibility Principle.
    Its only responsibility is to manage WebSocket connections.
    """

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        """Accepts a new WebSocket connection."""
        await websocket.accept()
        client_id = str(uuid.uuid4())
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")
        return client_id

    async def disconnect(self, client_id: str):
        """Disconnects a WebSocket client."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")

    async def send_to_client(self, client_id: str, message: str):
        """Sends a message to a specific client."""
        websocket = self.active_connections.get(client_id)
        if websocket:
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                await self.disconnect(client_id)

    async def broadcast(self, message: str):
        """Broadcasts a message to all connected clients."""
        for client_id in list(self.active_connections):
            await self.send_to_client(client_id, message)