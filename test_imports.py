#!/usr/bin/env python3
"""
Test script to verify all imports work without circular dependencies.
Run this before starting the backend to catch import issues early.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all critical imports to catch circular dependencies."""
    print("🧪 Testing imports...")
    
    try:
        print("   Testing basic imports...")
        import controlflow as cf
        print("   ✅ ControlFlow imported")
        
        from backend.agui.protocol import agui_handler
        print("   ✅ AG-UI protocol imported")
        
        from backend.connection_manager import EnhancedConnectionManager
        print("   ✅ Connection manager imported")
        
        from backend.agent_status_broadcaster import AgentStatusBroadcaster
        print("   ✅ Status broadcaster imported")
        
        from backend.heartbeat_monitor import HeartbeatMonitor
        print("   ✅ Heartbeat monitor imported")
        
        from backend.error_handler import ErrorHandler
        print("   ✅ Error handler imported")
        
        from backend.bridge import AGUI_Handler
        print("   ✅ Bridge imported")
        
        from backend.workflow import botarmy_workflow
        print("   ✅ Workflow imported")
        
        # Test the main app import last
        from backend.main import app
        print("   ✅ Main app imported")
        
        print("")
        print("🎉 All imports successful! No circular dependencies detected.")
        print("")
        print("✅ Ready to start backend:")
        print("   python start_backend.py")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        print("")
        print("💡 Possible fixes:")
        print("   1. Run: ./clean_cache.sh")
        print("   2. Check for circular imports")
        print("   3. Verify all files exist")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
