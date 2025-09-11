import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from unittest.mock import AsyncMock, patch
import sys
from pathlib import Path

# Add project root to path to allow absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Import the FastAPI app from backend.main
from backend.main import app

@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client

# Mock the handle_websocket_message to prevent side effects during testing
@pytest.fixture(autouse=True)
def mock_handle_websocket_message():
    with patch('backend.main.handle_websocket_message', new_callable=AsyncMock) as mock_handle:
        yield mock_handle

@pytest.mark.asyncio
async def test_general_websocket_connection(test_app):
    """
    Tests that a general WebSocket connection can be established and receives initial messages.
    """
    with test_app.websocket_connect("/ws/general/test_session_general") as websocket:
        # Expecting the welcome message
        response = websocket.receive_json()
        assert response["type"] == "system"
        assert response["event"] == "connected"
        assert "Welcome" in response["data"]["message"]

        # Expecting the connection established message
        response = websocket.receive_json()
        assert response["type"] == "agent_response"
        assert "WebSocket connection established successfully!" in response["content"]

@pytest.mark.asyncio
async def test_general_websocket_ping_pong(test_app):
    """
    Tests the ping-pong functionality for a general WebSocket session.
    """
    with test_app.websocket_connect("/ws/general/test_session_ping_pong") as websocket:
        # Consume initial messages
        websocket.receive_json()
        websocket.receive_json()

        websocket.send_json({"type": "ping"})
        
        # Loop to consume messages until 'pong' is received or max attempts
        max_attempts = 5
        for _ in range(max_attempts):
            response = websocket.receive_json()
            if response.get("type") == "pong":
                assert response["type"] == "pong"
                return # Test passed
            print(f"Received unexpected message type: {response.get('type')}")
        
        pytest.fail(f"Did not receive 'pong' message after {max_attempts} attempts.")

@pytest.mark.asyncio
async def test_general_websocket_echo(mock_handle_websocket_message, test_app):
    """
    Tests that handle_websocket_message is called for a general WebSocket session.
    """
    test_message = {"type": "user_message", "content": "Hello, WebSocket!"}
    with test_app.websocket_connect("/ws/general/test_session_echo") as websocket:
        # Consume initial messages
        websocket.receive_json()
        websocket.receive_json()

        print(f"Sending message: {test_message}")
        websocket.send_json(test_message)
        
        # Add a small delay to allow the server to process the message
        await asyncio.sleep(0.1) 
        
        print(f"Mock call count: {mock_handle_websocket_message.call_count}")
        mock_handle_websocket_message.assert_called_once_with(
            "test_session_echo", # client_id is session_id for general type
            test_message,
            websocket.app.state.manager,
            websocket.app.state.heartbeat_monitor,
            websocket.app.state.status_broadcaster,
            websocket.app.state
        )

@pytest.mark.asyncio
async def test_general_websocket_disconnection(test_app):
    """
    Tests that a general WebSocket client can disconnect gracefully.
    """
    with pytest.raises(WebSocketDisconnect):
        with test_app.websocket_connect("/ws/general/test_session_disconnect") as websocket:
            # Consume initial messages
            websocket.receive_json()
            websocket.receive_json()
            websocket.close()

@pytest.mark.asyncio
async def test_unknown_session_type_websocket(test_app):
    """
    Tests that connecting with an unknown session type closes the connection.
    """
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with test_app.websocket_connect("/ws/unknown/test_session") as websocket:
            pass # Connection should be closed immediately
    assert excinfo.value.code == 1008
    assert "Unknown session type" in excinfo.value.reason
