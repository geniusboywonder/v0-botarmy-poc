import asyncio
import json
import logging
from typing import Dict

from backend.simple_connection_manager import SimpleConnectionManager

logger = logging.getLogger(__name__)

class HeartbeatService:
    """
    A service that sends heartbeats to connected clients to keep connections alive.
    Adheres to the Single Responsibility Principle.
    """

    def __init__(self, connection_manager: SimpleConnectionManager, interval: int = 30):
        self.connection_manager = connection_manager
        self.interval = interval
        self._task = None

    async def start(self):
        """Starts the heartbeat service."""
        if self._task is None:
            self._task = asyncio.create_task(self._run())
            logger.info("Heartbeat service started.")

    async def stop(self):
        """Stops the heartbeat service."""
        if self._task:
            self._task.cancel()
            self._task = None
            logger.info("Heartbeat service stopped.")

    async def _run(self):
        """The main loop of the heartbeat service."""
        while True:
            await asyncio.sleep(self.interval)
            logger.debug("Sending heartbeat pings to all clients.")
            await self.connection_manager.broadcast(json.dumps({"type": "ping"}))