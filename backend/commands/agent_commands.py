from typing import Dict, Any

from backend.agent_status_broadcaster import AgentStatusBroadcaster

async def handle_pause_agent(status_broadcaster: AgentStatusBroadcaster, session_id: str, **kwargs):
    from backend.main import agent_pause_states
    agent_name = kwargs.get("agent_name")
    agent_pause_states[agent_name] = True
    await status_broadcaster.broadcast_agent_status(
        agent_name=agent_name,
        status="paused",
        task="Paused by user.",
        session_id=session_id
    )

async def handle_resume_agent(status_broadcaster: AgentStatusBroadcaster, session_id: str, **kwargs):
    from backend.main import agent_pause_states
    agent_name = kwargs.get("agent_name")
    agent_pause_states[agent_name] = False
    await status_broadcaster.broadcast_agent_status(
        agent_name=agent_name,
        status="working",
        task="Resumed by user.",
        session_id=session_id
    )

AGENT_COMMANDS = {
    "pause_agent": handle_pause_agent,
    "resume_agent": handle_resume_agent,
}
