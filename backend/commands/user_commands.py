import asyncio
from typing import Dict, Any

from backend.connection_manager import EnhancedConnectionManager
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.runtime_env import IS_REPLIT
from backend.agui.protocol import agui_handler

async def handle_ping(manager: EnhancedConnectionManager, session_id: str, **kwargs):
    env_mode = "Replit" if IS_REPLIT else "Development"
    response = agui_handler.create_agent_message(
        content=f"✅ Backend connection successful! Running in {env_mode} mode.",
        agent_name="System",
        session_id=session_id
    )
    await manager.broadcast_to_all(agui_handler.serialize_message(response))

async def handle_test_openai(manager: EnhancedConnectionManager, session_id: str, app_state: Any, **kwargs):
    from backend.main import test_openai_connection
    test_message = kwargs.get("message")
    asyncio.create_task(test_openai_connection(session_id, manager, test_message))

async def handle_chat_message(manager: EnhancedConnectionManager, session_id: str, app_state: Any, **kwargs):
    from backend.main import handle_chat_message
    chat_text = kwargs.get("text", "")
    if chat_text:
        asyncio.create_task(handle_chat_message(session_id, manager, chat_text, app_state))

async def handle_stop_all_agents(manager: EnhancedConnectionManager, session_id: str, **kwargs):
    from backend.main import active_workflows, agent_pause_states
    if session_id in active_workflows:
        active_workflows[session_id]["status"] = "stopped"
        for agent_name in ["Analyst", "Architect", "Developer", "Tester", "Deployer"]:
            agent_pause_states[agent_name] = True
        
        response = agui_handler.create_agent_message(
            content="🛑 All agent activities have been stopped. Agents are now paused.",
            agent_name="System",
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))
    else:
        response = agui_handler.create_agent_message(
            content="No active workflows to stop.",
            agent_name="System", 
            session_id=session_id
        )
        await manager.broadcast_to_all(agui_handler.serialize_message(response))

async def handle_start_project(manager: EnhancedConnectionManager, session_id: str, app_state: Any, **kwargs):
    from backend.main import handle_chat_message
    project_brief = kwargs.get("brief", "No brief provided.")
    chat_text = f"start project {project_brief}"
    asyncio.create_task(handle_chat_message(session_id, manager, chat_text, app_state))

async def handle_set_artifact_preference(**kwargs):
    from backend.main import artifact_preferences
    artifact_id = kwargs.get("artifact_id")
    is_enabled = kwargs.get("is_enabled")
    if artifact_id is not None and is_enabled is not None:
        artifact_preferences[artifact_id] = is_enabled

USER_COMMANDS = {
    "ping": handle_ping,
    "test_openai": handle_test_openai,
    "chat_message": handle_chat_message,
    "stop_all_agents": handle_stop_all_agents,
    "start_project": handle_start_project,
    "set_artifact_preference": handle_set_artifact_preference,
}
