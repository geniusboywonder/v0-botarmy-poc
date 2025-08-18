from fastapi import WebSocket
from typing import Dict, Any, Optional
import json
import logging
from .protocol import AGUIProtocolHandler, MessageType, AgentState
from ..agents.orchestrator import orchestrator

logger = logging.getLogger(__name__)

class AGUIWebSocketAdapter:
    """WebSocket adapter for AG-UI Protocol"""
    
    def __init__(self, protocol_handler: AGUIProtocolHandler):
        self.protocol_handler = protocol_handler
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Connect a WebSocket with AG-UI Protocol session"""
        await websocket.accept()
        
        # Create AG-UI session
        session = self.protocol_handler.create_session(session_id)
        self.active_connections[session_id] = websocket
        
        orchestrator.set_websocket_callback(self._handle_agent_update)
        
        # Send connection acknowledgment
        ack_message = {
            "type": MessageType.CONNECTION_ACK.value,
            "session_id": session_id,
            "data": {
                "message": "Connected to BotArmy AG-UI Protocol",
                "session": session
            }
        }
        await self.send_message(websocket, ack_message)
        
        logger.info(f"AG-UI session {session_id} connected")
    
    async def _handle_agent_update(self, update_data: Dict[str, Any]):
        """Handle real-time updates from agents and broadcast to all sessions"""
        # Broadcast update to all connected sessions
        for session_id, websocket in self.active_connections.items():
            try:
                # Convert to AG-UI Protocol format
                agui_message = {
                    "type": "agent_update",
                    "session_id": session_id,
                    "timestamp": update_data.get("timestamp"),
                    "data": update_data
                }
                await self.send_message(websocket, agui_message)
            except Exception as e:
                logger.error(f"Failed to send update to session {session_id}: {e}")
    
    def disconnect(self, session_id: str):
        """Disconnect a session"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"AG-UI session {session_id} disconnected")
    
    async def handle_message(self, websocket: WebSocket, session_id: str, message_data: Dict[str, Any]):
        """Handle incoming WebSocket message using AG-UI Protocol"""
        try:
            # Process message through AG-UI Protocol
            response = self.protocol_handler.process_message(message_data, session_id)
            
            if response:
                await self.send_message(websocket, response.dict())
            
            # Handle specific message types
            msg_type = MessageType(message_data.get("type"))
            
            if msg_type == MessageType.USER_MESSAGE:
                await self.handle_user_message(websocket, session_id, message_data)
            elif msg_type == MessageType.USER_COMMAND:
                await self.handle_user_command(websocket, session_id, message_data)
                
        except Exception as e:
            logger.error(f"Error handling AG-UI message: {e}")
            error_response = self.protocol_handler.create_error_message(str(e), session_id)
            await self.send_message(websocket, error_response.dict())
    
    async def handle_user_message(self, websocket: WebSocket, session_id: str, message_data: Dict[str, Any]):
        """Handle user message and route to appropriate agent"""
        content = message_data.get("content", "")
        target_agent = message_data.get("target_agent")
        
        # Send thinking status
        thinking_msg = self.protocol_handler.create_agent_thinking(
            agent_name="system",
            thought="Processing your message...",
            session_id=session_id
        )
        await self.send_message(websocket, thinking_msg.dict())
        
        if target_agent and target_agent in orchestrator.agents:
            # Send to specific agent
            result = await orchestrator.send_message_to_agent(target_agent, content)
            
            # Send agent response
            agent_response = self.protocol_handler.create_agent_message(
                content=result.get("result", "No response"),
                agent_name=target_agent,
                session_id=session_id,
                metadata={"success": result.get("success", False)}
            )
            await self.send_message(websocket, agent_response.dict())
            
        else:
            # General message - route to analyst for initial processing
            result = await orchestrator.send_message_to_agent("analyst", content)
            
            agent_response = self.protocol_handler.create_agent_message(
                content=result.get("result", "I'll help you with that request."),
                agent_name="analyst",
                session_id=session_id,
                metadata={"success": result.get("success", False)}
            )
            await self.send_message(websocket, agent_response.dict())
    
    async def handle_user_command(self, websocket: WebSocket, session_id: str, message_data: Dict[str, Any]):
        """Handle user commands"""
        command = message_data.get("data", {}).get("command")
        
        if command == "start_project":
            # Start new project workflow
            project_desc = message_data.get("data", {}).get("description", "New project")
            requirements = message_data.get("data", {}).get("requirements", {})
            
            workflow_id = await orchestrator.start_project_workflow(project_desc, requirements)
            
            response = self.protocol_handler.create_agent_message(
                content=f"Started new project workflow: {workflow_id}",
                agent_name="system",
                session_id=session_id,
                metadata={"workflow_id": workflow_id}
            )
            await self.send_message(websocket, response.dict())
            
        elif command == "get_agent_status":
            # Get agent status
            status = await orchestrator.get_agent_status()
            
            for agent_name, agent_info in status.items():
                status_msg = self.protocol_handler.create_agent_status(
                    agent_name=agent_name,
                    state=AgentState(agent_info["status"]),
                    session_id=session_id,
                    current_task=agent_info.get("current_task")
                )
                await self.send_message(websocket, status_msg.dict())
    
    async def send_message(self, websocket: WebSocket, message: Dict[str, Any]):
        """Send message through WebSocket"""
        try:
            await websocket.send_text(json.dumps(message, default=str))
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
    
    async def broadcast_agent_status(self, agent_name: str, state: AgentState, 
                                   current_task: str = None, progress: float = None):
        """Broadcast agent status to all connected sessions"""
        for session_id, websocket in self.active_connections.items():
            status_msg = self.protocol_handler.create_agent_status(
                agent_name=agent_name,
                state=state,
                session_id=session_id,
                current_task=current_task,
                progress=progress
            )
            await self.send_message(websocket, status_msg.dict())
    
    async def broadcast_system_status(self, status: str, health_data: Dict[str, Any] = None):
        """Broadcast system status to all connected sessions"""
        active_agents = list(orchestrator.agents.keys())
        
        for session_id, websocket in self.active_connections.items():
            system_msg = self.protocol_handler.create_system_status(
                status=status,
                active_agents=active_agents,
                session_id=session_id,
                health_data=health_data or {}
            )
            await self.send_message(websocket, system_msg.dict())

# Global AG-UI WebSocket adapter
from .protocol import agui_handler
agui_websocket = AGUIWebSocketAdapter(agui_handler)
