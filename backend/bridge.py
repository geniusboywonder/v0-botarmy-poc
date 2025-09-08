import logging
import asyncio
import re
from backend.agui.protocol import agui_handler, AgentState

class AGUI_Handler(logging.Handler):
    """
    A custom logging handler that acts as a bridge between ControlFlow/Prefect's
    logging system and the AG-UI WebSocket protocol.

    It intercepts log records, transforms them into structured status messages,
    and sends them to the frontend via the AgentStatusBroadcaster.
    """
    def __init__(self, loop, status_broadcaster=None):
        super().__init__()
        self.loop = loop
        self.status_broadcaster = status_broadcaster
        self.is_emitting = False

    def set_status_broadcaster(self, status_broadcaster):
        """Set the status broadcaster after initialization to avoid circular imports."""
        self.status_broadcaster = status_broadcaster

    def emit(self, record: logging.LogRecord):
        """
        This method is called for every log record from a synchronous context.
        We schedule the asynchronous broadcast on the running event loop.
        """
        if self.is_emitting:
            return
        try:
            self.is_emitting = True
            if self.loop.is_running():
                asyncio.create_task(self._async_emit(record))
        finally:
            self.is_emitting = False

    async def _async_emit(self, record: logging.LogRecord):
        """
        Asynchronously transforms the log record and broadcasts it.
        """
        try:
            # Skip if no broadcaster is set
            if not self.status_broadcaster:
                return

            agent_name = getattr(record, 'task_run_name', None)
            session_id = getattr(record, 'flow_run_id', None)

            # Only process logs that have agent and session context
            if not agent_name or not session_id:
                return

            log_message = record.getMessage()

            # Use regex to parse messages for more specific status updates
            if "Starting" in log_message and "task" in log_message:
                # Extract task description from the log if possible
                match = re.search(r"for brief: '([^']*)'", log_message)
                task_description = match.group(1) + "..." if match else "Processing request."
                await self.status_broadcaster.broadcast_agent_status(
                    agent_name=agent_name,
                    status="working",
                    task=task_description,
                    session_id=session_id
                )

            elif "is thinking..." in log_message:
                from backend.agent_status_broadcaster import broadcast_agent_thinking
                await broadcast_agent_thinking(self.status_broadcaster, agent_name, "Processing...", session_id)

            elif "completed" in log_message:
                # The actual result is returned by the task, so we just send a generic completion status.
                # A more advanced implementation could capture the task result here.
                # Note: The result itself isn't in the log, so we send a generic message.
                # The actual result is handled by the workflow. This is a slight duplication.
                # A future refactor could unify this.
                await self.status_broadcaster.broadcast_agent_completed(agent_name, "Task finished successfully.", session_id)

        except Exception as e:
            # Avoid crashing the logger
            print(f"Error in AGUI_Handler: {e}")
