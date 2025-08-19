import asyncio
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import uuid

import controlflow as cf
from prefect.client.orchestration import get_client
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Import AG-UI handler for creating messages
from backend.agui.protocol import agui_handler, MessageType
from backend.artifacts import get_artifacts_structure
from backend.bridge import AGUI_Handler
from backend.workflow import botarmy_workflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

active_workflows: Dict[str, Any] = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("BotArmy Backend is starting up...")
    loop = asyncio.get_running_loop()
    agui_bridge_handler = AGUI_Handler(connection_manager=manager, loop=loop)
    cf_logger = logging.getLogger("prefect")
    cf_logger.addHandler(agui_bridge_handler)
    cf_logger.setLevel(logging.INFO)
    logger.info("ControlFlow to AG-UI bridge initialized.")
    yield
    logger.info("BotArmy Backend is shutting down...")
    cf_logger.removeHandler(agui_bridge_handler)

app = FastAPI(title="BotArmy Backend v2", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root(): return {"message": "BotArmy Backend v2 is running"}

async def run_and_track_workflow(project_brief: str, session_id: str):
    """Runs the workflow, tracks it, and handles top-level errors."""
    global active_workflows
    flow_run_id = str(uuid.uuid4())
    active_workflows[session_id] = {"flow_run_id": flow_run_id, "status": "running"}
    logger.info(f"Workflow {flow_run_id} started for session {session_id}.")

    try:
        await cf.run(botarmy_workflow, parameters={"project_brief": project_brief})
        logger.info(f"Workflow {flow_run_id} for session {session_id} completed successfully.")
    except Exception as e:
        logger.error(f"Workflow {flow_run_id} for session {session_id} failed: {e}", exc_info=True)
        # Create a system error message and broadcast it
        error_message = agui_handler.create_error_message(
            error=f"The workflow failed with an unexpected error: {e}",
            session_id=session_id
        )
        serialized_message = agui_handler.serialize_message(error_message)
        await manager.broadcast(serialized_message)
    finally:
        if session_id in active_workflows:
            del active_workflows[session_id]

async def handle_websocket_message(websocket: WebSocket, message: dict):
    msg_type = message.get("type")
    session_id = message.get("session_id", "global_session")

    if msg_type == "user_command":
        command_data = message.get("data", {})
        command = command_data.get("command")
        
        if command == "start_project":
            if session_id in active_workflows:
                logger.warning(f"Workflow already in progress for session {session_id}.")
                return
            project_brief = command_data.get("brief", "No brief provided.")
            asyncio.create_task(run_and_track_workflow(project_brief, session_id))
        
        elif command in ["pause_workflow", "resume_workflow"]:
            workflow_data = active_workflows.get(session_id)
            if not workflow_data:
                logger.warning(f"No active workflow found for session {session_id} to {command}.")
                return

            flow_run_id = workflow_data["flow_run_id"]
            is_pause = command == "pause_workflow"
            new_state = "PAUSED" if is_pause else "RESUMING"
            log_action = "pause" if is_pause else "resume"

            logger.info(f"Attempting to {log_action} workflow run: {flow_run_id}")
            try:
                async with get_client() as client:
                    await client.set_flow_run_state(
                        flow_run_id=flow_run_id,
                        state={"type": new_state, "name": f"Paused by user via UI"},
                    )
                logger.info(f"{log_action.capitalize()} command sent successfully.")
                workflow_data["status"] = "paused" if is_pause else "running"
            except Exception as e:
                logger.error(f"Failed to send {log_action} command: {e}")
        else:
            logger.warning(f"Unknown user command: {command}")
    else:
        logger.warning(f"Unknown message type received: {msg_type}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await handle_websocket_message(websocket, message)
    except WebSocketDisconnect:
        logger.info("Client disconnected.")
    finally:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)