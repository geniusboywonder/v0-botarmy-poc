#!/usr/bin/env python3
"""
WebSocket Test Script for Replit
Run this in Replit shell to test WebSocket connectivity
"""

import asyncio
import websockets
import json
import os
import sys

async def test_websocket():
    """Test WebSocket connection to BotArmy backend"""
    
    # Get the PORT that Replit sets
    port = os.getenv('PORT', '8000')
    
    # Test URLs
    local_url = f"ws://localhost:{port}/api/ws"
    
    print("🔌 Testing WebSocket Connection")
    print("=" * 50)
    print(f"Port: {port}")
    print(f"Testing URL: {local_url}")
    print("=" * 50)
    
    try:
        print("⏳ Attempting connection...")
        
        # Try to connect with a timeout
        async with websockets.connect(local_url, timeout=10) as websocket:
            print("✅ WebSocket connection successful!")
            
            # Send a test message
            test_message = {
                "type": "user_command",
                "data": {
                    "command": "ping"
                },
                "timestamp": "2025-01-01T00:00:00Z",
                "session_id": "test_session"
            }
            
            print("📤 Sending test message...")
            await websocket.send(json.dumps(test_message))
            
            # Wait for response with timeout
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                print("📥 Received response:")
                print(json.dumps(json.loads(response), indent=2))
                print("✅ WebSocket communication working!")
                
            except asyncio.TimeoutError:
                print("⚠️ No response received within 5 seconds")
                print("   Backend may be processing but WebSocket is connected")
                
    except ConnectionRefusedError:
        print("❌ Connection refused!")
        print("   → Backend is not running or not listening on the expected port")
        print(f"   → Check if uvicorn is running on port {port}")
        
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Additional diagnostics
        if "connection failed" in str(e).lower():
            print("   → This usually means the backend is not accessible")
        elif "handshake" in str(e).lower():
            print("   → WebSocket handshake failed - check CORS or endpoint")

async def check_backend_health():
    """Check if backend HTTP endpoints are working"""
    import aiohttp
    
    port = os.getenv('PORT', '8000')
    base_url = f"http://localhost:{port}"
    
    print("\n🏥 Testing Backend Health")
    print("=" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test health endpoint
            async with session.get(f"{base_url}/health", timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Health endpoint working")
                    print(f"   Environment: {data.get('environment', 'unknown')}")
                    print(f"   Port: {data.get('port', 'unknown')}")
                else:
                    print(f"⚠️ Health endpoint returned status {response.status}")
                    
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        print("   → Backend may not be running")

def check_process():
    """Check if uvicorn process is running"""
    import subprocess
    
    print("\n🔍 Checking Running Processes")
    print("=" * 50)
    
    try:
        # Check for uvicorn process
        result = subprocess.run(['pgrep', '-f', 'uvicorn'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"✅ Found {len(pids)} uvicorn process(es)")
            for pid in pids:
                if pid:
                    print(f"   PID: {pid}")
        else:
            print("❌ No uvicorn processes found")
            print("   → Backend may not be running")
            
    except Exception as e:
        print(f"⚠️ Could not check processes: {e}")

async def main():
    """Main test function"""
    print("🤖 BotArmy WebSocket Diagnostic Tool")
    print("=" * 60)
    
    # Check if backend is running
    check_process()
    
    # Test HTTP health endpoint
    await check_backend_health()
    
    # Test WebSocket connection
    await test_websocket()
    
    print("\n" + "=" * 60)
    print("🎯 Diagnostic Complete")
    
    # Provide next steps
    print("\n💡 Next Steps:")
    print("   1. If backend is not running:")
    print("      → cd backend && python main.py")
    print("   2. If health check fails:")
    print("      → Check for errors in backend startup")
    print("   3. If WebSocket fails but health works:")
    print("      → Check frontend WebSocket URL construction")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)