"""
Adaptive main application that works in both development and Replit environments.
FIXED: OpenAI provider argument error and enhanced WebSocket stability
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
from backend.runtime_env import IS_REPLIT, get_environment_info, get_prefect_client

# Core imports that work in both environments
from backend.agui.protocol import agui_handler, MessageType
from backend.artifacts import get_artifacts_structure
from backend.bridge import AGUI_Handler
from backend.connection_manager import EnhancedConnectionManager
from backend.error_handler import ErrorHandler
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.heartbeat_monitor import HeartbeatMonitor
from backend.workflow import botarmy_workflow, simple_workflow

# Import rate limiter and enhanced LLM service
from backend.rate_limiter import rate_limiter
from backend.services.llm_service import get_llm_service

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
    logger.info(f"BotArmy Backend starting up in {'Replit' if IS_REPLIT else 'Development'} mode")
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

    # Initialize ControlFlow bridge - now available in Replit
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

    # Initialize LLM service
    try:
        llm_service = get_llm_service()
        app.state.llm_service = llm_service
        logger.info("LLM service initialized with rate limiting")
    except Exception as e:
        logger.warning(f"Could not initialize LLM service: {e}")
        app.state.llm_service = None

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
    description="Multi-agent workflow system with rate limiting and HITL",
    lifespan=lifespan
)

# Enhanced CORS configuration for better WebSocket stability
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://localhost:3000",
]

if IS_REPLIT:
    # Add Replit-specific origins
    allowed_origins.extend([
        "https://*.replit.app",
        "https://*.replit.dev",
        "https://*.replit.co"
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,  # Set to False for better WebSocket compatibility
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with environment information."""
    env_info = get_environment_info()
    return {
        "message": "BotArmy Backend is running",
        "version": "3.0.0",
        "environment": "Replit" if IS_REPLIT else "Development",
        "features": {
            "full_workflow": True,  # Now available in Replit
            "controlflow": True,
            "prefect": True,
            "websockets": True,
            "llm_integration": True,
            "rate_limiting": True,   # New feature
            "multi_llm": True,       # New feature
            "hitl": True             # New feature
        },
        "runtime_info": env_info
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": "replit" if IS_REPLIT else "development",
        "port": os.getenv("PORT", "8000")
    }

# Workflow execution
async def run_and_track_workflow(project_brief: str, session_id: str, manager: EnhancedConnectionManager):
    """Run workflow with full functionality in Replit."""
    global active_workflows
    flow_run_id = str(uuid.uuid4())
    active_workflows[session_id] = {"flow_run_id": flow_run_id, "status": "running"}
    
    logger.info(f"Starting workflow {flow_run_id} for session {session_id} in {'Replit' if IS_REPLIT else 'Development'} mode")

    try:
        # Send starting message
        response = agui_handler.create_agent_message(
            content=f"🚀 Starting workflow in {'Replit' if IS_REPLIT else 'Development'} mode...",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))
        
        # Use full workflow - now available in Replit
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

async def test_openai_connection(session_id: str, manager: EnhancedConnectionManager, test_message: str = None):
    """Test OpenAI connection and return result via WebSocket."""
    try:
        # Send starting message
        response = agui_handler.create_agent_message(
            content="🧠 Testing OpenAI connection...",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))
        
        # Get LLM service
        llm_service = get_llm_service()
        
        # Test message
        if not test_message:
            test_message = "Hello! This is a test message to verify OpenAI integration is working properly. Please respond with a brief confirmation."
        
        # FIXED: Use correct method signature
        result = await llm_service.generate_response(
            prompt=test_message,
            agent_name="OpenAI Test",
            preferred_provider="openai"  # Fixed: Use correct parameter name
        )
        
        # Send success message with response
        success_response = agui_handler.create_agent_message(
            content=f"✅ OpenAI test successful!\n\n📝 Test Message: {test_message}\n\n🤖 OpenAI Response: {result}",
            agent_name="OpenAI Test",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(success_response))
        
        logger.info(f"OpenAI test successful for session {session_id}")
        
    except Exception as e:
        # Send error message
        error_response = agui_handler.create_agent_message(
            content=f"❌ OpenAI test failed: {str(e)}\n\nPlease check your OPENAI_API_KEY environment variable and ensure you have sufficient credits.",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(error_response))
        logger.error(f"OpenAI test failed for session {session_id}: {e}")

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
            env_mode = "Replit" if IS_REPLIT else "Development"
            response = agui_handler.create_agent_message(
                content=f"✅ Backend connection successful! Running in {env_mode} mode.",
                agent_name="System",
                session_id=session_id
            )
            await manager.broadcast_to_all(agui_handler.serialize_message(response))
            
        elif command == "test_openai":
            test_message = command_data.get("message")
            asyncio.create_task(test_openai_connection(session_id, manager, test_message))
            
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
    """Enhanced WebSocket endpoint for more stable connections."""
    manager = websocket.app.state.manager
    heartbeat_monitor = websocket.app.state.heartbeat_monitor

    client_id = await manager.connect(websocket)
    disconnect_reason = "Unknown"
    
    try:
        # Send welcome message
        welcome_msg = agui_handler.create_agent_message(
            content="🔗 WebSocket connection established successfully!",
            agent_name="System",
            session_id="global_session"
        )
        await websocket.send_text(agui_handler.serialize_message(welcome_msg))
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("type") == "batch":
                for msg in message.get("messages", []):
                    await handle_websocket_message(client_id, msg, manager, heartbeat_monitor)
            else:
                await handle_websocket_message(client_id, message, manager, heartbeat_monitor)
                
    except WebSocketDisconnect as e:
        disconnect_reason = f"Code: {e.code}, Reason: {e.reason if e.reason else 'Normal closure'}"
        logger.info(f"Client {client_id} disconnected: {disconnect_reason}")
    except Exception as e:
        disconnect_reason = f"Error: {e}"
        logger.error(f"Error for client {client_id}: {e}", exc_info=True)
    finally:
        await manager.disconnect(client_id, reason=disconnect_reason)

# Additional API endpoints for status and monitoring
@app.get("/api/status")
async def get_status():
    """Get current system status."""
    return {
        "active_workflows": len(active_workflows),
        "environment": "replit" if IS_REPLIT else "development",
        "features_available": {
            "full_workflow": True,
            "websockets": True,
            "artifacts": True,
            "controlflow": True,
            "rate_limiting": True,
            "multi_llm": True,
            "hitl": True
        }
    }

if __name__ == "__main__":
    print("🚀 Starting BotArmy Backend...")
    print(f"Environment: {'Replit' if IS_REPLIT else 'Development'}")
    print("=" * 50)
    
    # Use PORT environment variable for Replit
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
