import asyncio
import os
import controlflow as cf
# Removed direct import of status_broadcaster to prevent circular dependencies

async def request_human_approval(
    agent_name: str,
    description: str,
    session_id: str,
    status_broadcaster
) -> str:
    """
    Requests human approval for a specific agent task, with a timeout.

    This function will:
    1. Check an environment variable to bypass approval for testing.
    2. Broadcast a "waiting for approval" status to the UI via the passed broadcaster.
    3. Use `cf.input()` to prompt for user approval with a 5-minute timeout.
    4. Return the user's decision or the default action on timeout.
    """
    # Broadcast to the UI first, so it's always sent
    if hasattr(status_broadcaster, "broadcast_agent_waiting"):
        await status_broadcaster.broadcast_agent_waiting(agent_name, description, session_id)
    else:
        print(f"Warning: status_broadcaster does not have method 'broadcast_agent_waiting'.")

    # Bypass mechanism for automated runs
    auto_action = os.getenv("AUTO_ACTION", "none").lower()
    if auto_action == "approve":
        print(f"AUTO_ACTION=approve enabled. Automatically approving {agent_name}.")
        return "approved"
    elif auto_action == "deny":
        print(f"AUTO_ACTION=deny enabled. Automatically denying {agent_name}.")
        return "denied"

    prompt = (
        f"Agent '{agent_name}' is ready to start. "
        f"Task: {description}. "
        "Please type 'approve' to continue or 'deny' to skip."
    )


    try:
        # Use asyncio.wait_for to enforce a timeout on the ControlFlow input
        # cf.input itself doesn't have a timeout parameter.
        decision_future = cf.input(prompt)

        # In a real scenario, cf.input() returns a future-like object
        # that we can await.
        decision = await asyncio.wait_for(
            decision_future,
            timeout=300.0  # 5 minutes
        )

        # Normalize the decision
        if isinstance(decision, str) and decision.lower().strip() == 'approve':
            print(f"User approved task for agent: {agent_name}")
            return "approved"
        else:
            print(f"User denied task for agent: {agent_name}. Input was: {decision}")
            return "denied"

    except asyncio.TimeoutError:
        print(f"Approval for {agent_name} timed out after 5 minutes. Defaulting to 'approved'.")
        # If the user is unavailable, we continue the workflow by default
        # as per architectural guidelines.
        return "approved_timeout"
    except Exception as e:
        print(f"An error occurred while waiting for human input for {agent_name}: {e}")
        return "denied_error"
