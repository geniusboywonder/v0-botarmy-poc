from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum
import json
import uuid
from pydantic import BaseModel, Field

from backend.agui.message_protocol import MessageProtocol

# --- Enums and Pydantic models for INCOMING messages ---
# These are kept for processing messages sent from the UI.
# The creation methods below will now generate standardized dictionaries.

class MessageType(Enum):
    """AG-UI Protocol message types"""
    # Agent to UI messages
    AGENT_MESSAGE = "agent_message"
    AGENT_STATUS = "agent_status"
    AGENT_PROGRESS = "agent_progress"
    AGENT_THINKING = "agent_thinking"
    AGENT_TOOL_CALL = "agent_tool_call"
    AGENT_RESULT = "agent_result"
    
    # UI to Agent messages
    USER_MESSAGE = "user_message"
    USER_COMMAND = "user_command"
    USER_FEEDBACK = "user_feedback"
    
    # System messages
    SYSTEM_STATUS = "system_status"
    SYSTEM_ERROR = "system_error"
    CONNECTION_ACK = "connection_ack"
    HEARTBEAT = "heartbeat"

class AgentState(Enum):
    """Agent state enumeration for AG-UI Protocol"""
    IDLE = "idle"
    THINKING = "thinking"
    WORKING = "working"
    WAITING_INPUT = "waiting_input"
    COMPLETED = "completed"
    ERROR = "error"

class AGUIMessage(BaseModel):
    """Base AG-UI Protocol message structure"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    agent_id: Optional[str] = None
    session_id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)

class AgentMessage(AGUIMessage):
    """Agent message to UI"""
    type: MessageType = MessageType.AGENT_MESSAGE
    content: str
    agent_name: str
    metadata: Optional[Dict[str, Any]] = None

class AgentStatus(AGUIMessage):
    """Agent status update"""
    type: MessageType = MessageType.AGENT_STATUS
    agent_name: str
    state: AgentState
    current_task: Optional[str] = None
    progress: Optional[float] = None

class AgentProgress(AGUIMessage):
    """Agent progress update for tasks"""
    type: MessageType = MessageType.AGENT_PROGRESS
    agent_name: str
    stage: str
    current: int
    total: int
    estimated_time_remaining: Optional[float] = None

class AgentThinking(AGUIMessage):
    """Agent thinking process (streaming thoughts)"""
    type: MessageType = MessageType.AGENT_THINKING
    agent_name: str
    thought: str
    step: Optional[int] = None

class UserMessage(AGUIMessage):
    """User message to agent"""
    type: MessageType = MessageType.USER_MESSAGE
    content: str
    target_agent: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = None

class SystemStatus(AGUIMessage):
    """System status message"""
    type: MessageType = MessageType.SYSTEM_STATUS
    status: str
    active_agents: List[str]
    system_health: Dict[str, Any]

class AGUIProtocolHandler:
    """Handles AG-UI Protocol message processing"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.message_handlers: Dict[MessageType, callable] = {}
        self.register_default_handlers()
    
    def register_default_handlers(self):
        """Register default message handlers"""
        self.message_handlers[MessageType.USER_MESSAGE] = self.handle_user_message
        self.message_handlers[MessageType.USER_COMMAND] = self.handle_user_command
        self.message_handlers[MessageType.USER_FEEDBACK] = self.handle_user_feedback
        self.message_handlers[MessageType.HEARTBEAT] = self.handle_heartbeat
    
    def create_session(self, session_id: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new AG-UI session"""
        session_data = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "message_history": [],
            "active_agents": [],
            "state": "active"
        }
        self.sessions[session_id] = session_data
        return session_data
    
    def process_message(self, message_data: Dict[str, Any], session_id: str) -> Optional[AGUIMessage]:
        """Process incoming message according to AG-UI Protocol"""
        try:
            # Parse message type
            msg_type = MessageType(message_data.get("type"))
            
            # Create appropriate message object
            if msg_type == MessageType.USER_MESSAGE:
                message = UserMessage(**message_data)
            else:
                message = AGUIMessage(**message_data)
            
            # Add session context
            message.session_id = session_id
            
            # Store in session history
            if session_id in self.sessions:
                self.sessions[session_id]["message_history"].append(message.dict())
            
            # Handle message
            if msg_type in self.message_handlers:
                return self.message_handlers[msg_type](message)
            
            return message
            
        except Exception as e:
            return self.create_error_message(f"Message processing error: {str(e)}", session_id)
    
    def handle_user_message(self, message: UserMessage) -> AGUIMessage:
        """Handle user message"""
        # This will be processed by the orchestrator
        return AgentMessage(
            content=f"Received message: {message.content}",
            agent_name="system",
            session_id=message.session_id,
            data={"original_message": message.dict()}
        )
    
    def handle_user_command(self, message: AGUIMessage) -> AGUIMessage:
        """Handle user command"""
        command = message.data.get("command")
        return AgentMessage(
            content=f"Processing command: {command}",
            agent_name="system",
            session_id=message.session_id
        )
    
    def handle_user_feedback(self, message: AGUIMessage) -> AGUIMessage:
        """Handle user feedback"""
        feedback = message.data.get("feedback")
        return AgentMessage(
            content=f"Feedback received: {feedback}",
            agent_name="system",
            session_id=message.session_id
        )
    
    def handle_heartbeat(self, message: AGUIMessage) -> AGUIMessage:
        """Handle heartbeat message"""
        return AGUIMessage(
            type=MessageType.HEARTBEAT,
            session_id=message.session_id,
            data={"status": "alive", "timestamp": datetime.now().isoformat()}
        )
    
    def create_agent_message(self, content: str, agent_name: str, session_id: str, 
                           metadata: Dict[str, Any] = None) -> Dict:
        """Create an agent message using the new standard protocol."""
        return MessageProtocol.create_agent_response(
            agent_name=agent_name,
            content=content,
            metadata=metadata,
            session_id=session_id
        )
    
    def create_agent_status(self, agent_name: str, state: AgentState, session_id: str,
                          current_task: str = None, progress: float = None) -> Dict:
        """Create an agent status message using the new standard protocol."""
        return MessageProtocol.create_agent_status_update(
            agent_name=agent_name,
            status=state.value,  # Convert Enum to string
            task=current_task,
            session_id=session_id
        )

    def create_agent_progress(self, agent_name: str, stage: str, current: int, total: int,
                            session_id: str, estimated_time_remaining: float = None) -> Dict:
        """Create an agent progress message using the new standard protocol."""
        # This is a new method, so it doesn't correspond to a method in the old protocol.
        # We will create a dictionary that conforms to our new AgentProgress model.
        return {
            "id": str(uuid.uuid4()),
            "type": MessageType.AGENT_PROGRESS.value,
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "stage": stage,
            "current": current,
            "total": total,
            "estimated_time_remaining": estimated_time_remaining,
            "session_id": session_id,
            "data": {}
        }
    
    def create_agent_thinking(self, agent_name: str, thought: str, session_id: str,
                            step: int = None) -> Dict:
        """Create an agent thinking message using the new standard protocol."""
        # The new protocol doesn't have a dedicated "thinking" type, so we use a system message.
        metadata = {"step": step}
        return MessageProtocol.create_system_message(
            content=thought,
            message_type="agent_thinking",
            session_id=session_id,
            metadata=metadata
        )
    
    def create_system_status(self, status: str, active_agents: List[str], 
                           session_id: str, health_data: Dict[str, Any] = None) -> Dict:
        """Create a system status message using the new standard protocol."""
        metadata = {
            "active_agents": active_agents,
            "system_health": health_data or {}
        }
        return MessageProtocol.create_system_message(
            content=status,
            message_type="system_status",
            session_id=session_id,
            metadata=metadata
        )
    
    def create_error_message(self, error: str, session_id: str, agent_name: str = "System", **kwargs) -> Dict:
        """Create an error message using the new standard protocol."""
        # This signature is updated to be more flexible and compatible with ErrorHandler.
        return MessageProtocol.create_error_message(
            error=error,
            agent_name=agent_name,
            session_id=session_id,
            # Pass any other details from ErrorHandler into metadata
            error_type=kwargs.get("details", "general")
        )
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get message history for a session"""
        if session_id in self.sessions:
            return self.sessions[session_id]["message_history"]
        return []
    
    def serialize_message(self, message: Dict) -> str:
        """Serialize message dictionary to JSON string"""
        # The message is now a dict, not a Pydantic model that needs .dict()
        return json.dumps(message, default=str)
    
    def deserialize_message(self, message_str: str) -> Dict[str, Any]:
        """Deserialize message from JSON string"""
        return json.loads(message_str)

# Global protocol handler
agui_handler = AGUIProtocolHandler()
