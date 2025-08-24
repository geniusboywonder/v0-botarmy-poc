#!/bin/bash

# BotArmy Integration Issue Fix Script
echo "🔧 BotArmy Integration Issue Fix"
echo "==============================="
echo "Date: $(date)"
echo

echo "📊 Issues to Fix:"
echo "1. OpenAI provider argument error"  
echo "2. WebSocket connection stability"
echo "3. CORS configuration optimization"
echo

# Step 1: Backup current main.py
echo "💾 Step 1: Backing up current main.py..."
cp backend/main.py backend/main_backup_$(date +%Y%m%d_%H%M%S).py
echo "✅ Backup created"
echo

# Step 2: Apply the fixed version
echo "🔄 Step 2: Applying fixes..."
cp backend/main_fixed.py backend/main.py

if [ $? -eq 0 ]; then
    echo "✅ Fixed main.py applied successfully"
else
    echo "❌ Failed to apply fixes"
    exit 1
fi

echo

# Step 3: Verify the fixes
echo "🔍 Step 3: Verifying fixes..."

# Check if the OpenAI fix is in place
if grep -q "preferred_provider=" backend/main.py; then
    echo "✅ OpenAI provider argument fix verified"
else
    echo "⚠️ OpenAI fix may not be applied correctly"
fi

# Check if CORS improvements are in place  
if grep -q "allow_credentials=False" backend/main.py; then
    echo "✅ CORS WebSocket optimization verified"
else
    echo "⚠️ CORS optimization may not be applied correctly"  
fi

# Check if WebSocket welcome message is added
if grep -q "WebSocket connection established" backend/main.py; then
    echo "✅ WebSocket stability improvements verified"
else
    echo "⚠️ WebSocket improvements may not be applied correctly"
fi

echo

# Step 4: Environment check
echo "🔧 Step 4: Environment check..."

# Check if TEST_MODE is still enabled
if grep -q "TEST_MODE=true" .env; then
    echo "✅ Safety brakes still engaged (TEST_MODE=true)"
else
    echo "⚠️ Check TEST_MODE setting in .env file"
fi

# Check WebSocket URL consistency
WS_URL_1=$(grep "NEXT_PUBLIC_WEBSOCKET_URL=" .env | cut -d'=' -f2)
WS_URL_2=$(grep "NEXT_PUBLIC_WEBSOCKET_URL=" .env.local | cut -d'=' -f2)

if [ "$WS_URL_1" = "$WS_URL_2" ]; then
    echo "✅ WebSocket URLs consistent between .env files"
else
    echo "⚠️ WebSocket URL mismatch between .env files"
fi

echo

# Step 5: Restart instructions
echo "🚀 Step 5: Restart Instructions"
echo "================================"
echo
echo "To apply the fixes:"
echo "1. Stop the backend server (Ctrl+C)"
echo "2. Restart with: python backend/main.py"  
echo "3. The frontend should reconnect automatically"
echo
echo "Expected results after restart:"
echo "✅ OpenAI test should work without 'unexpected keyword' error"
echo "✅ WebSocket connections should be more stable"
echo "✅ Backend should send welcome message on connection"
echo "✅ CORS should be optimized for WebSocket stability"
echo

echo "🎯 Next steps:"
echo "1. Restart backend server"
echo "2. Test WebSocket connection from frontend"
echo "3. Try OpenAI test - should work without errors"
echo "4. Verify agent workflow functionality"

echo
echo "🔧 Fix script complete!"
