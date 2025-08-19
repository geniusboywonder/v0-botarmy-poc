import logging
import asyncio
from backend.agui.protocol import agui_handler, AgentMessage, AgentStatus, AgentState

class AGUI_Handler(logging.Handler):
    """
    A custom logging handler that acts as a bridge between ControlFlow/Prefect's
    logging system and the AG-UI WebSocket protocol.

    It intercepts log records, transforms them into AG-UI messages, and sends
    them to the frontend via the provided WebSocket connection manager.
    """
    def __init__(self, connection_manager, loop):
        super().__init__()
        self.connection_manager = connection_manager
        self.loop = loop

    def emit(self, record: logging.LogRecord):
        """
        This method is called for every log record from a synchronous context.
        We schedule the asynchronous broadcast on the running event loop.
        """
        if self.loop.is_running():
            asyncio.create_task(self._async_emit(record))

    async def _async_emit(self, record: logging.LogRecord):
        """
        Asynchronously transforms the log record and broadcasts it.
        """
        try:
            # Prefect attaches rich context to its log records. We can extract it.
            agent_name = getattr(record, 'task_run_name', 'System')
            session_id = getattr(record, 'flow_run_id', 'global_session')

            # Simple mapping from log level to agent state
            state = AgentState.WORKING
            if record.levelno >= logging.ERROR:
                state = AgentState.ERROR
            elif record.levelno <= logging.INFO:
                state = AgentState.IDLE # Or based on message content

            # For now, we will treat every log as a generic agent message.
            # We can add more sophisticated parsing later.
            agui_message = agui_handler.create_agent_message(
                content=record.getMessage(),
                agent_name=agent_name,
                session_id=session_id
            )

            serialized_message = agui_handler.serialize_message(agui_message)

            # Use the connection manager to broadcast the message
            await self.connection_manager.broadcast(serialized_message)

        except Exception as e:
            # Avoid crashing the logger
            print(f"Error in AGUI_Handler: {e}")
