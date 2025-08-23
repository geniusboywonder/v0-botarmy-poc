import pytest
import asyncio
import websockets
import json
import subprocess
import time
import os

# Add project root to path to allow imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test mode for agents
os.environ["AGENT_TEST_MODE"] = "true"

@pytest.fixture(scope="module")
def server():
    """Starts and stops the FastAPI server for the test module."""
    process = subprocess.Popen(["python", "backend/main.py"])
    time.sleep(5) # Give server time to start
    yield
    process.terminate()
    process.wait()

@pytest.mark.asyncio
async def test_websocket_communication_on_start_project(server):
    """
    Tests the WebSocket communication during a `start_project` command.
    """
    uri = "ws://localhost:8000/api/ws"
    async with websockets.connect(uri) as websocket:
        # Send start_project command
        await websocket.send(json.dumps({
            "type": "user_command",
            "data": {
                "command": "start_project",
                "brief": "Test project brief"
            },
            "session_id": "integration_test"
        }))

        received_messages = []
        try:
            async with asyncio.timeout(30):
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    received_messages.append(data)
                    # Exit condition: workflow is complete when Deployer is done
                    if data.get("type") == "agent_status" and \
                       data.get("data", {}).get("agent_name") == "Deployer" and \
                       data.get("data", {}).get("status") == "completed":
                        break
        except asyncio.TimeoutError:
            pytest.fail("Test timed out waiting for workflow to complete.")

        # Assertions
        assert len(received_messages) > 0

        # Check for workflow progress messages
        workflow_progress_messages = [msg for msg in received_messages if msg.get("type") == "workflow_progress"]
        assert len(workflow_progress_messages) > 0

        # Check for agent status messages
        agent_status_messages = [msg for msg in received_messages if msg.get("type") == "agent_status"]
        assert len(agent_status_messages) > 0

        # Check for messages from all agents
        agents = ["Analyst", "Architect", "Developer", "Tester", "Deployer"]
        for agent_name in agents:
            agent_msgs = [msg for msg in agent_status_messages if msg.get("data", {}).get("agent_name") == agent_name]
            assert len(agent_msgs) > 0
            # Check for a 'completed' status for each agent
            assert any(msg.get("data", {}).get("status") == "completed" for msg in agent_msgs)
