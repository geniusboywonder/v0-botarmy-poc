from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum
import json
import uuid
from pydantic import BaseModel, Field

class MessageType(Enum):
    """AG-UI Protocol message types"""
    # Agent to UI messages
    AGENT_MESSAGE = "agent_message"
    AGENT_STATUS = "agent_status"
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
                           metadata: Dict[str, Any] = None) -> AgentMessage:
        """Create an agent message"""
        return AgentMessage(
            content=content,
            agent_name=agent_name,
            session_id=session_id,
            metadata=metadata or {}
        )
    
    def create_agent_status(self, agent_name: str, state: AgentState, session_id: str,
                          current_task: str = None, progress: float = None) -> AgentStatus:
        """Create an agent status message"""
        return AgentStatus(
            agent_name=agent_name,
            state=state,
            session_id=session_id,
            current_task=current_task,
            progress=progress
        )
    
    def create_agent_thinking(self, agent_name: str, thought: str, session_id: str,
                            step: int = None) -> AgentThinking:
        """Create an agent thinking message"""
        return AgentThinking(
            agent_name=agent_name,
            thought=thought,
            session_id=session_id,
            step=step
        )
    
    def create_system_status(self, status: str, active_agents: List[str], 
                           session_id: str, health_data: Dict[str, Any] = None) -> SystemStatus:
        """Create a system status message"""
        return SystemStatus(
            status=status,
            active_agents=active_agents,
            session_id=session_id,
            system_health=health_data or {}
        )
    
    def create_error_message(self, error: str, session_id: str) -> AGUIMessage:
        """Create an error message"""
        return AGUIMessage(
            type=MessageType.SYSTEM_ERROR,
            session_id=session_id,
            data={"error": error, "timestamp": datetime.now().isoformat()}
        )
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get message history for a session"""
        if session_id in self.sessions:
            return self.sessions[session_id]["message_history"]
        return []
    
    def serialize_message(self, message: AGUIMessage) -> str:
        """Serialize message to JSON string"""
        return json.dumps(message.dict(), default=str)
    
    def deserialize_message(self, message_str: str) -> Dict[str, Any]:
        """Deserialize message from JSON string"""
        return json.loads(message_str)

# Global protocol handler
agui_handler = AGUIProtocolHandler()
