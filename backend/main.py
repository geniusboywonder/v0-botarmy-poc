"""
Adaptive main application that works in both development and Vercel environments.
"""

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
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Runtime environment detection
from backend.runtime_env import IS_VERCEL, get_environment_info, get_prefect_client

# Core imports that work in both environments
from backend.agui.protocol import agui_handler, MessageType
from backend.artifacts import get_artifacts_structure
from backend.bridge import AGUI_Handler
from backend.connection_manager import EnhancedConnectionManager
from backend.error_handler import ErrorHandler
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.heartbeat_monitor import HeartbeatMonitor
from backend.workflow import botarmy_workflow, simple_workflow

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global state for active workflows
active_workflows: Dict[str, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with environment-aware initialization."""
    
    env_info = get_environment_info()
    logger.info(f"BotArmy Backend starting up in {'Vercel' if IS_VERCEL else 'Development'} mode")
    logger.info(f"Environment: {env_info}")

    # Core services that work in all environments
    manager = EnhancedConnectionManager()
    heartbeat_monitor = HeartbeatMonitor(manager)
    status_broadcaster = AgentStatusBroadcaster(manager)

    # Set the status broadcaster in error handler
    ErrorHandler.set_status_broadcaster(status_broadcaster)

    # Store managers in app state
    app.state.manager = manager
    app.state.heartbeat_monitor = heartbeat_monitor
    app.state.status_broadcaster = status_broadcaster

    await heartbeat_monitor.start()

    # Initialize ControlFlow bridge only in development
    if not IS_VERCEL:
        try:
            loop = asyncio.get_running_loop()
            agui_bridge_handler = AGUI_Handler(loop=loop)
            agui_bridge_handler.set_status_broadcaster(status_broadcaster)
            app.state.agui_bridge_handler = agui_bridge_handler

            # Setup ControlFlow logging bridge
            cf_logger = logging.getLogger("prefect")
            cf_logger.addHandler(agui_bridge_handler)
            cf_logger.setLevel(logging.INFO)
            logger.info("ControlFlow to AG-UI bridge initialized.")
        except Exception as e:
            logger.warning(f"Could not initialize ControlFlow bridge: {e}")
            app.state.agui_bridge_handler = None
    else:
        app.state.agui_bridge_handler = None
        logger.info("Running in Vercel mode - ControlFlow bridge disabled")

    yield

    logger.info("BotArmy Backend shutting down...")
    await app.state.heartbeat_monitor.stop()

    # Clean up ControlFlow bridge if it exists
    if hasattr(app.state, 'agui_bridge_handler') and app.state.agui_bridge_handler:
        try:
            cf_logger = logging.getLogger("prefect")
            cf_logger.removeHandler(app.state.agui_bridge_handler)
        except:
            pass

# FastAPI App
app = FastAPI(
    title="BotArmy Backend",
    version="3.0.0",
    description="Multi-agent workflow system for software development",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    """Root endpoint with environment information."""
    env_info = get_environment_info()
    return {
        "message": "BotArmy Backend is running",
        "version": "3.0.0",
        "environment": "Vercel" if IS_VERCEL else "Development",
        "features": {
            "full_workflow": not IS_VERCEL,
            "controlflow": not IS_VERCEL,
            "prefect": not IS_VERCEL,
            "websockets": True,
            "llm_integration": True
        },
        "runtime_info": env_info if not IS_VERCEL else {"is_vercel": True}
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": "vercel" if IS_VERCEL else "development"
    }

# Artifacts handling
ARTIFACTS_ROOT = Path("artifacts").resolve()

@app.get("/artifacts/download/{file_path:path}")
async def download_artifact(file_path: str):
    """Download artifact files with security checks."""
    try:
        requested_path = ARTIFACTS_ROOT.joinpath(file_path).resolve()
        if not requested_path.is_relative_to(ARTIFACTS_ROOT) or not requested_path.is_file():
            raise HTTPException(status_code=404, detail="File not found or access denied")
        return FileResponse(requested_path)
    except Exception as e:
        logger.error(f"Error downloading file {file_path}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/artifacts/structure")
async def get_artifacts_structure_endpoint():
    """Get artifacts directory structure."""
    try:
        return get_artifacts_structure()
    except Exception as e:
        logger.error(f"Error getting artifacts structure: {e}")
        raise HTTPException(status_code=500, detail="Could not read artifacts structure")

# Workflow execution with environment adaptation
async def run_and_track_workflow(project_brief: str, session_id: str, manager: EnhancedConnectionManager):
    """Run workflow with environment-appropriate implementation."""
    global active_workflows
    flow_run_id = str(uuid.uuid4())
    active_workflows[session_id] = {"flow_run_id": flow_run_id, "status": "running"}
    
    logger.info(f"Starting workflow {flow_run_id} for session {session_id} in {'Vercel' if IS_VERCEL else 'Development'} mode")

    try:
        # Send starting message
        response = agui_handler.create_agent_message(
            content=f"🚀 Starting workflow in {'Vercel' if IS_VERCEL else 'Development'} mode...",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))
        
        # Choose workflow based on environment
        if IS_VERCEL:
            # Use simplified workflow in Vercel
            result = await simple_workflow(project_brief=project_brief, session_id=session_id)
        else:
            # Use full workflow in development
            result = await botarmy_workflow(project_brief=project_brief, session_id=session_id)
        
        # Send completion message
        response = agui_handler.create_agent_message(
            content=f"✅ Workflow completed! Results: {len(result)} components generated.",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))
        
        logger.info(f"Workflow {flow_run_id} completed successfully")
        
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
    """Handle incoming WebSocket messages."""
    logger.debug(f"Message from {client_id}: {message}")
    msg_type = message.get("type")

    if msg_type == "heartbeat_response":
        heartbeat_monitor.handle_heartbeat_response(client_id)
        return

    session_id = message.get("session_id", "global_session")

    if msg_type == "user_command":
        command_data = message.get("data", {})
        command = command_data.get("command")
        
        if command == "ping":
            env_mode = "Vercel" if IS_VERCEL else "Development"
            response = agui_handler.create_agent_message(
                content=f"✅ Backend connection successful! Running in {env_mode} mode.",
                agent_name="System",
                session_id=session_id
            )
            await manager.broadcast_to_all(agui_handler.serialize_message(response))
            
        elif command == "start_project":
            if session_id in active_workflows:
                response = agui_handler.create_agent_message(
                    content="⚠️ A workflow is already running. Please wait for completion.",
                    agent_name="System",
                    session_id=session_id
                )
                await manager.broadcast_to_all(agui_handler.serialize_message(response))
                return
                
            project_brief = command_data.get("brief", "No brief provided.")
            asyncio.create_task(run_and_track_workflow(project_brief, session_id, manager))
        else:
            logger.warning(f"Unknown command: {command}")
    else:
        logger.warning(f"Unknown message type: {msg_type}")

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
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
        logger.info(f"Client {client_id} disconnected: {disconnect_reason}")
    except Exception as e:
        disconnect_reason = f"Error: {e}"
        logger.error(f"Error for client {client_id}: {e}", exc_info=True)
        raise
    finally:
        await manager.disconnect(client_id, reason=disconnect_reason)

# Additional API endpoints for status and monitoring
@app.get("/api/status")
async def get_status():
    """Get current system status."""
    return {
        "active_workflows": len(active_workflows),
        "environment": "vercel" if IS_VERCEL else "development",
        "features_available": {
            "full_workflow": not IS_VERCEL,
            "websockets": True,
            "artifacts": True
        }
    }

@app.get("/api/workflows")
async def get_active_workflows():
    """Get list of active workflows."""
    return {
        "active_workflows": active_workflows,
        "count": len(active_workflows)
    }

if __name__ == "__main__":
    print("🚀 Starting BotArmy Backend...")
    print(f"Environment: {'Vercel' if IS_VERCEL else 'Development'}")
    print("=" * 50)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
