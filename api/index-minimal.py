# Lightweight Vercel Serverless Function Entrypoint
import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

# Add project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Create a minimal FastAPI app for Vercel
app = FastAPI(title="BotArmy API - Vercel", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "BotArmy API is running on Vercel"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "platform": "vercel"}

# Minimal agent status endpoint
@app.get("/api/agent-status")
async def get_agent_status():
    return {
        "agents": [],
        "total_agents": 0,
        "active_agents": 0,
        "message": "Minimal API - Full functionality available in local development"
    }

# Basic workflow endpoint
@app.post("/api/workflow/start")
async def start_workflow(request: dict):
    return {
        "status": "not_implemented",
        "message": "Workflow functionality requires local development environment",
        "request_received": True
    }

# Health check for the serverless function
@app.get("/api/ping")
async def ping():
    return {"pong": True, "timestamp": "2025-08-21"}

# Export the app for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
