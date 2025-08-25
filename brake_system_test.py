#!/usr/bin/env python3
"""
Agent Brake System Verification Test
Verifies that the safety brakes prevent LLM calls
"""
import sys
import os
import asyncio
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Load environment with brakes
from dotenv import load_dotenv
load_dotenv()

print("🛡️ Agent Brake System Verification")
print("=" * 45)
print(f"AGENT_TEST_MODE: {os.getenv('AGENT_TEST_MODE')}")
print(f"TEST_MODE: {os.getenv('TEST_MODE')}")
print("=" * 45)

async def test_agent_brakes():
    """Test that agent brakes prevent LLM calls"""

    try:
        from backend.agents.base_agent import BaseAgent

        # Check if test mode is active
        test_mode_active = BaseAgent.is_test_mode()
        print(f"🧪 Test Mode Active: {test_mode_active}")

        if not test_mode_active:
            print("❌ WARNING: Test mode is NOT active - agents may make real LLM calls!")
            return False

        # Create a test agent
        test_agent = BaseAgent("You are a test agent to verify the brake system works.")
        print("✅ BaseAgent created successfully")

        # Execute a test task - this should NOT make an LLM call
        print("🧪 Testing agent execution with brakes engaged...")
        result = await test_agent.execute(
            "Please write a comprehensive business plan for a new startup",
            "BrakeTestAgent",
            "brake_test_session"
        )

        # Verify it's a test mode response
        is_test_response = "Test Mode" in result
        is_role_confirmed = "Role Confirmed" in result
        contains_brake_info = "TEST_MODE" in result or "test mode" in result.lower()

        print(f"✅ Agent execution completed")
        print(f"📝 Response type: {'Test Mode Response' if is_test_response else 'Unexpected Response'}")
        print(f"🎯 Role confirmation: {'Yes' if is_role_confirmed else 'No'}")
        print(f"🛡️ Brake info included: {'Yes' if contains_brake_info else 'No'}")

        # Show a preview of the response
        print(f"📄 Response preview (first 200 chars):")
        print(f"   {result[:200]}{'...' if len(result) > 200 else ''}")

        # Verify it's safe
        safe_response = is_test_response and is_role_confirmed and contains_brake_info

        if safe_response:
            print("🎉 SUCCESS: Brakes working perfectly - NO LLM calls made!")
            print("💰 Cost: $0.00 - No tokens consumed")
            return True
        else:
            print("⚠️ WARNING: Response doesn't look like expected test mode response")
            return False

    except Exception as e:
        print(f"❌ Error testing agent brakes: {e}")
        return False

async def test_llm_service_brakes():
    """Test that LLM service brakes prevent API calls"""

    try:
        from backend.services.llm_service import get_llm_service

        llm_service = get_llm_service()
        print(f"✅ LLM Service created")

        # Check if test mode is active
        test_mode_active = llm_service.is_test_mode
        print(f"🧪 LLM Service Test Mode: {test_mode_active}")

        if not test_mode_active:
            print("❌ WARNING: LLM Service test mode is NOT active!")
            return False

        # Try to generate a response - this should return a mock
        print("🧪 Testing LLM service with brakes engaged...")
        result = await llm_service.generate_response(
            "Write a detailed technical specification",
            "BrakeLLMTestAgent"
        )

        # Should be a mock response
        is_mock = "Mocked LLM Result" in result
        print(f"📝 Response: {result}")
        print(f"🛡️ Mock response: {'Yes' if is_mock else 'No'}")

        if is_mock:
            print("🎉 SUCCESS: LLM Service brakes working - NO API calls made!")
            return True
        else:
            print("⚠️ WARNING: LLM Service may have made real API call")
            return False

    except Exception as e:
        print(f"❌ Error testing LLM service brakes: {e}")
        return False

async def main():
    """Run all brake system tests"""

    print("🧪 Starting Brake System Verification Tests...")
    print("")

    # Test 1: Agent Brakes
    print("Test 1: BaseAgent Brake System")
    print("-" * 35)
    agent_brakes_ok = await test_agent_brakes()

    print("\n" + "-" * 45 + "\n")

    # Test 2: LLM Service Brakes
    print("Test 2: LLM Service Brake System")
    print("-" * 37)
    llm_brakes_ok = await test_llm_service_brakes()

    print("\n" + "=" * 45)
    print("🛡️ BRAKE SYSTEM TEST SUMMARY")
    print("=" * 45)

    print(f"BaseAgent Brakes: {'✅ WORKING' if agent_brakes_ok else '❌ FAILED'}")
    print(f"LLM Service Brakes: {'✅ WORKING' if llm_brakes_ok else '❌ FAILED'}")

    all_brakes_working = agent_brakes_ok and llm_brakes_ok

    if all_brakes_working:
        print("\n🎉 ALL BRAKES WORKING PERFECTLY!")
        print("✅ Safe to proceed with testing")
        print("💰 Zero API costs - No LLM calls made")
        print("🛡️ Maximum safety level achieved")
    else:
        print("\n❌ BRAKE SYSTEM ISSUES DETECTED!")
        print("⚠️ NOT safe to proceed - fix brake issues first")
        print("💸 Risk of unexpected API costs")

    return all_brakes_working

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
