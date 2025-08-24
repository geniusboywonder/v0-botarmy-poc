#!/usr/bin/env python3
"""
Simple backend test to diagnose connection issues
"""

import sys
import os
import traceback
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test if all imports work"""
    print("🔍 Testing imports...")
    
    try:
        print("  ✓ Testing basic imports...")
        import uvicorn
        from fastapi import FastAPI
        print("    ✓ FastAPI/Uvicorn imported successfully")
        
        print("  ✓ Testing environment detection...")
        from backend.runtime_env import IS_REPLIT, get_environment_info
        print(f"    ✓ Runtime environment: {'Replit' if IS_REPLIT else 'Development'}")
        
        print("  ✓ Testing core modules...")
        from backend.agui.protocol import agui_handler
        print("    ✓ AGUI protocol imported")
        
        from backend.connection_manager import EnhancedConnectionManager
        print("    ✓ Connection manager imported")
        
        print("  ✓ Testing LLM service...")
        from backend.services.llm_service import get_llm_service
        print("    ✓ LLM service imported")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_basic_server():
    """Test basic FastAPI server"""
    print("\n🚀 Testing basic server...")
    
    try:
        from fastapi import FastAPI
        app = FastAPI()
        
        @app.get("/test")
        def test_endpoint():
            return {"status": "working"}
        
        print("    ✓ Basic FastAPI app created")
        return True
        
    except Exception as e:
        print(f"    ❌ Server test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 BotArmy Backend Diagnostic Test")
    print("=" * 50)
    
    # Test 1: Imports
    imports_ok = test_imports()
    
    # Test 2: Basic server
    server_ok = test_basic_server()
    
    # Summary
    print("\n📊 Test Summary:")
    print(f"  Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"  Server:  {'✅ PASS' if server_ok else '❌ FAIL'}")
    
    if imports_ok and server_ok:
        print("\n✅ Backend dependencies are working!")
        print("💡 Try running: python backend/main.py")
    else:
        print("\n❌ Backend has issues that need to be fixed")
        print("💡 Check the error messages above")

if __name__ == "__main__":
    main()
