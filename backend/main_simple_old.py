#!/usr/bin/env python3
"""
Simplified BotArmy Backend with Test Mode Support
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

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Basic imports that should always work
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Check test mode
TEST_MODE = os.getenv("AGENT_TEST_MODE", "false").lower() == "true"

# Try to import LLM service
try:
    from backend.services.llm_service import get_llm_service
    HAS_LLM_SERVICE = True
except ImportError:
    HAS_LLM_SERVICE = False
    print("Warning: Could not import LLM service")

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
        
    async def connect(self, websocket: WebSocket, endpoint: str = "unknown") -> str:
        await websocket.accept()
        client_id = f"client_{len(self.active_connections)}_{endpoint}"
        self.active_connections[client_id] = websocket
        
        # Send welcome message
        test_mode_status = "🧪 TEST_MODE enabled" if TEST_MODE else "🔥 Full mode enabled"
        welcome_msg = {
            "type": "system",
            "data": {
                "event": "connected",
                "client_id": client_id,
                "message": f"✅ Connected to BotArmy Backend via {endpoint} ({test_mode_status})",
                "endpoint": endpoint,
                "test_mode": TEST_MODE
            },
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send_text(json.dumps(welcome_msg))
        logger.info(f"Client {client_id} connected via {endpoint} (TEST_MODE: {TEST_MODE})")
        return client_id
    
    async def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        logger.info(f"Client {client_id} disconnected")
    
    async def send_to_client(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send message to {client_id}: {e}")
    
    async def broadcast_to_all(self, message: dict):
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to broadcast to {client_id}: {e}")

# Create FastAPI app
app = FastAPI(
    title="BotArmy Backend (Simple + Test Mode)",
    version="1.0.0", 
    description="Simplified backend with test mode support"
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
    openai_key_status = "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Missing"
    llm_service_status = "✅ Available" if HAS_LLM_SERVICE else "❌ Not available"
    test_mode_status = "🧪 Enabled" if TEST_MODE else "🔥 Disabled"
    
    return {
        "message": "BotArmy Backend (Simple Mode + Test Mode)",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": "development",
        "websocket_endpoints": ["/api/ws", "/ws"],
        "openai_key": openai_key_status,
        "llm_service": llm_service_status,
        "test_mode": test_mode_status,
        "features": {
            "websockets": True,
            "basic_commands": True,
            "openai_integration": HAS_LLM_SERVICE and bool(os.getenv("OPENAI_API_KEY")),
            "test_mode": TEST_MODE,
            "multiple_endpoints": True
        }
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "connections": len(manager.active_connections),
        "websocket_endpoints": ["/api/ws", "/ws"],
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "llm_service_available": HAS_LLM_SERVICE,
        "test_mode": TEST_MODE
    }

async def test_real_openai(client_id: str, test_message: str = None):
    """Test real OpenAI integration with test mode support"""
    try:
        # Send starting message
        await manager.send_to_client(client_id, {
            "type": "agent_response",
            "agent_name": "System",
            "content": "🧠 Testing OpenAI connection...",
            "timestamp": datetime.now().isoformat()
        })
        
        # TEST MODE: Return simple confirmation
        if TEST_MODE:
            await manager.send_to_client(client_id, {
                "type": "agent_response",
                "agent_name": "OpenAI Test",
                "content": f"""🧪 **OpenAI Test - Test Mode**

✅ **Test Mode Active**: Agents will return role confirmations only
📝 **Test Message**: {test_message[:100]}{'...' if test_message and len(test_message) > 100 else ''}

⚙️ **Status**: OpenAI integration skipped in test mode
🔥 **To enable full OpenAI testing**: Set AGENT_TEST_MODE=false and restart backend

---
*OpenAI test command received and acknowledged.*""",
                "timestamp": datetime.now().isoformat()
            })
            return
            
        if not HAS_LLM_SERVICE:
            await manager.send_to_client(client_id, {
                "type": "agent_response",
                "agent_name": "OpenAI Test",
                "content": "❌ LLM service not available. Check backend dependencies.",
                "timestamp": datetime.now().isoformat()
            })
            return
            
        if not os.getenv("OPENAI_API_KEY"):
            await manager.send_to_client(client_id, {
                "type": "agent_response", 
                "agent_name": "OpenAI Test",
                "content": "❌ OpenAI API key not configured. Add OPENAI_API_KEY to your environment variables.",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        # Get LLM service and make real API call
        llm_service = get_llm_service()
        
        if not test_message:
            test_message = "Hello! This is a test message to verify OpenAI integration. Please respond with a brief confirmation that you received this message."
        
        logger.info(f"Making OpenAI API call for client {client_id}")
        
        # Call the LLM service with correct parameters
        result = await llm_service.generate_response(
            prompt=test_message,
            agent_name="OpenAI Test"
        )
        
        # Send success response
        await manager.send_to_client(client_id, {
            "type": "agent_response",
            "agent_name": "OpenAI Test", 
            "content": f"✅ OpenAI test successful!\n\n📝 Test Message: {test_message}\n\n🤖 OpenAI Response: {result}",
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"OpenAI test successful for client {client_id}")
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"OpenAI test failed for client {client_id}: {error_msg}")
        
        await manager.send_to_client(client_id, {
            "type": "agent_response",
            "agent_name": "System",
            "content": f"❌ OpenAI test failed: {error_msg}\n\nPlease check your OPENAI_API_KEY environment variable and ensure you have sufficient credits.",
            "timestamp": datetime.now().isoformat()
        })

async def handle_simple_command(client_id: str, command: str, data: dict):
    """Handle simple commands with test mode support"""
    
    if command == "ping":
        mode_info = "🧪 Test mode enabled" if TEST_MODE else "🔥 Full mode enabled"
        response = {
            "type": "agent_response",
            "agent_name": "System",
            "content": f"✅ Backend connection successful! Simple mode is working perfectly.\n\n{mode_info}",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_to_client(client_id, response)
        
    elif command == "test_openai":
        test_msg = data.get("message", "Test message")
        asyncio.create_task(test_real_openai(client_id, test_msg))
        
    elif command == "start_project":
        brief = data.get("brief", "No brief provided")
        mode_info = "🧪 Test mode: Agents will return role confirmations" if TEST_MODE else "🔥 Full mode: Real agent processing enabled"
        
        response = {
            "type": "agent_response",
            "agent_name": "System", 
            "content": f"🚀 Project started in simple mode!\n\nBrief: {brief}\n\n{mode_info}\n\n⚠️ Full workflow disabled in simple mode\n✅ Connection and messaging working perfectly!\n\nTo test full workflow, switch to main.py backend.",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_to_client(client_id, response)
        
    else:
        response = {
            "type": "agent_response",
            "agent_name": "System",
            "content": f"⚠️ Unknown command: {command}\n\nAvailable commands: ping, test_openai, start_project",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_to_client(client_id, response)

async def websocket_handler(websocket: WebSocket, endpoint: str):
    """Common WebSocket handler for both endpoints"""
    client_id = await manager.connect(websocket, endpoint)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            logger.info(f"Received from {client_id}: {message}")
            
            msg_type = message.get("type")
            
            if msg_type == "user_command":
                command_data = message.get("data", {})
                command = command_data.get("command")
                await handle_simple_command(client_id, command, command_data)
                
            elif msg_type == "ping":
                # Respond to ping
                pong_response = {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_to_client(client_id, pong_response)
                
            elif msg_type == "batch":
                # Handle batched messages
                messages = message.get("messages", [])
                for msg in messages:
                    if msg.get("type") == "user_command":
                        command_data = msg.get("data", {})
                        command = command_data.get("command")
                        await handle_simple_command(client_id, command, command_data)
                
            else:
                logger.warning(f"Unknown message type: {msg_type}")
                response = {
                    "type": "agent_response",
                    "agent_name": "System",
                    "content": f"⚠️ Unknown message type: {msg_type}",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_to_client(client_id, response)
                
    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected normally")
    except Exception as e:
        logger.error(f"Error for client {client_id}: {e}")
    finally:
        await manager.disconnect(client_id)

@app.websocket("/api/ws")
async def websocket_endpoint_api(websocket: WebSocket):
    """WebSocket endpoint at /api/ws (preferred)"""
    await websocket_handler(websocket, "/api/ws")

@app.websocket("/ws")
async def websocket_endpoint_root(websocket: WebSocket):
    """WebSocket endpoint at /ws (fallback)"""
    await websocket_handler(websocket, "/ws")

if __name__ == "__main__":
    print("🚀 Starting BotArmy Backend (Simple Mode + Test Mode)...")
    print("This version includes test mode support for agent workflow testing")
    print("=" * 70)
    
    # Check environment
    openai_key = os.getenv("OPENAI_API_KEY")
    test_mode = os.getenv("AGENT_TEST_MODE", "false").lower() == "true"
    
    print(f"OpenAI API Key: {'✅ Configured' if openai_key else '❌ Missing (add OPENAI_API_KEY to .env.local)'}")
    print(f"LLM Service: {'✅ Available' if HAS_LLM_SERVICE else '❌ Import failed'}")
    print(f"Test Mode: {'🧪 ENABLED - Agents return role confirmations only' if test_mode else '🔥 DISABLED - Full LLM processing'}")
    
    if test_mode:
        print("\n🧪 TEST MODE ACTIVE:")
        print("  - Agents will return simple role confirmations")
        print("  - No real LLM processing (saves tokens)")
        print("  - Perfect for testing workflow and UI")
        print("  - Set AGENT_TEST_MODE=false to disable")
    
    # Use environment PORT or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    print(f"\nStarting server on http://localhost:{port}")
    print(f"WebSocket endpoints:")
    print(f"  - ws://localhost:{port}/api/ws (preferred)")
    print(f"  - ws://localhost:{port}/ws (fallback)")
    print("=" * 70)
    
    uvicorn.run(
        "main_simple:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True,
        log_level="info"
    )
