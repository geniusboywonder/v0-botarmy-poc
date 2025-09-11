"""
Main application file for the BotArmy backend.
This version is refactored to use a simplified WebSocket architecture and a centralized StateService.
"""

import asyncio
import json
import logging
import sys
import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
import uuid

from dotenv import load_dotenv

# Load environment variables as early as possible
load_dotenv()

# --- Debugging .env loading ---
print(f"[DEBUG .env] LOG_LEVEL: {os.getenv('LOG_LEVEL')}")
print(f"[DEBUG .env] ENABLE_HITL: {os.getenv('ENABLE_HITL')}")
print(f"[DEBUG .env] AUTO_ACTION: {os.getenv('AUTO_ACTION')}")
print(f"[DEBUG .env] OPENAI_API_KEY (first 5 chars): {os.getenv('OPENAI_API_KEY', '')[:5]}...")
print(f"[DEBUG .env] GOOGLE_API_KEY (first 5 chars): {os.getenv('GOOGLE_API_KEY', '')[:5]}...")
print(f"[DEBUG .env] GEMINI_KEY_KEY (first 5 chars): {os.getenv('GEMINI_KEY_KEY', '')[:5]}...")
print(f"[DEBUG .env] TEST_MODE: {os.getenv('TEST_MODE')}")
print(f"[DEBUG .env] AGENT_TEST_MODE: {os.getenv('AGENT_TEST_MODE')}")
print(f"[DEBUG .env] ROLE_TEST_MODE: {os.getenv('ROLE_TEST_MODE')}")
# --- End Debugging .env loading ---

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Project imports
from backend.runtime_env import IS_REPLIT
from backend.simple_connection_manager import SimpleConnectionManager
from backend.heartbeat_service import HeartbeatService
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.state_service import get_state_service, StateService
from backend.workflow.simple_orchestrator import create_simple_workflow
from backend.services.llm_service import get_llm_service, LLMService

# Initial setup
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ensure logs are always printed to console
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Ensure logs are always printed to console
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with simplified, centralized services."""
    logger.info(f"BotArmy Backend starting up in {'Replit' if IS_REPLIT else 'Development'} mode")
    logger.info(f"[DEBUG] ENABLE_HITL: {os.getenv('ENABLE_HITL')}")
    logger.info(f"[DEBUG] AUTO_ACTION: {os.getenv('AUTO_ACTION')}")

    # Initialize services
    manager = SimpleConnectionManager()
    heartbeat_service = HeartbeatService(manager)
    status_broadcaster = AgentStatusBroadcaster(manager)
    state_service = get_state_service()
    llm_service = get_llm_service()

    # Store services in app state
    app.state.manager = manager
    app.state.heartbeat_service = heartbeat_service
    app.state.status_broadcaster = status_broadcaster
    app.state.state_service = state_service
    app.state.llm_service = llm_service

    await heartbeat_service.start()
    logger.info("All services initialized.")

    yield

    logger.info("BotArmy Backend shutting down...")
    await app.state.heartbeat_service.stop()

# FastAPI App
app = FastAPI(
    title="BotArmy Backend",
    version="3.2.0",
    description="Refactored multi-agent workflow system with centralized state management.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Simplified for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Helper Functions ---

async def run_workflow(
    project_brief: str, 
    session_id: str, 
    status_broadcaster: AgentStatusBroadcaster, 
    state_service: StateService,
    llm_service: LLMService
):
    """Runs the simple SDLC workflow and manages state."""
    logger.info(f"[DEBUG] run_workflow called for session {session_id} with brief: {project_brief[:50]}...")
    if state_service.get_workflow_status(session_id):
        await status_broadcaster.broadcast_agent_error("System", "A workflow is already in progress.", session_id)
        logger.info(f"[DEBUG] Workflow already in progress for session {session_id}. Aborting new workflow.")
        return

    state_service.update_workflow_status(session_id, "running")
    logger.info(f"Starting SDLC workflow for session {session_id}")

    try:
        await status_broadcaster.broadcast_agent_status("System", "starting", f"Starting SDLC workflow for: {project_brief}", session_id)
        
        simple_workflow = create_simple_workflow(llm_service, status_broadcaster)
        result = await simple_workflow.execute_workflow(project_brief, session_id)

        completion_content = f"🎉 Workflow completed successfully!\n\n## 📋 PROJECT DELIVERABLES\n{result}"
        await status_broadcaster.broadcast_agent_response("System", completion_content, session_id)
        state_service.update_workflow_status(session_id, "completed")
        logger.info(f"Workflow for session {session_id} completed successfully")

    except Exception as e:
        error_message = f"❌ Workflow failed: {str(e)}"
        await status_broadcaster.broadcast_agent_error("System", error_message, session_id)
        state_service.update_workflow_status(session_id, "failed")
        logger.error(f"Workflow for session {session_id} failed: {e}", exc_info=True)
    finally:
        # Optionally clear workflow state upon completion
        pass

async def handle_websocket_message(client_id: str, message: dict, app_state: Any):
    """Handles incoming WebSocket messages."""
    msg_type = message.get("type")
    manager = app_state.manager
    status_broadcaster = app_state.status_broadcaster
    llm_service = app_state.llm_service

    logger.info(f"[DEBUG] Received message from {client_id}: {message}")

    # Send acknowledgment
    ack_message = {
        "type": "system",
        "content": f"Backend received your message of type: {msg_type}"
    }
    await manager.send_to_client(client_id, json.dumps(ack_message))

    if msg_type == "start_project":
        project_brief = message.get("data", {}).get("brief")
        if project_brief:
            asyncio.create_task(
                run_workflow(
                    project_brief, 
                    client_id, 
                    app_state.status_broadcaster, 
                    app_state.state_service,
                    app_state.llm_service
                )
            )
        else:
            await app_state.status_broadcaster.broadcast_agent_error("System", "Project brief is missing.", client_id)
    
    elif msg_type == "pong":
        logger.debug(f"Pong received from {client_id}")

    else:
        logger.warning(f"Unknown message type from {client_id}: {msg_type}")

# --- API Endpoints ---

@app.get("/")
async def root():
    return {"message": "BotArmy Backend is running", "version": app.version}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """The single WebSocket endpoint for all real-time communication."""
    manager = websocket.app.state.manager
    client_id = await manager.connect(websocket)
    
    try:
        while True:
            logger.info(f"[DEBUG] Backend entering WebSocket receive loop for {client_id}.")
            data = await websocket.receive_text()
            logger.info(f"[DEBUG] Raw data received from {client_id}: {data}")
            try:
                message = json.loads(data)
                await handle_websocket_message(client_id, message, websocket.app.state)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON from {client_id}")
            except Exception as e:
                logger.error(f"Error handling message from {client_id}: {e}", exc_info=True)

    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected.")
    finally:
        await manager.disconnect(client_id)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    reload = not IS_REPLIT
    
    print("🚀 Starting BotArmy Backend (Refactored)...")
    print(f"Environment: {'Replit' if IS_REPLIT else 'Development'}")
    print(f"URL: http://localhost:{port}")
    print("=" * 50)
    
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=reload)
