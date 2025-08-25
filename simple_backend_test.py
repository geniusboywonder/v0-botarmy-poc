#!/usr/bin/env python3
"""
Simplified Backend Import Test
Tests just the critical imports to verify Jules' backend works
"""
import sys
import os
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Load environment with brakes
from dotenv import load_dotenv
load_dotenv()

print("🧪 Simplified Backend Import Test")
print("=" * 40)
print(f"🛡️ AGENT_TEST_MODE: {os.getenv('AGENT_TEST_MODE')}")
print(f"🛡️ TEST_MODE: {os.getenv('TEST_MODE')}")
print("=" * 40)

results = []

# Test 1: FastAPI
try:
    from fastapi import FastAPI, WebSocket
    results.append("✅ FastAPI - Core web framework")
except Exception as e:
    results.append(f"❌ FastAPI - {e}")

# Test 2: Runtime Environment
try:
    from backend.runtime_env import IS_REPLIT
    results.append("✅ Runtime Environment - Platform detection")
except Exception as e:
    results.append(f"❌ Runtime Environment - {e}")

# Test 3: Connection Manager
try:
    from backend.connection_manager import EnhancedConnectionManager
    results.append("✅ Connection Manager - WebSocket handling")
except Exception as e:
    results.append(f"❌ Connection Manager - {e}")

# Test 4: Agent Status Broadcaster
try:
    from backend.agent_status_broadcaster import AgentStatusBroadcaster
    results.append("✅ Status Broadcaster - Real-time updates")
except Exception as e:
    results.append(f"❌ Status Broadcaster - {e}")

# Test 5: LLM Service
try:
    from backend.services.llm_service import get_llm_service
    results.append("✅ LLM Service - Multi-provider support")
except Exception as e:
    results.append(f"❌ LLM Service - {e}")

# Test 6: Base Agent
try:
    from backend.agents.base_agent import BaseAgent
    results.append("✅ Base Agent - Agent foundation")
except Exception as e:
    results.append(f"❌ Base Agent - {e}")

# Test 7: AGUI Protocol
try:
    from backend.agui.protocol import agui_handler
    results.append("✅ AGUI Protocol - Message handling")
except Exception as e:
    results.append(f"❌ AGUI Protocol - {e}")

# Test 8: Workflow
try:
    from backend.workflow import botarmy_workflow
    results.append("✅ Workflow - Agent orchestration")
except Exception as e:
    results.append(f"❌ Workflow - {e}")

# Test 9: Simple Backend
try:
    from backend.main_simple import app
    results.append("✅ Simple Backend - Testing application")
except Exception as e:
    results.append(f"❌ Simple Backend - {e}")

# Test 10: Full Backend
try:
    from backend.main import app
    results.append("✅ Full Backend - Production application")
except Exception as e:
    results.append(f"❌ Full Backend - {e}")

# Results
print("\nResults:")
for result in results:
    print(result)

passed = sum(1 for r in results if r.startswith("✅"))
total = len(results)
rate = (passed/total)*100

print(f"\nSummary: {passed}/{total} passed ({rate:.1f}%)")

if rate >= 90:
    print("🎉 OUTSTANDING - Jules' backend is excellent!")
elif rate >= 75:
    print("✅ EXCELLENT - Jules' backend is solid!")
elif rate >= 60:
    print("⚠️ GOOD - Jules' backend mostly works")
else:
    print("❌ ISSUES - Backend needs attention")

print("=" * 40)
