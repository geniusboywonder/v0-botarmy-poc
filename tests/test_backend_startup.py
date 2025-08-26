#!/usr/bin/env python3
"""
Backend Testing Script - Phase 1
Tests backend startup and identifies issues
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all backend imports to identify missing dependencies"""
    print("🧪 Testing Backend Imports...")

    import_tests = [
        ("dotenv", "from dotenv import load_dotenv"),
        ("fastapi", "from fastapi import FastAPI"),
        ("uvicorn", "import uvicorn"),
        ("backend.runtime_env", "from backend.runtime_env import IS_REPLIT, get_environment_info"),
        ("backend.agui.protocol", "from backend.agui.protocol import agui_handler"),
        ("backend.artifacts", "from backend.artifacts import get_artifacts_structure"),
        ("backend.bridge", "from backend.bridge import AGUI_Handler"),
        ("backend.connection_manager", "from backend.connection_manager import EnhancedConnectionManager"),
        ("backend.error_handler", "from backend.error_handler import ErrorHandler"),
        ("backend.agent_status_broadcaster", "from backend.agent_status_broadcaster import AgentStatusBroadcaster"),
        ("backend.workflow", "from backend.workflow import botarmy_workflow, simple_workflow"),
        ("backend.human_input_handler", "from backend.human_input_handler import request_human_approval"),
    ]

    results = {}

    for module_name, import_statement in import_tests:
        try:
            exec(import_statement)
            results[module_name] = "✅ Success"
            print(f"  ✅ {module_name}")
        except ImportError as e:
            results[module_name] = f"❌ ImportError: {e}"
            print(f"  ❌ {module_name}: {e}")
        except Exception as e:
            results[module_name] = f"❌ Error: {e}"
            print(f"  ❌ {module_name}: {e}")

    return results

def test_environment_setup():
    """Test environment variables and configuration"""
    print("\n🔧 Testing Environment Setup...")

    # Load environment
    from dotenv import load_dotenv
    load_dotenv()

    env_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "AGENT_TEST_MODE": os.getenv("AGENT_TEST_MODE", "false"),
        "ENABLE_HITL": os.getenv("ENABLE_HITL", "true"),
        "AUTO_ACTION": os.getenv("AUTO_ACTION", "none"),
    }

    for var_name, var_value in env_vars.items():
        if var_value:
            if "API_KEY" in var_name:
                print(f"  ✅ {var_name}: {'*' * 8}...{var_value[-4:] if len(var_value) > 4 else '***'}")
            else:
                print(f"  ✅ {var_name}: {var_value}")
        else:
            print(f"  ⚠️  {var_name}: Not set")

    return env_vars

def test_basic_functionality():
    """Test basic backend functionality"""
    print("\n⚙️ Testing Basic Backend Functionality...")

    try:
        # Test environment detection
        from backend.runtime_env import IS_REPLIT, get_environment_info
        env_info = get_environment_info()
        print(f"  ✅ Environment: {'Replit' if IS_REPLIT else 'Development'}")
        print(f"  ✅ Environment Info: {env_info}")

        # Test AGUI handler
        from backend.agui.protocol import agui_handler
        test_message = agui_handler.create_agent_message(
            content="Test message",
            agent_name="Test",
            session_id="test_session"
        )
        print(f"  ✅ AGUI Handler: Message created")

        # Test status broadcaster
        from backend.agent_status_broadcaster import AgentStatusBroadcaster
        broadcaster = AgentStatusBroadcaster()
        print(f"  ✅ Status Broadcaster: Initialized")

        # Test workflow import
        from backend.workflow import botarmy_workflow
        print(f"  ✅ Workflow: Imported successfully")

        return True

    except Exception as e:
        print(f"  ❌ Basic functionality test failed: {e}")
        import traceback
        print(f"  📋 Traceback: {traceback.format_exc()}")
        return False

def main():
    print("🚀 BotArmy Backend Testing - Phase 1")
    print("=" * 50)

    # Test imports
    import_results = test_imports()

    # Test environment
    env_results = test_environment_setup()

    # Test basic functionality
    basic_test_result = test_basic_functionality()

    # Summary
    print("\n📊 Test Summary:")
    print("=" * 30)

    failed_imports = [k for k, v in import_results.items() if not v.startswith("✅")]
    if failed_imports:
        print(f"❌ Failed Imports: {len(failed_imports)}")
        for module in failed_imports:
            print(f"  - {module}")
    else:
        print("✅ All imports successful")

    missing_env = [k for k, v in env_results.items() if not v and "API_KEY" in k]
    if missing_env:
        print(f"⚠️  Missing API Keys: {missing_env}")
    else:
        print("✅ API Keys configured")

    if basic_test_result:
        print("✅ Basic functionality working")
    else:
        print("❌ Basic functionality has issues")

    # Overall status
    all_imports_ok = len(failed_imports) == 0
    basic_ok = basic_test_result

    if all_imports_ok and basic_ok:
        print("\n🎉 Backend Status: READY FOR STARTUP")
        return True
    else:
        print("\n🚨 Backend Status: NEEDS FIXES")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
