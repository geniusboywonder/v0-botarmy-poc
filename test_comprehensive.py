#!/usr/bin/env python3

"""
Comprehensive testing script for BotArmy Enhanced HITL Integration.
Tests WebSocket connectivity, agent functionality, and HITL workflows.
"""

import asyncio
import json
import logging
import websockets
import time
import sys
import os
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BotArmyTester:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.ws_url = f'ws://{host}:{port}/api/ws'
        self.websocket = None
        self.messages_received = []
        self.test_results = {}

    async def connect(self):
        """Establish WebSocket connection"""
        try:
            logger.info(f"Connecting to {self.ws_url}")
            self.websocket = await websockets.connect(self.ws_url)
            logger.info("✅ WebSocket connection established")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect: {e}")
            return False

    async def send_message(self, message_type, data, timeout=5):
        """Send a message and wait for response"""
        if not self.websocket:
            logger.error("No WebSocket connection")
            return False

        message = {
            "type": message_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "session_id": "test_session"
        }

        try:
            logger.info(f"📤 Sending: {message}")
            await self.websocket.send(json.dumps(message))

            # Wait for response
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    response = await asyncio.wait_for(self.websocket.recv(), timeout=1)
                    parsed_response = json.loads(response)
                    self.messages_received.append(parsed_response)
                    logger.info(f"📥 Received: {parsed_response}")
                    return True
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"Error receiving message: {e}")
                    return False

            logger.warning(f"⏰ No response received within {timeout} seconds")
            return False

        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False

    async def test_basic_connectivity(self):
        """Test basic WebSocket connectivity"""
        logger.info("🧪 Testing basic connectivity...")

        success = await self.send_message(
            "user_command",
            {"command": "ping"}
        )

        self.test_results["basic_connectivity"] = success
        return success

    async def test_openai_integration(self):
        """Test OpenAI API integration"""
        logger.info("🧪 Testing OpenAI integration...")

        success = await self.send_message(
            "user_command",
            {
                "command": "test_openai",
                "message": "Hello! This is a test message. Please confirm you can receive and process this."
            },
            timeout=30  # OpenAI calls might take longer
        )

        self.test_results["openai_integration"] = success
        return success

    async def test_agent_workflow(self):
        """Test starting an agent workflow"""
        logger.info("🧪 Testing agent workflow...")

        success = await self.send_message(
            "user_command",
            {
                "command": "start_project",
                "brief": "Create a simple Python function that adds two numbers and returns the result. Include basic error handling."
            },
            timeout=60  # Workflows might take longer
        )

        self.test_results["agent_workflow"] = success
        return success

    async def listen_for_messages(self, duration=10):
        """Listen for incoming messages for a specified duration"""
        logger.info(f"👂 Listening for messages for {duration} seconds...")

        start_time = time.time()
        message_count = 0

        while time.time() - start_time < duration:
            try:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=1)
                parsed_response = json.loads(response)
                self.messages_received.append(parsed_response)
                message_count += 1

                # Parse message content
                msg_type = parsed_response.get('type', 'unknown')
                agent_name = parsed_response.get('agent_name', 'System')
                content = parsed_response.get('content', str(parsed_response))

                logger.info(f"📥 [{msg_type}] {agent_name}: {content}")

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error listening: {e}")
                break

        logger.info(f"📊 Received {message_count} messages in {duration} seconds")
        return message_count

    async def run_comprehensive_test(self):
        """Run all tests in sequence"""
        logger.info("🚀 Starting comprehensive BotArmy test suite...")

        # Connect first
        if not await self.connect():
            logger.error("❌ Cannot run tests without connection")
            return self.test_results

        # Test 1: Basic connectivity
        await self.test_basic_connectivity()
        await asyncio.sleep(2)

        # Test 2: OpenAI integration
        await self.test_openai_integration()
        await asyncio.sleep(2)

        # Test 3: Agent workflow
        await self.test_agent_workflow()

        # Test 4: Listen for ongoing messages
        message_count = await self.listen_for_messages(30)
        self.test_results["message_listening"] = message_count > 0

        return self.test_results

    def print_summary(self):
        """Print test results summary"""
        logger.info("📋 Test Results Summary:")
        logger.info("=" * 50)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)

        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{test_name:<20}: {status}")

        logger.info("=" * 50)
        logger.info(f"Overall: {passed_tests}/{total_tests} tests passed")
        logger.info(f"Total messages received: {len(self.messages_received)}")

        if self.messages_received:
            logger.info("📨 Sample messages received:")
            for msg in self.messages_received[-3:]:  # Last 3 messages
                logger.info(f"   {json.dumps(msg, indent=2)}")

    async def close(self):
        """Close WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
            logger.info("🔌 WebSocket connection closed")

async def main():
    """Main test runner"""
    tester = BotArmyTester()

    try:
        results = await tester.run_comprehensive_test()
        tester.print_summary()

        # Exit code based on results
        failed_tests = sum(1 for result in results.values() if not result)
        sys.exit(failed_tests)

    except KeyboardInterrupt:
        logger.info("🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Test suite failed: {e}")
        sys.exit(1)
    finally:
        await tester.close()

if __name__ == "__main__":
    logger.info("🧪 BotArmy Enhanced HITL Integration Test Suite")
    logger.info("Make sure the backend is running on localhost:8000")
    logger.info("Press Ctrl+C to interrupt at any time")

    asyncio.run(main())
