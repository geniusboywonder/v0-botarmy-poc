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

# New architectural imports
from backend.agui.protocol import agui_handler, MessageType
from backend.artifacts import get_artifacts_structure
from backend.bridge import AGUI_Handler
from backend.workflow import botarmy_workflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Global State (for POC) ---
# This dictionary will hold the state of active workflow runs.
# In a real multi-user app, this would be a database or Redis.
active_workflows: Dict[str, Any] = {}

# --- Connection Manager ---
class ConnectionManager:
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
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# --- Application Lifespan (Startup & Shutdown) ---
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

# --- FastAPI App ---
app = FastAPI(title="BotArmy Backend v2", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root(): return {"message": "BotArmy Backend v2 is running"}

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
    """Handles incoming messages from the UI."""
    msg_type = message.get("type")
    session_id = message.get("session_id", "global_session")

    if msg_type == "user_command":
        command_data = message.get("data", {})
        command = command_data.get("command")
        
        if command == "ping":
            # Test backend connection
            response = agui_handler.create_agent_message(
                content="Backend connection successful! Server is running on port 8000.",
                agent_name="System",
                session_id=session_id
            )
            await manager.broadcast(agui_handler.serialize_message(response))
            
        elif command == "test_openai":
            # Test OpenAI API connection
            try:
                import openai
                import os
                
                # Check if API key is set
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    response = agui_handler.create_error_message(
                        error="OpenAI API key not found. Set OPENAI_API_KEY environment variable.",
                        session_id=session_id
                    )
                else:
                    # Test API call
                    client = openai.OpenAI(api_key=api_key)
                    test_response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "Say 'OpenAI connection test successful'"}],
                        max_tokens=20
                    )
                    response = agui_handler.create_agent_message(
                        content=f"✅ OpenAI API test successful! Response: {test_response.choices[0].message.content}",
                        agent_name="System",
                        session_id=session_id
                    )
            except ImportError:
                response = agui_handler.create_error_message(
                    error="OpenAI package not installed. Run: pip install openai",
                    session_id=session_id
                )
            except Exception as e:
                response = agui_handler.create_error_message(
                    error=f"OpenAI API test failed: {str(e)}",
                    session_id=session_id
                )
            
            await manager.broadcast(agui_handler.serialize_message(response))
        
        elif command == "start_project":
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
                # This is a HYPOTHETICAL function call based on Prefect patterns
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
