from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time communication"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_data: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        """Accept and store a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_data[websocket] = {
            "client_id": client_id,
            "connected_at": datetime.now(),
            "last_ping": datetime.now()
        }
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            client_data = self.connection_data.get(websocket, {})
            client_id = client_data.get("client_id", "unknown")
            self.active_connections.remove(websocket)
            del self.connection_data[websocket]
            logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific client"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients"""
        if not self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_heartbeat(self):
        """Send periodic heartbeat to maintain connections"""
        heartbeat_message = {
            "type": "heartbeat",
            "timestamp": datetime.now().isoformat(),
            "active_connections": len(self.active_connections)
        }
        await self.broadcast(heartbeat_message)

# Global connection manager
manager = ConnectionManager()

from agui.websocket_adapter import agui_websocket
from agui.protocol import MessageType

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("BotArmy Backend starting up...")
    
    # Start heartbeat task
    heartbeat_task = asyncio.create_task(heartbeat_loop())
    
    yield
    
    # Shutdown
    logger.info("BotArmy Backend shutting down...")
    heartbeat_task.cancel()
    try:
        await heartbeat_task
    except asyncio.CancelledError:
        pass

async def heartbeat_loop():
    """Periodic heartbeat to maintain WebSocket connections"""
    while True:
        try:
            await asyncio.sleep(30)  # Send heartbeat every 30 seconds
            await manager.send_heartbeat()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")

# Create FastAPI app
app = FastAPI(
    title="BotArmy Backend",
    description="Multi-agent AI orchestration system backend",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "BotArmy Backend is running",
        "timestamp": datetime.now().isoformat(),
        "active_connections": len(manager.active_connections)
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_connections": len(manager.active_connections),
        "services": {
            "websocket": "operational",
            "agents": "initializing"
        }
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for real-time communication"""
    client_id = None
    try:
        # Accept connection
        await manager.connect(websocket, client_id="frontend")
        
        # Send welcome message
        welcome_message = {
            "type": "connection_established",
            "message": "Connected to BotArmy Backend",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_personal_message(welcome_message, websocket)
        
        # Listen for messages
        while True:
            try:
                # Wait for message with timeout
                data = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)
                message = json.loads(data)
                
                # Update last ping time
                if websocket in manager.connection_data:
                    manager.connection_data[websocket]["last_ping"] = datetime.now()
                
                # Handle different message types
                await handle_websocket_message(websocket, message)
                
            except asyncio.TimeoutError:
                logger.warning("WebSocket timeout - sending ping")
                ping_message = {
                    "type": "ping",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_personal_message(ping_message, websocket)
                
    except WebSocketDisconnect:
        logger.info("Client disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)

@app.websocket("/ws/agui")
async def agui_websocket_endpoint(websocket: WebSocket):
    """AG-UI Protocol WebSocket endpoint"""
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        await agui_websocket.connect(websocket, session_id)
        
        while True:
            try:
                # Receive message
                data = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)
                message_data = json.loads(data)
                
                # Handle through AG-UI Protocol
                await agui_websocket.handle_message(websocket, session_id, message_data)
                
            except asyncio.TimeoutError:
                # Send heartbeat
                heartbeat = {
                    "type": MessageType.HEARTBEAT.value,
                    "session_id": session_id,
                    "data": {"status": "alive"}
                }
                await agui_websocket.send_message(websocket, heartbeat)
                
    except WebSocketDisconnect:
        logger.info(f"AG-UI session {session_id} disconnected")
    except Exception as e:
        logger.error(f"AG-UI WebSocket error: {e}")
    finally:
        agui_websocket.disconnect(session_id)

async def handle_websocket_message(websocket: WebSocket, message: dict):
    """Handle incoming WebSocket messages"""
    message_type = message.get("type", "unknown")
    
    if message_type == "pong":
        # Client responded to ping
        logger.debug("Received pong from client")
        return
    
    elif message_type == "chat_message":
        # Handle chat messages (will be expanded with agent integration)
        response = {
            "type": "chat_response",
            "message": f"Received: {message.get('content', '')}",
            "timestamp": datetime.now().isoformat(),
            "agent": "system"
        }
        await manager.send_personal_message(response, websocket)
    
    elif message_type == "agent_status_request":
        # Send current agent status
        status_response = {
            "type": "agent_status_update",
            "agents": [
                {"name": "Analyst", "status": "idle", "last_activity": datetime.now().isoformat()},
                {"name": "Architect", "status": "active", "last_activity": datetime.now().isoformat()},
                {"name": "Developer", "status": "idle", "last_activity": datetime.now().isoformat()},
                {"name": "Tester", "status": "idle", "last_activity": datetime.now().isoformat()},
                {"name": "Deployer", "status": "idle", "last_activity": datetime.now().isoformat()},
                {"name": "Monitor", "status": "active", "last_activity": datetime.now().isoformat()}
            ],
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_personal_message(status_response, websocket)
    
    else:
        logger.warning(f"Unknown message type: {message_type}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
