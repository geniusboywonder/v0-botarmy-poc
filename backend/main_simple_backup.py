#!/usr/bin/env python3
"""
Simplified BotArmy Backend for debugging connection issues
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Basic imports that should always work
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Simple WebSocket connection manager
class SimpleConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> origin/feature/add-test-framework
=======
        
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        client_id = f"client_{len(self.active_connections)}"
        self.active_connections[client_id] = websocket
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> origin/feature/add-test-framework
=======
        
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
        # Send welcome message
        welcome_msg = {
            "type": "system",
            "data": {
                "event": "connected",
                "client_id": client_id,
                "message": "✅ Connected to BotArmy Backend (Simple Mode)"
            },
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send_text(json.dumps(welcome_msg))
        logger.info(f"Client {client_id} connected")
        return client_id
<<<<<<< HEAD
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature/add-test-framework
=======
    
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    async def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        logger.info(f"Client {client_id} disconnected")
<<<<<<< HEAD
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature/add-test-framework
=======
    
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    async def send_to_client(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_text(json.dumps(message))
<<<<<<< HEAD
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature/add-test-framework
=======
    
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    async def broadcast_to_all(self, message: dict):
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except:
                # Connection might be closed
                pass

# Create FastAPI app
app = FastAPI(
    title="BotArmy Backend (Simple)",
<<<<<<< HEAD
<<<<<<< HEAD
    version="1.0.0", 
=======
    version="1.0.0",
>>>>>>> origin/feature/add-test-framework
=======
    version="1.0.0", 
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    description="Simplified backend for debugging"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global connection manager
manager = SimpleConnectionManager()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BotArmy Backend (Simple Mode) is running",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": "development",
        "features": {
            "websockets": True,
            "basic_commands": True
        }
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "connections": len(manager.active_connections)
    }

async def handle_simple_command(client_id: str, command: str, data: dict):
    """Handle simple commands"""
<<<<<<< HEAD
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature/add-test-framework
=======
    
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    if command == "ping":
        response = {
            "type": "agent_response",
            "agent_name": "System",
            "content": "✅ Backend connection successful! Simple mode is working.",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_to_client(client_id, response)
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
        
    elif command == "test_openai":
        # Simple OpenAI test without actual API call
        response = {
            "type": "agent_response", 
<<<<<<< HEAD
=======

    elif command == "test_openai":
        # Simple OpenAI test without actual API call
        response = {
            "type": "agent_response",
>>>>>>> origin/feature/add-test-framework
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            "agent_name": "OpenAI Test",
            "content": "🧠 Testing OpenAI connection...\n\n⚠️ Simple mode: OpenAI test skipped (add API key to enable)",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_to_client(client_id, response)
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> origin/feature/add-test-framework
=======
        
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    elif command == "start_project":
        brief = data.get("brief", "No brief provided")
        response = {
            "type": "agent_response",
<<<<<<< HEAD
<<<<<<< HEAD
            "agent_name": "System", 
=======
            "agent_name": "System",
>>>>>>> origin/feature/add-test-framework
=======
            "agent_name": "System", 
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            "content": f"🚀 Project started in simple mode!\n\nBrief: {brief}\n\n⚠️ Full workflow disabled in simple mode",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_to_client(client_id, response)
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> origin/feature/add-test-framework
=======
        
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    else:
        response = {
            "type": "agent_response",
            "agent_name": "System",
            "content": f"⚠️ Unknown command: {command}",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_to_client(client_id, response)

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Simple WebSocket endpoint"""
    client_id = await manager.connect(websocket)
<<<<<<< HEAD
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature/add-test-framework
=======
    
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            
            logger.info(f"Received from {client_id}: {message}")
            
            msg_type = message.get("type")
            
<<<<<<< HEAD
=======

            logger.info(f"Received from {client_id}: {message}")

            msg_type = message.get("type")

>>>>>>> origin/feature/add-test-framework
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            if msg_type == "user_command":
                command_data = message.get("data", {})
                command = command_data.get("command")
                await handle_simple_command(client_id, command, command_data)
<<<<<<< HEAD
<<<<<<< HEAD
                
=======

>>>>>>> origin/feature/add-test-framework
=======
                
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            elif msg_type == "ping":
                # Respond to ping
                pong_response = {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_to_client(client_id, pong_response)
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
                
            else:
                logger.warning(f"Unknown message type: {msg_type}")
                
<<<<<<< HEAD
=======

            else:
                logger.warning(f"Unknown message type: {msg_type}")

>>>>>>> origin/feature/add-test-framework
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected normally")
    except Exception as e:
        logger.error(f"Error for client {client_id}: {e}")
    finally:
        await manager.disconnect(client_id)

if __name__ == "__main__":
    print("🚀 Starting BotArmy Backend (Simple Mode)...")
    print("This is a simplified version for debugging connection issues")
    print("=" * 60)
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    
    # Use environment PORT or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting server on http://localhost:{port}")
    print(f"WebSocket endpoint: ws://localhost:{port}/api/ws")
    print("=" * 60)
    
    uvicorn.run(
        "main_simple:app", 
        host="0.0.0.0", 
        port=port, 
<<<<<<< HEAD
=======

    # Use environment PORT or default to 8000
    port = int(os.getenv("PORT", 8000))

    print(f"Starting server on http://localhost:{port}")
    print(f"WebSocket endpoint: ws://localhost:{port}/api/ws")
    print("=" * 60)

    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=port,
>>>>>>> origin/feature/add-test-framework
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
        reload=True,
        log_level="info"
    )
