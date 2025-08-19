import asyncio
import json
import logging
import os
from typing import Dict, List
import uuid

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error sending message to client: {e}")

manager = ConnectionManager()

# --- FastAPI App ---
app = FastAPI(title="BotArmy Backend v2 - Simplified")
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "BotArmy Backend v2 is running"}

async def handle_websocket_message(websocket: WebSocket, message: dict):
    """Handles incoming messages from the UI."""
    try:
        msg_type = message.get("type")
        session_id = message.get("session_id", "global_session")
        
        logger.info(f"Received message: {message}")

        if msg_type == "user_command":
            command_data = message.get("data", {})
            command = command_data.get("command")
            
            if command == "ping":
                # Test backend connection
                response = create_message(
                    content="✅ Backend connection successful! Server is running on port 8000.",
                    agent_name="System",
                    session_id=session_id
                )
                await manager.broadcast(json.dumps(response))
                
            elif command == "test_openai":
                # Test OpenAI API connection
                try:
                    # Check if API key is set
                    api_key = os.getenv("OPENAI_API_KEY")
                    if not api_key:
                        response = create_error_message(
                            error="❌ OpenAI API key not found. Set OPENAI_API_KEY environment variable.",
                            session_id=session_id
                        )
                    else:
                        try:
                            import openai
                            # Test API call
                            client = openai.OpenAI(api_key=api_key)
                            test_response = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[{"role": "user", "content": "Say 'OpenAI connection test successful'"}],
                                max_tokens=20
                            )
                            response = create_message(
                                content=f"✅ OpenAI API test successful! Response: {test_response.choices[0].message.content}",
                                agent_name="System",
                                session_id=session_id
                            )
                        except ImportError:
                            response = create_error_message(
                                error="❌ OpenAI package not installed. Run: pip install openai",
                                session_id=session_id
                            )
                        except Exception as e:
                            response = create_error_message(
                                error=f"❌ OpenAI API test failed: {str(e)}",
                                session_id=session_id
                            )
                            
                    await manager.broadcast(json.dumps(response))
                except Exception as e:
                    response = create_error_message(
                        error=f"❌ Unexpected error during OpenAI test: {str(e)}",
                        session_id=session_id
                    )
                    await manager.broadcast(json.dumps(response))
            
            elif command == "start_project":
                project_brief = command_data.get("brief", "No brief provided.")
                response = create_message(
                    content=f"🚀 Project started: {project_brief[:100]}... (This is a simplified version - full workflow not implemented yet)",
                    agent_name="System",
                    session_id=session_id
                )
                await manager.broadcast(json.dumps(response))
            else:
                logger.warning(f"Unknown user command: {command}")
        elif msg_type == "artifacts_get_all":
            # Handle artifacts request
            response = create_message(
                content="No artifacts available in simplified version.",
                agent_name="System",
                session_id=session_id
            )
            await manager.broadcast(json.dumps(response))
        else:
            logger.warning(f"Unknown message type received: {msg_type}")
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        error_response = create_error_message(
            error=f"Message handling error: {str(e)}",
            session_id=session_id
        )
        await manager.broadcast(json.dumps(error_response))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                await handle_websocket_message(websocket, message)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                error_response = create_error_message(f"Invalid JSON: {str(e)}")
                await websocket.send_text(json.dumps(error_response))
            except Exception as e:
                logger.error(f"Message handling error: {e}")
                error_response = create_error_message(f"Error: {str(e)}")
                await websocket.send_text(json.dumps(error_response))
    except WebSocketDisconnect:
        logger.info("Client disconnected gracefully.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)

if __name__ == "__main__":
    print("🚀 Starting BotArmy Backend v2 (Simplified)")
    print("📍 Server will be available at: http://localhost:8000")
    print("🔌 WebSocket endpoint: ws://localhost:8000/ws")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
