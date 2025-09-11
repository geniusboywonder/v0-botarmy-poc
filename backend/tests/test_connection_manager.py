import asyncio
import pytest_asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.connection_manager import EnhancedConnectionManager

@pytest_asyncio.fixture
async def manager():
    m = EnhancedConnectionManager()
    
    yield m

@pytest.mark.asyncio
async def test_connect_disconnect(manager: EnhancedConnectionManager):
    websocket = AsyncMock()
    client_id = await manager.connect(websocket)
    assert client_id in manager.active_connections
    await manager.disconnect(client_id)
    assert client_id not in manager.active_connections

@pytest.mark.asyncio
async def test_send_to_client(manager: EnhancedConnectionManager):
    websocket = AsyncMock()
    client_id = await manager.connect(websocket)
    await manager.send_to_client(client_id, "test message")
    assert websocket.send_text.call_count == 3
    await manager.disconnect(client_id)

@pytest.mark.asyncio
async def test_broadcast(manager: EnhancedConnectionManager):
    websocket1 = AsyncMock()
    websocket2 = AsyncMock()
    client_id1 = await manager.connect(websocket1)
    client_id2 = await manager.connect(websocket2)

    await manager.broadcast_to_all("broadcast message")

    assert websocket1.send_text.call_count == 3
    assert websocket2.send_text.call_count == 3

    await manager.disconnect(client_id1)
    await manager.disconnect(client_id2)
