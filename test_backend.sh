#!/bin/bash

echo "=== BotArmy Server Testing Script ==="
echo "Date: $(date)"

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "=== Testing Backend Server (Python FastAPI) ==="
echo "Activating virtual environment..."

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
    echo "Python version: $(python --version)"
    echo "pip version: $(pip --version)"
    
    echo "Starting backend server..."
    echo "Command: python start_backend.py"
    echo "Expected: Server should start on http://localhost:8000"
    echo "Expected: WebSocket should be available at ws://localhost:8000/ws"
    echo ""
    echo "Press Ctrl+C to stop the server and continue with frontend testing"
    echo ""
    
    # Start the backend server
    python start_backend.py
else
    echo "❌ Virtual environment not found. Please create venv first:"
    echo "python -m venv venv"
    echo "source venv/bin/activate"
    echo "pip install -r requirements.txt"
fi
