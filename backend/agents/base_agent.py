import controlflow as cf
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    COMPLETED = "completed"

class BaseAgent:
    """Base class for all BotArmy agents"""
    
    def __init__(self, name: str, description: str, instructions: str):
        self.name = name
        self.description = description
        self.instructions = instructions
        self.status = AgentStatus.IDLE
        self.last_activity = datetime.now()
        self.current_task = None
        self.task_history: List[Dict[str, Any]] = []
        
        self.websocket_callback: Optional[Callable] = None
        self.progress = 0.0
        self.current_step = ""
        
        # Create ControlFlow agent
        self.cf_agent = cf.Agent(
            name=self.name,
            description=self.description,
            instructions=self.instructions
        )
    
    def set_websocket_callback(self, callback: Callable):
        """Set callback function for WebSocket updates"""
        self.websocket_callback = callback
    
    async def _send_websocket_update(self, update_type: str, data: Dict[str, Any] = None):
        """Send real-time update via WebSocket"""
        if self.websocket_callback:
            update_data = {
                "type": update_type,
                "agent": self.name,
                "status": self.status.value,
                "timestamp": datetime.now().isoformat(),
                "progress": self.progress,
                "current_step": self.current_step,
                **(data or {})
            }
            try:
                await self.websocket_callback(update_data)
            except Exception as e:
                logger.error(f"WebSocket update failed for {self.name}: {e}")
    
    async def update_status(self, status: AgentStatus, task_info: Optional[str] = None):
        """Update agent status and activity timestamp"""
        self.status = status
        self.last_activity = datetime.now()
        if task_info:
            self.current_task = task_info
        
        logger.info(f"Agent {self.name} status updated to {status.value}")
        
        await self._send_websocket_update("agent_status_update", {
            "current_task": self.current_task
        })
    
    async def update_progress(self, progress: float, step: str = ""):
        """Update task progress and current step"""
        self.progress = max(0.0, min(100.0, progress))
        self.current_step = step
        
        await self._send_websocket_update("agent_progress_update", {
            "step_description": step
        })
    
    async def send_thinking_update(self, thought: str):
        """Send thinking process update"""
        await self._send_websocket_update("agent_thinking", {
            "thought": thought
        })
    
    async def send_message_update(self, message: str, message_type: str = "info"):
        """Send message update to UI"""
        await self._send_websocket_update("agent_message", {
            "message": message,
            "message_type": message_type
        })
    
    async def execute_task(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a task using ControlFlow with real-time updates"""
        await self.update_status(AgentStatus.ACTIVE, task_description)
        await self.update_progress(0.0, "Starting task...")
        
        try:
            # Send thinking update
            await self.send_thinking_update(f"Analyzing task: {task_description}")
            await self.update_progress(10.0, "Analyzing requirements...")
            
            # Create ControlFlow task
            await self.update_progress(20.0, "Creating execution plan...")
            task = cf.Task(
                objective=task_description,
                agents=[self.cf_agent],
                context=context or {}
            )
            
            # Send progress updates during execution
            await self.update_progress(30.0, "Executing task...")
            await self.send_thinking_update("Processing request with specialized knowledge...")
            
            # Execute task
            await self.update_progress(50.0, "Generating response...")
            result = await asyncio.to_thread(task.run)
            
            await self.update_progress(80.0, "Finalizing results...")
            
            # Record task completion
            task_record = {
                "description": task_description,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
            self.task_history.append(task_record)
            
            await self.update_progress(100.0, "Task completed successfully")
            await self.update_status(AgentStatus.COMPLETED)
            
            # Send completion message
            await self.send_message_update(f"Task completed: {task_description}", "success")
            
            return {
                "success": True,
                "result": result,
                "agent": self.name,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Task execution failed for {self.name}: {e}")
            await self.update_status(AgentStatus.ERROR)
            await self.send_message_update(f"Task failed: {str(e)}", "error")
            
            error_record = {
                "description": task_description,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
            self.task_history.append(error_record)
            
            return {
                "success": False,
                "error": str(e),
                "agent": self.name,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get current agent status information"""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "last_activity": self.last_activity.isoformat(),
            "current_task": self.current_task,
            "task_count": len(self.task_history),
            "progress": self.progress,
            "current_step": self.current_step
        }
