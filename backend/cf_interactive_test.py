import controlflow as cf
import asyncio
import logging

from backend.bridge import AGUI_Handler

# Mock the ConnectionManager for this standalone test
class MockConnectionManager:
    def __init__(self):
        self.broadcast_messages = []
        print("[MockConnectionManager] Initialized.")

    async def broadcast(self, message: str):
        # In a real scenario, this would send a message over WebSocket
        print(f"[MockConnectionManager] Broadcasting: {message}")
        self.broadcast_messages.append(message)

# This is the task that will ask for user input
@cf.task(interactive=True)
def get_user_favorite_color():
    """
    Asks the user for their favorite color and returns it.
    """
    logger = cf.get_run_logger()
    logger.info("Now asking the user for their favorite color.")
    # The agent will implicitly use the "ask user" tool here
    # because the task is interactive.
    return "What is your favorite color?"

async def main():
    print("--- Testing ControlFlow Interactive Task ---")

    # 1. Set up the mock manager and our custom handler
    mock_manager = MockConnectionManager()
    # We need a running event loop to create the handler
    loop = asyncio.get_running_loop()
    agui_handler = AGUI_Handler(mock_manager, loop)

    # 2. Get the root logger and add our handler
    root_logger = logging.getLogger("prefect")
    root_logger.addHandler(agui_handler)
    root_logger.setLevel(logging.INFO)

    print("\nLogger setup complete. Running an interactive ControlFlow task...")

    try:
        # 3. Run the task
        # We expect this to hang because we can't provide input,
        # but we should see the log messages from the AGUI_Handler first.
        # We add a timeout to prevent it from hanging forever.
        print("Running task with a 15-second timeout...")
        await asyncio.wait_for(
            cf.run(get_user_favorite_color),
            timeout=15.0
        )

    except asyncio.TimeoutError:
        print("\n--- Task Timed Out (as expected) ---")
        print("The task timed out waiting for user input, which is the expected behavior in this non-interactive test environment.")
        print("Please check the log output above for '[AGUI_Handler]' messages. These messages show what events were captured before the timeout.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        # Clean up the handler
        root_logger.removeHandler(agui_handler)


if __name__ == "__main__":
    # Note: This test requires an OPENAI_API_KEY to be set, as ControlFlow
    # initializes a default agent even for interactive tasks.
    asyncio.run(main())
