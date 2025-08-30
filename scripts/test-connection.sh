#!/bin/bash
# Test Frontend & Backend Connection Script

echo "🔍 BotArmy Connection Test"
echo "=========================="

# Check if frontend is running
echo "📱 Checking frontend (port 3000)..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running on http://localhost:3000"
else
    echo "❌ Frontend not running. Start with: npm run dev"
fi

echo ""

# Check if backend is running  
echo "🔗 Checking backend (port 8000)..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running on http://localhost:8000"
    echo "🌐 WebSocket should connect to ws://localhost:8000/api/ws"
elif curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "⚠️  Backend responding but /health endpoint not found"
    echo "🌐 WebSocket will try ws://localhost:8000/api/ws"
else
    echo "❌ Backend not running. Start with: python start_backend.py"
    echo "ℹ️  Frontend will work in demo-only mode (no real-time features)"
fi

echo ""

# WebSocket test
echo "🔌 Testing WebSocket connection..."
if command -v wscat > /dev/null 2>&1; then
    timeout 5 wscat -c ws://localhost:8000/api/ws 2>&1 | head -1
else
    echo "ℹ️  Install wscat to test WebSocket: npm install -g wscat"
fi

echo ""
echo "🎯 Summary:"
echo "- Frontend should show all 5 SDLC stages in dashboard"
echo "- Stage pages should show tasks and artifacts" 
echo "- WebSocket errors are normal if backend not running"
echo "- Demo data works independently of backend"
