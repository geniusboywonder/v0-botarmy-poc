"""
Adaptive main application that works in both development and Replit environments.
FIXED: OpenAI provider argument error and enhanced WebSocket stability
"""

import asyncio
import json
import logging
import sys
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
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
# Import from legacy_workflow.py file (renamed to avoid namespace collision)
from backend.legacy_workflow import simple_workflow
from backend.serialization_safe_wrapper import make_serialization_safe

# Import from workflow package
from backend.workflow.generic_orchestrator import generic_workflow
from backend.workflow.interactive_orchestrator import InteractiveWorkflowOrchestrator
from backend.workflow.simple_orchestrator import create_simple_workflow

# Import rate limiter and enhanced LLM service
from backend.rate_limiter import rate_limiter
from backend.services.llm_service import get_llm_service, LLMService
from backend.services.message_router import MessageRouter
from backend.services.general_chat_service import GeneralChatService
from backend.services.role_enforcer import RoleEnforcer
from backend.services.upload_rate_limiter import get_upload_rate_limiter, RateLimitType
from backend.services.performance_monitor import PerformanceMonitor

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global state for active workflows
active_workflows: Dict[str, Any] = {}
agent_pause_states: Dict[str, bool] = {}
artifact_preferences: Dict[str, bool] = {}
chat_sessions: Dict[str, Dict[str, Any]] = {}

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

    # Initialize new services
    app.state.message_router = MessageRouter()
    app.state.general_chat_service = GeneralChatService()
    app.state.role_enforcer = RoleEnforcer()
    app.state.upload_rate_limiter = get_upload_rate_limiter()
    
    # Initialize performance monitor
    app.state.performance_monitor = PerformanceMonitor()
    app.state.performance_monitor.set_connection_manager(manager)
    app.state.performance_monitor.set_status_broadcaster(status_broadcaster)
    await app.state.performance_monitor.start_monitoring()
    
    logger.info("All services initialized including performance monitoring")

    yield

    logger.info("BotArmy Backend shutting down...")
    await app.state.heartbeat_monitor.stop()
    
    # Stop performance monitoring
    if hasattr(app.state, 'performance_monitor'):
        await app.state.performance_monitor.stop_monitoring()

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
async def run_and_track_workflow(project_brief: str, session_id: str, manager: EnhancedConnectionManager, status_broadcaster: AgentStatusBroadcaster, role_enforcer: RoleEnforcer, llm_service: LLMService, config_name: str = "sdlc"):
    """Run a generic workflow based on a configuration."""
    global active_workflows
    flow_run_id = str(uuid.uuid4())
    active_workflows[session_id] = {
        "flow_run_id": flow_run_id,
        "status": "running",
        "process_config": config_name
    }

    logger.info(f"Starting generic workflow '{config_name}' ({flow_run_id}) for session {session_id}")

    try:
        # Send starting message
        response = agui_handler.create_agent_message(
            content=f"🚀 Starting generic workflow '{config_name}'...",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))
        # Choose workflow based on config_name - integrate both approaches
        if config_name == "sdlc":
            # Use simple orchestrator that actually works
            logger.info("Using Simple Orchestrator for SDLC workflow")
            simple_workflow = create_simple_workflow(llm_service, status_broadcaster)
            result = await simple_workflow.execute_workflow(project_brief, session_id)
        else:
            # Use the generic workflow for other process configurations
            result = await generic_workflow(
                config_name=config_name,
                initial_input=project_brief,
                session_id=session_id,
                status_broadcaster=status_broadcaster
            )

        # Send completion message with project artifacts
        completion_content = f"🎉 Workflow '{config_name}' completed successfully!"
        
        # Display project artifacts/results to the user
        if result and isinstance(result, dict):
            if result.get("artifacts"):
                completion_content += f"\n\nProduced {len(result['artifacts'])} artifacts."
            
            # Show actual agent results if available
            agent_results = []
            for agent_name in ["Analyst", "Architect", "Developer", "Tester", "Deployer"]:
                if agent_name in result and result[agent_name]:
                    agent_results.append(f"\n\n## {agent_name} Output:\n{result[agent_name]}")
            
            if agent_results:
                completion_content += "\n\n" + "="*50 + "\n## 📋 PROJECT DELIVERABLES\n" + "="*50
                completion_content += "".join(agent_results)
            elif result:
                # Fallback: show the raw result if no individual agent results
                completion_content += f"\n\n## 📋 PROJECT RESULT:\n```\n{str(result)[:2000]}...\n```" if len(str(result)) > 2000 else f"\n\n## 📋 PROJECT RESULT:\n{result}"
        
        response = agui_handler.create_agent_message(
            content=completion_content,
            agent_name="System", 
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))
        logger.info(f"Workflow {flow_run_id} completed successfully")

    except Exception as e:
        error_response = agui_handler.create_agent_message(
            content=f"❌ Workflow '{config_name}' failed: {str(e)}",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(error_response))
        logger.error(f"Workflow {flow_run_id} failed: {e}", exc_info=True)
        
        # Update workflow status to failed
        if session_id in active_workflows:
            active_workflows[session_id]["status"] = "failed"
            active_workflows[session_id]["error"] = str(e)
    finally:
        # Clean up workflow state after completion or failure
        if session_id in active_workflows:
            final_status = active_workflows[session_id].get("status", "unknown")
            logger.info(f"Workflow {flow_run_id} finished with status: {final_status}")
            del active_workflows[session_id]
        
        # Reset agent pause states for this session
        for agent_name in ["Analyst", "Architect", "Developer", "Tester", "Deployer"]:
            if agent_name in agent_pause_states:
                agent_pause_states[agent_name] = False

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

async def handle_chat_message(session_id: str, manager: EnhancedConnectionManager, chat_text: str, app_state: Any):
    """Handles a chat message from the user, routing it based on the current mode."""
    logger.info(f"HANDLE_CHAT_MESSAGE called: session={session_id}, text='{chat_text}'")
    global chat_sessions

    if session_id not in chat_sessions:
        chat_sessions[session_id] = {"mode": "general", "project_context": None}
        logger.info(f"Created new chat session for {session_id}")

    session = chat_sessions[session_id]
    current_mode = session["mode"]
    message_data = {"text": chat_text}
    
    logger.info(f"Current mode: {current_mode}, routing message: {message_data}")
    router_action = app_state.message_router.route_message(message_data, current_mode)
    logger.info(f"Router action determined: {router_action}")

    if router_action == "switch_to_project":
        if session_id in active_workflows:
            response = agui_handler.create_agent_message(
                content="⚠️ A workflow is already running. Please wait for completion.",
                agent_name="System",
                session_id=session_id
            )
            await manager.broadcast_to_all(agui_handler.serialize_message(response))
            return

        session["mode"] = "project"
        project_description = app_state.message_router.get_project_description(chat_text)
        session["project_context"] = {"description": project_description}
        response_msg = agui_handler.create_agent_message(
            content=f"Switched to project mode. Starting project: {project_description}",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response_msg))
        # Trigger the project workflow
        asyncio.create_task(run_and_track_workflow(project_description, session_id, manager, app_state.status_broadcaster, app_state.role_enforcer, app.state.llm_service))

    elif router_action == "switch_to_general":
        session["mode"] = "general"
        response_msg = agui_handler.create_agent_message(
            content="Switched to general chat mode.",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response_msg))

    elif router_action == "project_workflow":
        # In project mode, messages should trigger the workflow
        if session_id in active_workflows:
            response_msg = agui_handler.create_agent_message(
                content="⚠️ A workflow is already running. Please wait for completion.",
                agent_name="System",
                session_id=session_id
            )
            await manager.broadcast_to_all(agui_handler.serialize_message(response_msg))
        else:
            # Trigger the project workflow with the new message as project description
            logger.info(f"Triggering workflow for project message: {chat_text}")
            asyncio.create_task(run_and_track_workflow(chat_text, session_id, manager, app_state.status_broadcaster, app_state.role_enforcer, app.state.llm_service))

    elif router_action == "general_chat":
        try:
            response_text = await app_state.general_chat_service.handle_message(chat_text)
            response_msg = agui_handler.create_agent_message(
                content=response_text,
                agent_name="BotArmy Assistant",
                session_id=session_id
            )
            await manager.broadcast_to_all(agui_handler.serialize_message(response_msg))
        except Exception as e:
            logger.error(f"Error in general chat: {e}")
            error_response = agui_handler.create_agent_message(
                content=f"Sorry, I encountered an error in general chat: {e}",
                agent_name="System",
                session_id=session_id
            )
            await manager.broadcast_to_all(agui_handler.serialize_message(error_response))

async def handle_websocket_message(
    client_id: str,
    message: dict,
    manager: EnhancedConnectionManager,
    heartbeat_monitor: HeartbeatMonitor,
    status_broadcaster: AgentStatusBroadcaster,
    app_state: Any
):
    """Handle incoming WebSocket messages."""
    logger.info(f"WEBSOCKET MESSAGE from {client_id}: {message}")
    msg_type = message.get("type")

    if msg_type == "heartbeat_response":
        heartbeat_monitor.handle_heartbeat_response(client_id)
        return

    elif msg_type == "ping":
        await manager.send_to_client(
            client_id,
            json.dumps({"type": "pong", "timestamp": datetime.now().isoformat()})
        )
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

        elif command == "chat_message":
            chat_text = command_data.get("text", "")
            logger.info(f"CHAT MESSAGE received: '{chat_text}' for session {session_id}")
            if chat_text:
                logger.info(f"Creating task to handle chat message: '{chat_text}'")
                asyncio.create_task(handle_chat_message(session_id, manager, chat_text, app_state))
            else:
                logger.warning(f"Empty chat text received for session {session_id}")

        elif command == "stop_all_agents":
            # Stop all active workflows and agents
            global active_workflows, agent_pause_states
            if session_id in active_workflows:
                active_workflows[session_id]["status"] = "stopped"
                # Pause all agents
                for agent_name in ["Analyst", "Architect", "Developer", "Tester", "Deployer"]:
                    agent_pause_states[agent_name] = True
                
                response = agui_handler.create_agent_message(
                    content="🛑 All agent activities have been stopped. Agents are now paused.",
                    agent_name="System",
                    session_id=session_id
                )
                await manager.broadcast_to_all(agui_handler.serialize_message(response))
                logger.info(f"All agents stopped by user for session {session_id}")
            else:
                response = agui_handler.create_agent_message(
                    content="No active workflows to stop.",
                    agent_name="System", 
                    session_id=session_id
                )
                await manager.broadcast_to_all(agui_handler.serialize_message(response))

        elif command == "start_project":
            project_brief = command_data.get("brief", "No brief provided.")
            chat_text = f"start project {project_brief}"
            asyncio.create_task(handle_chat_message(session_id, manager, chat_text, app_state))
        elif command == "set_artifact_preference":
            artifact_id = command_data.get("artifact_id")
            is_enabled = command_data.get("is_enabled")
            if artifact_id is not None and is_enabled is not None:
                artifact_preferences[artifact_id] = is_enabled
                logger.info(f"Artifact preference set for {artifact_id}: {is_enabled}")
        else:
            logger.warning(f"Unknown command: {command}")

    elif msg_type == "agent_command":
        command_data = message.get("data", {})
        agent_name = command_data.get("agent_name")
        command = command_data.get("command")
        if agent_name and command:
            if command == "pause_agent":
                agent_pause_states[agent_name] = True
                await status_broadcaster.broadcast_agent_status(
                    agent_name=agent_name,
                    status="paused",
                    task="Paused by user.",
                    session_id=session_id
                )
                logger.info(f"Agent {agent_name} paused by user.")
            elif command == "resume_agent":
                agent_pause_states[agent_name] = False
                await status_broadcaster.broadcast_agent_status(
                    agent_name=agent_name,
                    status="working",
                    task="Resumed by user.",
                    session_id=session_id
                )
                logger.info(f"Agent {agent_name} resumed by user.")
    
    elif msg_type == "artifacts_get_all":
        # Handle request for all artifacts
        try:
            # Get all available artifacts (this could be expanded to read from file system)
            artifacts_response = {
                "type": "artifacts_response",
                "data": {
                    "artifacts": [],  # Empty for now, can be populated with actual artifacts
                    "total_count": 0
                }
            }
            await manager.send_to_client(session_id, artifacts_response)
            logger.info("Sent artifacts list to client")
        except Exception as e:
            logger.error(f"Error handling artifacts_get_all: {e}")
    
    else:
        # Reduce log level to debug to avoid spam
        logger.debug(f"Unknown message type: {msg_type}")

async def run_and_track_interactive_workflow(project_brief: str, session_id: str, status_broadcaster: AgentStatusBroadcaster):
    """Run an interactive workflow."""
    global active_workflows
    flow_run_id = str(uuid.uuid4())
    active_workflows[session_id] = {
        "flow_run_id": flow_run_id,
        "status": "running", 
        "process_config": "interactive_sdlc",
        "orchestrator": None
    }

    logger.info(f"Starting interactive workflow 'interactive_sdlc' ({flow_run_id}) for session {session_id}")

    try:
        orchestrator = InteractiveWorkflowOrchestrator(status_broadcaster)
        active_workflows[session_id]["orchestrator"] = orchestrator  # Store reference for answer submission
        
        await orchestrator.execute(
            config_name="interactive_sdlc",
            project_brief=project_brief,
            session_id=session_id,
        )
        logger.info(f"Interactive workflow {flow_run_id} completed successfully")
    except Exception as e:
        logger.error(f"Interactive workflow {flow_run_id} failed: {e}", exc_info=True)
        if session_id in active_workflows:
            active_workflows[session_id]["status"] = "failed"
            active_workflows[session_id]["error"] = str(e)
    finally:
        if session_id in active_workflows:
            del active_workflows[session_id]


@app.websocket("/ws/interactive/{session_id}")
async def interactive_websocket_endpoint(websocket: WebSocket, session_id: str):
    """Endpoint for interactive workflows."""
    manager = websocket.app.state.manager
    status_broadcaster = websocket.app.state.status_broadcaster
    await manager.connect(websocket) # Simple connect, no session mapping yet

    try:
        # The first message from the client should be the project brief.
        initial_data = await websocket.receive_text()
        message = json.loads(initial_data)
        if message.get("type") == "start_project":
            project_brief = message.get("data", {}).get("brief", "No brief provided.")

            # Use the session_id from the URL
            asyncio.create_task(run_and_track_interactive_workflow(
                project_brief, session_id, status_broadcaster
            ))

            # Acknowledge start
            await websocket.send_text(json.dumps({"status": "started", "session_id": session_id}))

            # Keep the connection alive to receive further interactions
            while True:
                # In a real implementation, we'd handle incoming user answers here
                await websocket.receive_text()
        else:
            await websocket.close(code=1008, reason="Protocol violation: First message must be 'start_project'")

    except WebSocketDisconnect:
        logger.info(f"Interactive client disconnected from session {session_id}")
    except Exception as e:
        logger.error(f"Error in interactive websocket for session {session_id}: {e}")
    finally:
        await manager.disconnect(websocket, reason="Interactive session ended")


@app.websocket("/api/copilotkit-ws")
async def copilotkit_websocket_endpoint(websocket: WebSocket):
    """Direct CopilotKit integration for chat messages - routes to orchestration."""
    manager = websocket.app.state.manager
    status_broadcaster = websocket.app.state.status_broadcaster
    
    # Use a specific client ID for CopilotKit sessions
    client_id = await manager.connect(websocket, client_id="copilotkit_session")
    disconnect_reason = "Unknown"
    
    logger.info(f"🤖 CopilotKit WebSocket connected: {client_id}")
    
    try:
        # Send welcome message to confirm connection
        welcome_message = agui_handler.create_agent_message(
            content="🤖 CopilotKit WebSocket connected! Ready for chat messages.",
            agent_name="System",
            session_id="copilotkit_session"
        )
        await websocket.send_text(json.dumps(agui_handler.serialize_message(welcome_message)))
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            logger.info(f"🔄 CopilotKit received: {message}")
            
            # Route directly to chat message handler - this is the KEY FIX
            if message.get("type") == "chat_message":
                content = message.get("content", "")
                session_id = message.get("session_id", "copilotkit_session")
                
                logger.info(f"🎯 Routing CopilotKit message to orchestration: '{content}'")
                
                # Direct routing to handle_chat_message - bypasses all the WebSocket complexity
                await handle_chat_message(session_id, manager, content, websocket.app.state)
                
            elif message.get("type") == "heartbeat":
                # Handle heartbeat for connection stability
                await websocket.send_text(json.dumps({
                    "type": "heartbeat_response",
                    "timestamp": datetime.now().isoformat()
                }))
                
            else:
                logger.warning(f"Unknown CopilotKit message type: {message.get('type')}")
                
    except WebSocketDisconnect as e:
        disconnect_reason = f"Code: {e.code}, Reason: {e.reason if e.reason else 'Normal closure'}"
        logger.info(f"CopilotKit client {client_id} disconnected: {disconnect_reason}")
    except Exception as e:
        disconnect_reason = f"Error: {e}"
        logger.error(f"Error in CopilotKit WebSocket for client {client_id}: {e}", exc_info=True)
    finally:
        await manager.disconnect(client_id, reason=disconnect_reason)


@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Enhanced WebSocket endpoint for more stable connections."""
    manager = websocket.app.state.manager
    heartbeat_monitor = websocket.app.state.heartbeat_monitor
    status_broadcaster = websocket.app.state.status_broadcaster

    client_id = await manager.connect(websocket, client_id="global_session")
    disconnect_reason = "Unknown"
    
    try:
        # Connection manager already sent welcome message - no need for duplicate
        logger.info(f"WebSocket endpoint ready for client {client_id}")
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("type") == "batch":
                for msg in message.get("messages", []):
                    await handle_websocket_message(client_id, msg, manager, heartbeat_monitor, status_broadcaster, websocket.app.state)
            else:
                await handle_websocket_message(client_id, message, manager, heartbeat_monitor, status_broadcaster, websocket.app.state)
                
    except WebSocketDisconnect as e:
        disconnect_reason = f"Code: {e.code}, Reason: {e.reason if e.reason else 'Normal closure'}"
        logger.info(f"Client {client_id} disconnected: {disconnect_reason}")
    except Exception as e:
        disconnect_reason = f"Error: {e}"
        logger.error(f"Error for client {client_id}: {e}", exc_info=True)
    finally:
        await manager.disconnect(client_id, reason=disconnect_reason)

# Configuration API endpoints for Settings page
@app.get("/api/config")
async def get_configuration():
    """Get current system configuration for Settings page."""
    from backend.config import settings, get_agent_configurations, get_environment_info
    
    return {
        "system": {
            "max_agents": settings.max_agents,
            "agent_timeout": settings.agent_timeout,
            "debug": settings.debug,
            "log_level": settings.log_level,
            "websocket_heartbeat_interval": settings.websocket_heartbeat_interval,
            "interactive_timeout_minutes": settings.interactive_timeout_minutes,
            "max_questions_per_session": settings.max_questions_per_session,
            "auto_proceed_on_timeout": settings.auto_proceed_on_timeout,
            "max_concurrent_workflows": settings.max_concurrent_workflows,
            "max_retry_attempts": settings.max_retry_attempts
        },
        "agents": get_agent_configurations(),
        "environment": get_environment_info()
    }

@app.post("/api/config")
async def update_configuration(config_update: Dict[str, Any]):
    """Update system configuration."""
    try:
        updated_fields = []
        
        if "system" in config_update:
            system_config = config_update["system"]
            from backend.config import settings
            
            # Update settings (in-memory for now)
            if "max_agents" in system_config:
                settings.max_agents = int(system_config["max_agents"])
                updated_fields.append("max_agents")
            
            if "agent_timeout" in system_config:
                settings.agent_timeout = int(system_config["agent_timeout"])
                updated_fields.append("agent_timeout")
        
        if "agents" in config_update:
            # Agent configuration updates (could be expanded)
            updated_fields.append("agent_configurations")
        
        logger.info(f"Configuration updated: {updated_fields}")
        return {
            "status": "success", 
            "message": f"Updated: {', '.join(updated_fields)}",
            "updated_fields": updated_fields
        }
        
    except Exception as e:
        logger.error(f"Failed to update configuration: {e}")
        raise HTTPException(status_code=500, detail=f"Configuration update failed: {str(e)}")

@app.post("/api/config/refresh")
async def refresh_configuration():
    """Refresh dynamic configuration cache from .env file."""
    try:
        from backend.dynamic_config import refresh_config
        refresh_config()
        logger.info("Configuration cache refreshed successfully")
        return {
            "status": "success",
            "message": "Configuration cache refreshed from .env file",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to refresh configuration: {e}")
        raise HTTPException(status_code=500, detail=f"Configuration refresh failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint for Replit monitoring."""
    return {
        "status": "healthy",
        "environment": "replit" if IS_REPLIT else "development",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "websocket": "available",
            "llm_providers": ["openai", "google"],
            "test_mode": os.getenv("TEST_MODE", "false").lower() == "true"
        }
    }

# File upload validation and rate limiting endpoints
@app.post("/api/uploads/validate")
async def validate_file_upload(request: Request):
    """
    Validate file upload before processing.
    Checks rate limits and file constraints.
    """
    try:
        # Get client IP for rate limiting
        client_ip = request.client.host if hasattr(request, 'client') else "unknown"
        
        # This would normally be called with file data, but for demo purposes:
        upload_rate_limiter = app.state.upload_rate_limiter
        
        # Example validation for a 500KB file
        test_size = 500 * 1024  # 500KB
        is_allowed, reason = await upload_rate_limiter.check_rate_limit(
            client_ip, test_size, RateLimitType.PER_IP
        )
        
        if not is_allowed:
            raise HTTPException(status_code=429, detail=reason)
        
        return {
            "status": "allowed",
            "message": reason,
            "rate_limit_info": upload_rate_limiter.get_rate_limit_status(client_ip)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload validation error: {e}")
        raise HTTPException(status_code=500, detail="Upload validation failed")

@app.get("/api/uploads/rate-limit/{identifier}")
async def get_upload_rate_limit_status(identifier: str):
    """Get rate limit status for a specific identifier"""
    try:
        upload_rate_limiter = app.state.upload_rate_limiter
        status = upload_rate_limiter.get_rate_limit_status(identifier)
        return status
    except Exception as e:
        logger.error(f"Error getting rate limit status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get rate limit status")

@app.get("/api/uploads/metrics")
async def get_upload_metrics():
    """Get global upload metrics for monitoring"""
    try:
        upload_rate_limiter = app.state.upload_rate_limiter
        metrics = upload_rate_limiter.get_global_metrics()
        
        # Also include LLM service performance metrics
        llm_metrics = {}
        if hasattr(app.state, 'llm_service') and app.state.llm_service:
            try:
                llm_metrics = app.state.llm_service.get_performance_metrics()
            except Exception as e:
                logger.warning(f"Could not get LLM metrics: {e}")
        
        return {
            "upload_metrics": metrics,
            "llm_metrics": llm_metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting upload metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get upload metrics")

# Additional API endpoints for status and monitoring  
@app.get("/api/status")
async def get_status():
    """Get current system status with enhanced metrics."""
    try:
        # Get upload rate limiter metrics
        upload_metrics = {}
        if hasattr(app.state, 'upload_rate_limiter'):
            upload_metrics = app.state.upload_rate_limiter.get_global_metrics()
        
        # Get LLM service status
        llm_status = {}
        if hasattr(app.state, 'llm_service') and app.state.llm_service:
            try:
                llm_status = app.state.llm_service.get_provider_status()
            except Exception as e:
                logger.warning(f"Could not get LLM status: {e}")
        
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
                "hitl": True,
                "upload_rate_limiting": True,  # New feature
                "yaml_validation": True,      # New feature
                "connection_pooling": True    # New feature
            },
            "upload_metrics": upload_metrics,
            "llm_status": llm_status
        }
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        # Return basic status on error
        return {
            "active_workflows": len(active_workflows),
            "environment": "replit" if IS_REPLIT else "development",
            "status": "partial - some metrics unavailable",
            "error": str(e)
        }

# Interactive session management endpoints
@app.post("/api/interactive/sessions/{session_id}/answers")
async def submit_interactive_answer(session_id: str, answer_data: Dict[str, Any]):
    """Submit an answer for an interactive session question."""
    try:
        # Find the active workflow with orchestrator
        workflow = active_workflows.get(session_id)
        if not workflow or not workflow.get("orchestrator"):
            raise HTTPException(status_code=404, detail=f"No active interactive session found for {session_id}")
        
        orchestrator = workflow["orchestrator"]
        session_manager = orchestrator.session_manager
        
        question_id = answer_data.get("question_id")
        answer_text = answer_data.get("answer", "")
        
        if not question_id:
            raise HTTPException(status_code=400, detail="question_id is required")
        
        success = await session_manager.submit_answer(session_id, question_id, answer_text)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to submit answer")
        
        # Get session status for response
        session_status = session_manager.get_session_status(session_id)
        
        return {
            "status": "success",
            "message": "Answer submitted successfully",
            "session_status": session_status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting interactive answer: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")

@app.get("/api/interactive/sessions/{session_id}/status")  
async def get_interactive_session_status(session_id: str):
    """Get the status of an interactive session."""
    try:
        # Find the active workflow with orchestrator
        workflow = active_workflows.get(session_id)
        if not workflow or not workflow.get("orchestrator"):
            raise HTTPException(status_code=404, detail=f"No active interactive session found for {session_id}")
        
        orchestrator = workflow["orchestrator"]
        session_manager = orchestrator.session_manager
        
        session_status = session_manager.get_session_status(session_id)
        
        if not session_status:
            raise HTTPException(status_code=404, detail="Session status not found")
        
        return session_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get session status: {str(e)}")

@app.post("/api/interactive/sessions/{session_id}/cancel")
async def cancel_interactive_session(session_id: str):
    """Cancel an active interactive session."""
    try:
        # Find the active workflow with orchestrator
        workflow = active_workflows.get(session_id)
        if not workflow or not workflow.get("orchestrator"):
            raise HTTPException(status_code=404, detail=f"No active interactive session found for {session_id}")
        
        orchestrator = workflow["orchestrator"] 
        session_manager = orchestrator.session_manager
        
        success = await session_manager.cancel_session(session_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to cancel session")
        
        return {
            "status": "success", 
            "message": "Interactive session cancelled"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cancel session: {str(e)}")

@app.get("/api/interactive/sessions")
async def list_interactive_sessions():
    """List all active interactive sessions."""
    try:
        all_sessions = []
        
        for session_id, workflow in active_workflows.items():
            if workflow.get("orchestrator"):
                orchestrator = workflow["orchestrator"]
                session_manager = orchestrator.session_manager
                session_status = session_manager.get_session_status(session_id)
                if session_status:
                    all_sessions.append(session_status)
        
        return {
            "sessions": all_sessions,
            "total_count": len(all_sessions)
        }
        
    except Exception as e:
        logger.error(f"Error listing interactive sessions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list sessions: {str(e)}")

# Performance monitoring and dashboard endpoints
@app.get("/api/performance/metrics/realtime")
async def get_realtime_metrics():
    """Get real-time performance metrics."""
    try:
        performance_monitor = app.state.performance_monitor
        metrics = performance_monitor.get_real_time_metrics()
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting realtime metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get realtime metrics: {str(e)}")

@app.get("/api/performance/summary")
async def get_performance_summary(hours: int = 1):
    """Get performance summary for specified time period."""
    try:
        if hours < 1 or hours > 168:  # Max 1 week
            raise HTTPException(status_code=400, detail="Hours must be between 1 and 168")
        
        performance_monitor = app.state.performance_monitor
        summary = performance_monitor.get_performance_summary(hours)
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting performance summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get performance summary: {str(e)}")

@app.get("/api/performance/workflows/{workflow_id}")
async def get_workflow_metrics(workflow_id: str):
    """Get detailed metrics for a specific workflow."""
    try:
        performance_monitor = app.state.performance_monitor
        
        if workflow_id not in performance_monitor.workflow_metrics:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        metric = performance_monitor.workflow_metrics[workflow_id]
        
        return {
            "workflow_id": metric.workflow_id,
            "config_name": metric.config_name,
            "session_id": metric.session_id,
            "status": metric.status,
            "start_time": metric.start_time,
            "end_time": metric.end_time,
            "duration": metric.duration,
            "agents_used": metric.agents_used,
            "artifacts_created": metric.artifacts_created,
            "error_message": metric.error_message,
            "is_completed": metric.is_completed
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow metrics: {str(e)}")

@app.get("/api/performance/agents")
async def get_agent_performance():
    """Get performance metrics for all agents."""
    try:
        performance_monitor = app.state.performance_monitor
        return {
            "agents": dict(performance_monitor.agent_performance),
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Error getting agent performance: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get agent performance: {str(e)}")

@app.get("/api/performance/connections")
async def get_connection_diagnostics(client_id: Optional[str] = None):
    """Get connection diagnostics for all clients or specific client."""
    try:
        manager = app.state.manager
        
        if client_id:
            # Get diagnostics for specific client
            diagnostics = manager.get_connection_diagnostics(client_id)
            if "error" in diagnostics:
                raise HTTPException(status_code=404, detail=diagnostics["error"])
            return diagnostics
        else:
            # Get system-wide diagnostics
            return manager.get_system_diagnostics()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting connection diagnostics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get connection diagnostics: {str(e)}")

@app.post("/api/performance/cleanup")
async def cleanup_performance_data(hours: int = 24):
    """Clean up old performance data."""
    try:
        if hours < 1 or hours > 8760:  # Max 1 year
            raise HTTPException(status_code=400, detail="Hours must be between 1 and 8760")
        
        performance_monitor = app.state.performance_monitor
        performance_monitor.cleanup_old_metrics(hours)
        
        return {
            "status": "success",
            "message": f"Cleaned up metrics older than {hours} hours",
            "cleaned_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cleaning up performance data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cleanup performance data: {str(e)}")

@app.get("/api/performance/dashboard")
async def get_dashboard_data():
    """Get comprehensive dashboard data including all key metrics."""
    try:
        performance_monitor = app.state.performance_monitor
        manager = app.state.manager
        
        # Get all key metrics
        realtime_metrics = performance_monitor.get_real_time_metrics()
        summary_1h = performance_monitor.get_performance_summary(1)
        summary_24h = performance_monitor.get_performance_summary(24)
        connection_diagnostics = manager.get_system_diagnostics()
        agent_performance = dict(performance_monitor.agent_performance)
        
        # Get LLM service metrics if available
        llm_metrics = {}
        if hasattr(app.state, 'llm_service') and app.state.llm_service:
            try:
                llm_metrics = app.state.llm_service.get_performance_metrics()
            except:
                pass
        
        # Get upload metrics
        upload_metrics = {}
        if hasattr(app.state, 'upload_rate_limiter'):
            upload_metrics = app.state.upload_rate_limiter.get_global_metrics()
        
        return {
            "dashboard_generated_at": datetime.now().isoformat(),
            "realtime_metrics": realtime_metrics,
            "summary_1h": summary_1h,
            "summary_24h": summary_24h,
            "connection_diagnostics": connection_diagnostics,
            "agent_performance": agent_performance,
            "llm_metrics": llm_metrics,
            "upload_metrics": upload_metrics,
            "system_info": {
                "uptime_seconds": time.time() - performance_monitor.start_time,
                "monitoring_active": performance_monitor._is_monitoring,
                "active_workflows_count": len([m for m in performance_monitor.workflow_metrics.values() if not m.is_completed])
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard data: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting BotArmy Backend...")
    print(f"Environment: {'Replit' if IS_REPLIT else 'Development'}")
    print("=" * 50)
    
    # Use PORT environment variable for Replit
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
