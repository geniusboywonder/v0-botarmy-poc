import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)

class EnhancedConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_metadata: Dict[str, dict] = {}
        self.message_queue: Dict[str, List[str]] = {}

    async def connect(self, websocket: WebSocket, client_id: str = None) -> str:
        """
        Accepts a new WebSocket connection, assigns a unique client ID,
        and stores connection details.
        """
        await websocket.accept()
        if client_id is None:
            client_id = str(uuid.uuid4())

        self.active_connections[client_id] = websocket
        self.connection_metadata[client_id] = {
            "connected_at": datetime.utcnow().isoformat(),
            "user_agent": websocket.headers.get("user-agent", "unknown"),
            "client_id": client_id
        }
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")

        # Send a welcome message so the client can learn its ID
        welcome_message = {
            "type": "system",
            "event": "connected",
            "data": {
                "message": "Welcome to the BotArmy backend!",
                "client_id": client_id,
            },
        }
        try:
            await websocket.send_text(json.dumps(welcome_message))
        except Exception as e:
            logger.error(f"Failed to send welcome message to client {client_id}: {e}")


        # If there are queued messages for this client, send them
        if client_id in self.message_queue:
            num_queued = len(self.message_queue[client_id])
            messages_to_send = self.message_queue.pop(client_id)
            logger.info(f"Sending {num_queued} queued messages to client {client_id}...")
            for message in messages_to_send:
                # We use a direct send here to avoid re-queuing if it fails again
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Failed to send queued message to client {client_id}: {e}. Message lost.")
            logger.info(f"Finished sending queued messages for client {client_id}")

        return client_id

    async def disconnect(self, client_id: str, reason: str = "No reason given"):
        """
        Closes a client's connection and removes associated metadata.
        """
        websocket = self.active_connections.pop(client_id, None)
        self.connection_metadata.pop(client_id, None)

        if websocket:
            try:
                # Close the WebSocket connection gracefully
                await websocket.close(code=1000)
                logger.info(f"Client {client_id} disconnected gracefully. Reason: {reason}. Total connections: {len(self.active_connections)}")
            except Exception as e:
                # This can happen if the connection is already closed
                logger.warning(f"Error closing websocket for client {client_id} (might be already closed): {e}")
        else:
            logger.warning(f"Attempted to disconnect a non-existent or already disconnected client: {client_id}")

    def get_client_id(self, websocket: WebSocket) -> str | None:
        """
        Retrieves the client_id for a given WebSocket object.
        This is a reverse lookup and might be slow with many connections.
        """
        for client_id, ws in self.active_connections.items():
            if ws == websocket:
                return client_id
        return None

    async def send_to_client(self, client_id: str, message: str):
        """
        Sends a message to a specific client. If the client is disconnected,
        the message is queued.
        """
        websocket = self.active_connections.get(client_id)
        if websocket:
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send message to client {client_id}: {e}. Queuing message.")
                self._queue_message(client_id, message)
        else:
            logger.warning(f"Client {client_id} not connected. Queuing message.")
            self._queue_message(client_id, message)

    def _queue_message(self, client_id: str, message: str):
        """Helper to queue messages for disconnected clients."""
        if client_id not in self.message_queue:
            self.message_queue[client_id] = []
        self.message_queue[client_id].append(message)

    async def broadcast_to_all(self, message: str):
        """
        Broadcasts a message to all currently connected clients.
        """
        # Create a list of send tasks
        tasks = [self.send_to_client(client_id, message) for client_id in self.active_connections.keys()]
        # Run all send tasks concurrently
        await asyncio.gather(*tasks)

    def get_connection_stats(self) -> dict:
        """
        Returns statistics about the current connections for monitoring.
        """
        return {
            "active_connections": len(self.active_connections),
            "clients": list(self.connection_metadata.values()),
            "queued_messages": {client_id: len(messages) for client_id, messages in self.message_queue.items()}
        }
