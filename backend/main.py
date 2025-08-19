import asyncio
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import controlflow as cf
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# New architectural imports
from backend.agui.protocol import MessageType
from backend.artifacts import get_artifacts_structure
from backend.bridge import AGUI_Handler
from backend.workflow import botarmy_workflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Connection Manager ---
class ConnectionManager:
    """Manages WebSocket connections for real-time communication."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        """Broadcasts a message to all connected clients."""
        # This now expects a pre-serialized JSON string from the AGUI_Handler
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        for connection in disconnected:
            self.disconnect(connection)

manager = ConnectionManager()

# --- Application Lifespan (Startup & Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown events."""
    logger.info("BotArmy Backend is starting up...")

    # 1. Get the current asyncio event loop
    loop = asyncio.get_running_loop()

    # 2. Initialize our custom AG-UI bridge handler
    agui_bridge_handler = AGUI_Handler(connection_manager=manager, loop=loop)

    # 3. Get the root logger for Prefect/ControlFlow and add our handler
    cf_logger = logging.getLogger("prefect")
    cf_logger.addHandler(agui_bridge_handler)
    cf_logger.setLevel(logging.INFO)
    
    logger.info("ControlFlow to AG-UI bridge initialized.")
    
    yield
    
    logger.info("BotArmy Backend is shutting down...")
    cf_logger.removeHandler(agui_bridge_handler)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="BotArmy Backend",
    description="Multi-agent AI orchestration system backend using ControlFlow",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HTTP API Endpoints ---
@app.get("/")
async def root():
    return {"message": "BotArmy Backend v2 is running"}

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
async def handle_websocket_message(websocket: WebSocket, message: dict):
    """Handles incoming messages from the UI."""
    msg_type = message.get("type")

    if msg_type == MessageType.USER_COMMAND.value:
        command_data = message.get("data", {})
        command = command_data.get("command")

        if command == "start_project":
            project_brief = command_data.get("brief", "No brief provided.")
            logger.info(f"Received start_project command. Brief: {project_brief}")
            # Run the main workflow as a background task
            asyncio.create_task(cf.run(botarmy_workflow, parameters={"project_brief": project_brief}))
        else:
            logger.warning(f"Unknown user command: {command}")

    elif msg_type == "artifacts_get_all":
        # This is now a legacy way of getting artifacts.
        # It will be replaced by events from the workflow.
        # For now, we keep it for the existing UI.
        artifacts_data = get_artifacts_structure()
        response = {
            "type": "artifacts_update",
            "payload": artifacts_data,
            "timestamp": datetime.now().isoformat(),
        }
        await websocket.send_text(json.dumps(response))

    else:
        logger.warning(f"Unknown message type received: {msg_type}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for all real-time communication."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await handle_websocket_message(websocket, message)
    except WebSocketDisconnect:
        logger.info("Client disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)

# --- Main Execution ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
