#!/bin/bash

# WebSocket Connection Debugger
echo "🔍 BotArmy WebSocket Connection Debugger"
echo "======================================="

# Test if backend is running
echo "1. Testing backend HTTP connection..."
if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ Backend HTTP is responding"
    
    # Get the response
    response=$(curl -s http://localhost:8000)
    echo "   Response: $response"
else
    echo "❌ Backend HTTP is not responding"
    echo "💡 Make sure backend is running: python start_backend.py"
    exit 1
fi

echo ""
echo "2. Testing WebSocket connection..."

# Install wscat if not available (optional)
if command -v wscat &> /dev/null; then
    echo "   Using wscat to test WebSocket..."
    echo "   Connecting to ws://localhost:8000/ws"
    echo "   (This will timeout after 5 seconds - that's expected)"
    
    # Test WebSocket connection with timeout
    timeout 5s wscat -c ws://localhost:8000/ws -x '{"type":"user_command","data":{"command":"ping"},"timestamp":"'$(date -Iseconds)'","session_id":"test"}' || true
    
else
    echo "   ⚠️ wscat not available (npm install -g wscat to install)"
    echo "   Checking if WebSocket port is listening..."
    
    if lsof -i :8000 > /dev/null 2>&1; then
        echo "   ✅ Port 8000 is listening"
    else
        echo "   ❌ Port 8000 is not listening"
    fi
fi

echo ""
echo "3. Checking environment variables..."

# Check .env file
if [ -f ".env" ]; then
    echo "✅ .env file exists"
    
    if grep -q "OPENAI_API_KEY=sk-" .env; then
        echo "✅ OpenAI API key appears to be set"
    else
        echo "❌ OpenAI API key not properly configured"
    fi
    
    if grep -q "NEXT_PUBLIC_WEBSOCKET_URL" .env; then
        websocket_url=$(grep "NEXT_PUBLIC_WEBSOCKET_URL" .env | cut -d'=' -f2)
        echo "✅ WebSocket URL configured: $websocket_url"
    else
        echo "⚠️  NEXT_PUBLIC_WEBSOCKET_URL not set (will use defaults)"
    fi
else
    echo "❌ .env file not found"
fi

echo ""
echo "4. Process check..."

# Check if processes are running
if pgrep -f "python.*start_backend.py\|python.*main.py" > /dev/null; then
    echo "✅ Backend process is running"
else
    echo "❌ Backend process not found"
fi

if pgrep -f "next-server\|npm.*dev\|pnpm.*dev" > /dev/null; then
    echo "✅ Frontend process is running"
else
    echo "⚠️  Frontend process not found"
fi

echo ""
echo "🔧 Troubleshooting Tips:"
echo "1. Make sure backend is running: python start_backend.py"
echo "2. Make sure frontend is running: pnpm dev"  
echo "3. Check browser console for WebSocket errors"
echo "4. Verify OpenAI API key is valid"
echo "5. Try clicking 'Test Backend' button in the UI"

echo ""
echo "📍 URLs to test:"
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   WebSocket: ws://localhost:8000/ws"
