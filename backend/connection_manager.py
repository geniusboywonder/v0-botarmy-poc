import asyncio
import json
import logging
import uuid
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict, deque

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

class ConnectionHealth:
    """Tracks health metrics for a WebSocket connection."""
    
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.connected_at = time.time()
        self.last_heartbeat = time.time()
        self.last_message = time.time()
        self.messages_sent = 0
        self.messages_received = 0
        self.errors = 0
        self.disconnections = 0
        self.latency_samples = deque(maxlen=10)  # Keep last 10 latency measurements
        
    def record_message_sent(self):
        self.messages_sent += 1
        self.last_message = time.time()
        
    def record_message_received(self):
        self.messages_received += 1
        self.last_message = time.time()
        
    def record_heartbeat(self):
        self.last_heartbeat = time.time()
        
    def record_error(self):
        self.errors += 1
        
    def record_latency(self, latency_ms: float):
        self.latency_samples.append(latency_ms)
        
    def get_average_latency(self) -> float:
        if not self.latency_samples:
            return 0.0
        return sum(self.latency_samples) / len(self.latency_samples)
    
    def get_uptime(self) -> float:
        return time.time() - self.connected_at
    
    def is_healthy(self, heartbeat_timeout: float = 60.0) -> bool:
        """Check if connection is healthy based on recent heartbeat."""
        return (time.time() - self.last_heartbeat) < heartbeat_timeout

class EnhancedConnectionManager:
    """
    Enhanced WebSocket connection manager with health monitoring,
    connection pooling, advanced message handling, and error recovery.
    """
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_metadata: Dict[str, dict] = {}
        self.connection_health: Dict[str, ConnectionHealth] = {}
        self.message_queue: Dict[str, List[str]] = {}
        
        # Enhanced features
        self.connection_groups: Dict[str, Set[str]] = defaultdict(set)  # Group connections by session/room
        self.rate_limits: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))  # Rate limiting per client
        self.blocked_clients: Set[str] = set()  # Temporarily blocked clients
        self.heartbeat_timers: Dict[str, asyncio.Task] = {}
        
        # Error handling and recovery
        self.connection_retries: Dict[str, int] = {}  # Track retry attempts per client
        self.failed_connections: Dict[str, float] = {}  # Track failed connection timestamps
        self.error_handlers: List[callable] = []  # Custom error handlers
        self.reconnection_callbacks: Dict[str, callable] = {}  # Client reconnection callbacks
        
        # Configuration - Disable heartbeat system temporarily to fix instability
        self.config = {
            "max_connections": 1000,
            "max_message_queue_size": 100,
            "heartbeat_interval": 0,     # DISABLED to prevent timeout conflicts
            "heartbeat_timeout": 0,      # DISABLED to prevent timeout conflicts  
            "rate_limit_window": 60.0,   # seconds
            "rate_limit_max_messages": 100,
            "connection_timeout": 3600.0, # 1 hour - very long to prevent timeouts
            "cleanup_interval": 60.0,    # seconds
            "max_retry_attempts": 3,     # Max reconnection attempts
            "retry_backoff_base": 2.0,   # Exponential backoff base
            "error_threshold": 5,        # Max errors before temporary block
            "block_duration": 300.0,     # 5 minutes block duration
        }
        
        # Start background tasks
        self._cleanup_task = None
        self._start_time = time.time()  # Add missing start time
        self._start_cleanup_task()
        
        logger.info("Enhanced Connection Manager initialized with error recovery")
    
    def _start_cleanup_task(self):
        """Start the background cleanup task."""
        if self._cleanup_task is None or self._cleanup_task.done():
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    async def _cleanup_loop(self):
        """Background task for cleaning up stale connections and data."""
        while True:
            try:
                await asyncio.sleep(self.config["cleanup_interval"])
                await self._cleanup_stale_connections()
                self._cleanup_failed_connections()
                self._cleanup_blocked_clients()
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
    
    async def _cleanup_stale_connections(self):
        """Remove stale connections that haven't responded to heartbeats."""
        current_time = time.time()
        stale_clients = []
        
        for client_id, health in self.connection_health.items():
            if not health.is_healthy(self.config["heartbeat_timeout"]):
                stale_clients.append(client_id)
        
        for client_id in stale_clients:
            logger.warning(f"Removing stale connection: {client_id}")
            await self.disconnect(client_id, reason="Stale connection - heartbeat timeout")
    
    def _cleanup_failed_connections(self):
        """Remove old failed connection records."""
        current_time = time.time()
        expired_failures = [
            client_id for client_id, fail_time in self.failed_connections.items()
            if current_time - fail_time > self.config["connection_timeout"]
        ]
        
        for client_id in expired_failures:
            del self.failed_connections[client_id]
            if client_id in self.connection_retries:
                del self.connection_retries[client_id]
    
    def _cleanup_blocked_clients(self):
        """Remove clients from blocked list after block duration expires."""
        current_time = time.time()
        unblock_clients = []
        
        for client_id in list(self.blocked_clients):
            if client_id in self.failed_connections:
                fail_time = self.failed_connections[client_id]
                if current_time - fail_time > self.config["block_duration"]:
                    unblock_clients.append(client_id)
        
        for client_id in unblock_clients:
            self.blocked_clients.discard(client_id)
            logger.info(f"Unblocked client: {client_id}")
    
    def add_error_handler(self, handler: callable):
        """Add a custom error handler function."""
        self.error_handlers.append(handler)
    
    async def _handle_connection_error(self, client_id: str, error: Exception, context: str = ""):
        """Enhanced error handling with recovery mechanisms."""
        if client_id in self.connection_health:
            self.connection_health[client_id].record_error()
        
        # Track errors for this client
        error_count = self.connection_health.get(client_id, ConnectionHealth(client_id)).errors
        
        logger.error(f"Connection error for {client_id} in {context}: {error} (error #{error_count})")
        
        # Call custom error handlers
        for handler in self.error_handlers:
            try:
                await handler(client_id, error, context)
            except Exception as handler_error:
                logger.error(f"Error in custom error handler: {handler_error}")
        
        # Block client if too many errors
        if error_count >= self.config["error_threshold"]:
            self.blocked_clients.add(client_id)
            self.failed_connections[client_id] = time.time()
            logger.warning(f"Blocked client {client_id} due to excessive errors")
        
        # Attempt graceful disconnect
        await self.disconnect(client_id, reason=f"Error: {str(error)[:100]}")
    
    async def send_with_retry(self, client_id: str, message: str, max_retries: int = 3) -> bool:
        """Send message with automatic retry on failure."""
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                success = await self.send_to_client(client_id, message)
                if success:
                    return True
                
                retry_count += 1
                if retry_count < max_retries:
                    # Exponential backoff
                    wait_time = self.config["retry_backoff_base"] ** retry_count
                    await asyncio.sleep(wait_time)
                    logger.info(f"Retrying message send to {client_id} (attempt {retry_count + 1})")
                    
            except Exception as e:
                await self._handle_connection_error(client_id, e, "send_with_retry")
                break
        
        logger.error(f"Failed to send message to {client_id} after {max_retries} retries")
        return False
    
    def get_connection_diagnostics(self, client_id: str) -> Dict[str, Any]:
        """Get detailed diagnostics for a connection."""
        health = self.connection_health.get(client_id)
        if not health:
            return {"error": "Client not found"}
        
        return {
            "client_id": client_id,
            "uptime_seconds": health.get_uptime(),
            "messages_sent": health.messages_sent,
            "messages_received": health.messages_received,
            "errors": health.errors,
            "average_latency_ms": health.get_average_latency(),
            "last_heartbeat_ago_seconds": time.time() - health.last_heartbeat,
            "is_healthy": health.is_healthy(self.config["heartbeat_timeout"]),
            "is_blocked": client_id in self.blocked_clients,
            "retry_count": self.connection_retries.get(client_id, 0),
            "queued_messages": len(self.message_queue.get(client_id, []))
        }
    
    def get_system_diagnostics(self) -> Dict[str, Any]:
        """Get system-wide connection diagnostics."""
        total_messages_sent = sum(h.messages_sent for h in self.connection_health.values())
        total_messages_received = sum(h.messages_received for h in self.connection_health.values())
        total_errors = sum(h.errors for h in self.connection_health.values())
        
        healthy_connections = sum(
            1 for h in self.connection_health.values() 
            if h.is_healthy(self.config["heartbeat_timeout"])
        )
        
        return {
            "total_connections": len(self.active_connections),
            "healthy_connections": healthy_connections,
            "blocked_clients": len(self.blocked_clients),
            "total_messages_sent": total_messages_sent,
            "total_messages_received": total_messages_received,
            "total_errors": total_errors,
            "queued_messages": sum(len(q) for q in self.message_queue.values()),
            "connection_groups": {group: len(clients) for group, clients in self.connection_groups.items()},
            "uptime_seconds": time.time() - getattr(self, '_start_time', time.time()),
            "config": self.config.copy()
        }

    async def connect(self, websocket: WebSocket, client_id: str = None, group: str = "default") -> str:
        """
        Enhanced connection method with health monitoring and group support.
        """
        # Check connection limits
        if len(self.active_connections) >= self.config["max_connections"]:
            await websocket.close(code=1013, reason="Server overloaded")
            raise ConnectionError("Maximum connections reached")
        
        await websocket.accept()
        
        if client_id is None:
            client_id = str(uuid.uuid4())

        # Store connection and metadata
        self.active_connections[client_id] = websocket
        self.connection_metadata[client_id] = {
            "connected_at": datetime.utcnow().isoformat(),
            "user_agent": websocket.headers.get("user-agent", "unknown"),
            "client_id": client_id,
            "group": group,
        }
        
        # Initialize health tracking
        self.connection_health[client_id] = ConnectionHealth(client_id)
        
        # Add to group
        self.connection_groups[group].add(client_id)
        
        logger.info(f"Client {client_id} connected to group '{group}'. Total connections: {len(self.active_connections)}")

        # Send consolidated welcome message (both system and agent-style)
        system_welcome = {
            "type": "system",
            "event": "connected", 
            "data": {
                "message": "Welcome to the BotArmy backend!",
                "client_id": client_id,
                "group": group,
                "server_time": datetime.utcnow().isoformat()
            },
        }
        
        try:
            await websocket.send_text(json.dumps(system_welcome))
            self.connection_health[client_id].record_message_sent()
            
            # Also send agent-style welcome message
            from backend.agui.agui_handler import agui_handler
            agent_welcome = agui_handler.create_agent_message(
                content="🔗 WebSocket connection established successfully!",
                agent_name="System",
                session_id=client_id
            )
            await websocket.send_text(agui_handler.serialize_message(agent_welcome))
            self.connection_health[client_id].record_message_sent()
            
        except Exception as e:
            logger.error(f"Failed to send welcome message to client {client_id}: {e}")
            await self.disconnect(client_id, f"Welcome message failed: {e}")
            raise

        # Process queued messages
        await self._process_queued_messages(client_id)

        return client_id

    async def disconnect(self, client_id: str, reason: str = "No reason given"):
        """Enhanced disconnect with cleanup of all related data."""
        websocket = self.active_connections.pop(client_id, None)
        metadata = self.connection_metadata.pop(client_id, None)
        health = self.connection_health.pop(client_id, None)
        
        # Cancel heartbeat timer
        if client_id in self.heartbeat_timers:
            self.heartbeat_timers[client_id].cancel()
            del self.heartbeat_timers[client_id]
        
        # Remove from groups
        if metadata:
            group = metadata.get("group", "default")
            self.connection_groups[group].discard(client_id)
            if not self.connection_groups[group]:  # Remove empty groups
                del self.connection_groups[group]
        
        # Update health metrics
        if health:
            health.disconnections += 1

        if websocket:
            try:
                if hasattr(websocket, 'client_state') and websocket.client_state.name == 'CONNECTED':
                    await websocket.close(code=1000, reason=reason[:120])
                logger.info(f"Client {client_id} disconnected. Reason: {reason}. Total connections: {len(self.active_connections)}")
            except Exception as e:
                logger.debug(f"Expected error closing websocket for client {client_id}: {e}")
        else:
            logger.debug(f"Client {client_id} was not found in active connections during disconnect")
        
        # Clean up rate limiting data
        if client_id in self.rate_limits:
            del self.rate_limits[client_id]
        
        self.blocked_clients.discard(client_id)

    def get_client_id(self, websocket: WebSocket) -> str | None:
        """
        Retrieves the client_id for a given WebSocket object.
        This is a reverse lookup and might be slow with many connections.
        """
        for client_id, ws in self.active_connections.items():
            if ws == websocket:
                return client_id
        return None

    async def send_to_client(self, client_id: str, message: str, priority: str = "normal"):
        """
        Enhanced send with rate limiting and priority support.
        """
        # Check if client is blocked
        if client_id in self.blocked_clients:
            logger.warning(f"Message to blocked client {client_id} discarded")
            return False
            
        # Check rate limiting (except for high priority messages)
        if priority != "high" and not self._check_rate_limit(client_id):
            logger.warning(f"Rate limit exceeded for client {client_id}, queuing message")
            self._queue_message(client_id, message)
            return False

        websocket = self.active_connections.get(client_id)
        if websocket:
            try:
                # Ensure message is properly serialized to JSON string
                if isinstance(message, dict):
                    message_str = json.dumps(message)
                else:
                    message_str = message
                await websocket.send_text(message_str)
                
                # Update health metrics
                if client_id in self.connection_health:
                    self.connection_health[client_id].record_message_sent()
                
                return True
            except Exception as e:
                logger.error(f"Failed to send message to client {client_id}: {e}. Queuing message.")
                
                # Update error count
                if client_id in self.connection_health:
                    self.connection_health[client_id].record_error()
                
                self._queue_message(client_id, message)
                return False
        else:
            logger.warning(f"Client {client_id} not connected. Queuing message.")
            self._queue_message(client_id, message)
            return False

    def _queue_message(self, client_id: str, message: str):
        """Helper to queue messages for disconnected clients."""
        if client_id not in self.message_queue:
            self.message_queue[client_id] = []
        
        # Limit queue size
        if len(self.message_queue[client_id]) >= self.config["max_message_queue_size"]:
            self.message_queue[client_id].pop(0)  # Remove oldest message
            
        self.message_queue[client_id].append(message)

    async def broadcast_to_all(self, message: str, priority: str = "normal"):
        """
        Enhanced broadcast with priority support.
        """
        # Create a list of send tasks
        tasks = [self.send_to_client(client_id, message, priority) for client_id in self.active_connections.keys()]
        # Run all send tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count successful sends
        successful = sum(1 for result in results if result is True)
        logger.debug(f"Broadcast message sent to {successful}/{len(tasks)} clients")
        
        return successful

    async def send_to_group(self, group: str, message: str, exclude_client: str = None, priority: str = "normal"):
        """Send message to all clients in a specific group."""
        if group not in self.connection_groups:
            logger.warning(f"Group '{group}' not found")
            return 0
            
        clients = self.connection_groups[group].copy()
        if exclude_client:
            clients.discard(exclude_client)
            
        tasks = [self.send_to_client(client_id, message, priority) for client_id in clients]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = sum(1 for result in results if result is True)
        logger.debug(f"Group '{group}' message sent to {successful}/{len(tasks)} clients")
        
        return successful

    def _check_rate_limit(self, client_id: str) -> bool:
        """Check if client is within rate limits."""
        now = time.time()
        window_start = now - self.config["rate_limit_window"]
        
        # Clean old entries
        client_history = self.rate_limits[client_id]
        while client_history and client_history[0] < window_start:
            client_history.popleft()
            
        # Check limit
        if len(client_history) >= self.config["rate_limit_max_messages"]:
            return False
            
        # Add current message
        client_history.append(now)
        return True

    async def _process_queued_messages(self, client_id: str):
        """Process any queued messages for a newly connected client."""
        if client_id in self.message_queue:
            num_queued = len(self.message_queue[client_id])
            messages_to_send = self.message_queue.pop(client_id)
            logger.info(f"Sending {num_queued} queued messages to client {client_id}...")
            
            for message in messages_to_send:
                try:
                    await self.send_to_client(client_id, message, "high")  # High priority for queued messages
                except Exception as e:
                    logger.error(f"Failed to send queued message to client {client_id}: {e}. Message lost.")
                    
            logger.info(f"Finished sending queued messages for client {client_id}")

    def get_connection_stats(self) -> dict:
        """
        Enhanced connection statistics with health metrics.
        """
        total_uptime = sum(health.get_uptime() for health in self.connection_health.values())
        total_messages_sent = sum(health.messages_sent for health in self.connection_health.values())
        total_messages_received = sum(health.messages_received for health in self.connection_health.values())
        total_errors = sum(health.errors for health in self.connection_health.values())
        
        healthy_connections = sum(1 for health in self.connection_health.values() 
                                if health.is_healthy(self.config["heartbeat_timeout"]))
        
        return {
            "active_connections": len(self.active_connections),
            "healthy_connections": healthy_connections,
            "blocked_clients": len(self.blocked_clients),
            "total_groups": len(self.connection_groups),
            "queued_messages": {client_id: len(messages) for client_id, messages in self.message_queue.items()},
            "total_messages_sent": total_messages_sent,
            "total_messages_received": total_messages_received,
            "total_errors": total_errors,
            "average_uptime": total_uptime / len(self.connection_health) if self.connection_health else 0,
            "groups": {group: len(clients) for group, clients in self.connection_groups.items()},
            "config": self.config
        }

    def get_client_health(self, client_id: str) -> Optional[dict]:
        """Get detailed health information for a specific client."""
        if client_id not in self.connection_health:
            return None
            
        health = self.connection_health[client_id]
        return {
            "client_id": client_id,
            "uptime": health.get_uptime(),
            "messages_sent": health.messages_sent,
            "messages_received": health.messages_received,
            "errors": health.errors,
            "average_latency": health.get_average_latency(),
            "is_healthy": health.is_healthy(self.config["heartbeat_timeout"]),
            "last_heartbeat": health.last_heartbeat,
            "last_message": health.last_message
        }
