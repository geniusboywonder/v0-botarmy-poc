import asyncio
import json
import logging
import sys
import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import uuid

# Load environment variables
from dotenv import load_dotenv
load_dotenv()  # Load .env file

# Add parent directory to path so we can import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# New architectural imports
from backend.agui.protocol import agui_handler, MessageType
from backend.artifacts import get_artifacts_structure
from backend.bridge import AGUI_Handler
from backend.connection_manager import EnhancedConnectionManager
from backend.error_handler import ErrorHandler
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.heartbeat_monitor import HeartbeatMonitor
from backend.workflow import botarmy_workflow

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- Global State (for POC) ---
# This dictionary will hold the state of active workflow runs.
# In a real multi-user app, this would be a database or Redis.
active_workflows: Dict[str, Any] = {}

# --- Application Lifespan (Startup & Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("BotArmy Backend is starting up...")

    # --- Services and Managers ---
    manager = EnhancedConnectionManager()
    heartbeat_monitor = HeartbeatMonitor(manager)
    status_broadcaster = AgentStatusBroadcaster(manager)

    # Set the status broadcaster in error handler to avoid circular imports
    ErrorHandler.set_status_broadcaster(status_broadcaster)

    # Store managers in app state
    app.state.manager = manager
    app.state.heartbeat_monitor = heartbeat_monitor
    app.state.status_broadcaster = status_broadcaster

    await heartbeat_monitor.start()

    loop = asyncio.get_running_loop()
    agui_bridge_handler = AGUI_Handler(loop=loop)
    agui_bridge_handler.set_status_broadcaster(status_broadcaster)

    # Store handler in app state so it can be removed on shutdown
    app.state.agui_bridge_handler = agui_bridge_handler

    cf_logger = logging.getLogger("prefect")
    cf_logger.addHandler(agui_bridge_handler)
    cf_logger.setLevel(logging.INFO)
    logger.info("ControlFlow to AG-UI bridge initialized.")

    yield

    logger.info("BotArmy Backend is shutting down...")
    await app.state.heartbeat_monitor.stop()

    cf_logger = logging.getLogger("prefect")
    cf_logger.removeHandler(app.state.agui_bridge_handler)

# --- FastAPI App ---
app = FastAPI(title="BotArmy Backend v3", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root(): return {"message": "BotArmy Backend v3 is running"}

ARTIFACTS_ROOT = Path("artifacts").resolve()
@app.get("/artifacts/download/{file_path:path}")
async def download_artifact(file_path: str):
    """Allows downloading of an artifact file with security checks."""
    try:
        requested_path = ARTIFACTS_ROOT.joinpath(file_path).resolve()
        if not requested_path.starts_with(ARTIFACTS_ROOT) or not requested_path.is_file():
            raise HTTPException(status_code=404, detail="File not found or access denied")
        return FileResponse(requested_path)
    except Exception as e:
        logger.error(f"Error during file download for path {file_path}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# --- WebSocket Handling ---
import controlflow as cf
from prefect.client.orchestration import get_client

async def run_and_track_workflow(project_brief: str, session_id: str, manager: EnhancedConnectionManager):
    """Runs the workflow, tracks it, and handles top-level errors."""
    global active_workflows
    flow_run_id = str(uuid.uuid4())
    active_workflows[session_id] = {"flow_run_id": flow_run_id, "status": "running"}
    logger.info(f"Workflow {flow_run_id} started for session {session_id}.")

    try:
        # Send a starting message
        response = agui_handler.create_agent_message(
            content="🚀 Starting multi-agent workflow...",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))
        
        # Run the workflow
        result = await botarmy_workflow(project_brief=project_brief, session_id=session_id)
        
        # Send completion message
        response = agui_handler.create_agent_message(
            content=f"✅ Workflow completed successfully! Results: {len(result)} agents completed their tasks.",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))
        
        logger.info(f"Workflow {flow_run_id} for session {session_id} completed successfully.")
    except Exception as e:
        error_response = agui_handler.create_agent_message(
            content=f"❌ Workflow failed: {str(e)}",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(error_response))
        logger.error(f"Workflow {flow_run_id} failed: {e}")
    finally:
        if session_id in active_workflows:
            del active_workflows[session_id]

async def handle_websocket_message(
    client_id: str,
    message: dict,
    manager: EnhancedConnectionManager,
    heartbeat_monitor: HeartbeatMonitor
):
    """Handles incoming messages from the UI."""
    logger.debug(f"Received message from client {client_id}: {message}")
    msg_type = message.get("type")

    # Handle heartbeat responses first as they are frequent and simple
    if msg_type == "heartbeat_response":
        heartbeat_monitor.handle_heartbeat_response(client_id)
        return

    session_id = message.get("session_id", "global_session")

    if msg_type == "user_command":
        command_data = message.get("data", {})
        command = command_data.get("command")
        
        if command == "ping":
            # Test backend connection
            response = agui_handler.create_agent_message(
                content="✅ Backend connection successful! Server is running on port 8000.",
                agent_name="System",
                session_id=session_id
            )
            await manager.broadcast_to_all(agui_handler.serialize_message(response))
            
        elif command == "start_project":
            if session_id in active_workflows:
                logger.warning(f"Workflow already in progress for session {session_id}.")
                response = agui_handler.create_agent_message(
                    content="⚠️ A workflow is already running. Please wait for it to complete.",
                    agent_name="System",
                    session_id=session_id
                )
                await manager.broadcast_to_all(agui_handler.serialize_message(response))
                return
            project_brief = command_data.get("brief", "No brief provided.")
            asyncio.create_task(run_and_track_workflow(project_brief, session_id, manager))

        else:
            logger.warning(f"Unknown user command: {command}")
    else:
        logger.warning(f"Unknown message type received: {msg_type}")

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    manager = websocket.app.state.manager
    heartbeat_monitor = websocket.app.state.heartbeat_monitor

    client_id = await manager.connect(websocket)
    disconnect_reason = "Unknown"
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await handle_websocket_message(client_id, message, manager, heartbeat_monitor)
    except WebSocketDisconnect as e:
        disconnect_reason = f"Code: {e.code}, Reason: {e.reason}"
        logger.info(f"Client {client_id} is disconnecting. {disconnect_reason}")
    except Exception as e:
        disconnect_reason = f"Unexpected error: {e}"
        logger.error(f"An unexpected error occurred for client {client_id}: {e}", exc_info=True)
        # Re-raising the exception so FastAPI can handle it if needed
        raise
    finally:
        await manager.disconnect(client_id, reason=disconnect_reason)

if __name__ == "__main__":
    print("🚀 Starting BotArmy Backend v3...")
    print("📍 Import paths configured")
    print("=" * 50)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
