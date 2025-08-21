import asyncio
import time
import logging
from typing import Dict

# Use a forward reference for the type hint to avoid circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.connection_manager import EnhancedConnectionManager

from backend.agui.protocol import MessageProtocol

logger = logging.getLogger(__name__)

class HeartbeatMonitor:
    def __init__(self, connection_manager: 'EnhancedConnectionManager', heartbeat_interval: int = 30, client_timeout: int = 90):
        """
        Initializes the HeartbeatMonitor.

        Args:
            connection_manager: The singleton instance of EnhancedConnectionManager.
            heartbeat_interval: How often to send heartbeats (in seconds).
            client_timeout: How long to wait for a client response before disconnecting (in seconds).
        """
        self.connection_manager = connection_manager
        self.heartbeat_interval = heartbeat_interval
        self.client_timeout = client_timeout
        self.client_last_seen: Dict[str, float] = {}
        self._task: asyncio.Task = None

    async def start(self):
        """Starts the heartbeat monitor as a background task."""
        if self._task is None:
            self._task = asyncio.create_task(self._heartbeat_loop())
            logger.info("Heartbeat monitor started.")

    async def stop(self):
        """Stops the heartbeat monitor."""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                logger.info("Heartbeat monitor stopped successfully.")
            self._task = None

    async def _heartbeat_loop(self):
        """The main loop that sends heartbeats and checks for timeouts."""
        while True:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                logger.info("Sending heartbeats to all clients...")
                await self._send_heartbeat_to_all()
                await self._check_client_timeouts()
            except asyncio.CancelledError:
                logger.info("Heartbeat loop is being cancelled.")
                break
            except Exception as e:
                logger.error(f"An error occurred in the heartbeat loop: {e}", exc_info=True)
                # Avoid crashing the loop on unexpected errors
                await asyncio.sleep(5)

    async def _send_heartbeat_to_all(self):
        """Sends a heartbeat message to all connected clients."""
        heartbeat_message = MessageProtocol.create_heartbeat_message()
        # Use a copy of the client IDs to avoid issues if the dictionary changes during iteration
        client_ids = list(self.connection_manager.active_connections.keys())
        for client_id in client_ids:
            # We assume the client is new until they respond to a heartbeat
            if client_id not in self.client_last_seen:
                self.client_last_seen[client_id] = time.time()

            await self.connection_manager.send_to_client(
                client_id,
                # The message protocol returns a dict, we need to serialize it
                # Let's assume the connection manager's send_to_client handles serialization
                # Or better, let's serialize it here.
                # Reading `connection_manager.py` again, it expects a string.
                # Let's import json.
                __import__('json').dumps(heartbeat_message)
            )

    def handle_heartbeat_response(self, client_id: str):
        """Updates the last seen timestamp for a client."""
        if client_id in self.connection_manager.active_connections:
            self.client_last_seen[client_id] = time.time()
            logger.info(f"Received heartbeat response from client {client_id}")
        else:
            logger.warning(f"Received heartbeat response from unknown or disconnected client {client_id}")


    async def _check_client_timeouts(self):
        """Disconnects clients that have not responded within the timeout period."""
        current_time = time.time()
        # Use a copy of the items to avoid runtime errors if the dict changes
        timed_out_clients = [
            client_id for client_id, last_seen in self.client_last_seen.items()
            if current_time - last_seen > self.client_timeout
        ]

        for client_id in timed_out_clients:
            logger.warning(f"Client {client_id} timed out. Last seen {current_time - self.client_last_seen[client_id]:.2f}s ago. Disconnecting.")
            await self.connection_manager.disconnect(client_id, reason="Heartbeat timeout")
            # Clean up the entry for the disconnected client
            self.client_last_seen.pop(client_id, None)
