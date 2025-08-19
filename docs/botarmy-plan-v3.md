# BotArmy Development Plan (v3 - Frontend Integration)

## 1. Overall Goal

To connect the existing frontend UI to the new, event-driven backend architecture, enabling end-to-end testing of the agent workflow.

---

## Phase 1: Connect UI to Backend Services

*   **Task 1.1: Connect the Chat Input to Start Workflow**
    *   **Objective:** Allow the user to trigger the main SDLC workflow from the UI.
    *   **Action:** Modify the dashboard page to ensure the 'Start New Project' button sends the `start_project` user command via the `websocketService`.

*   **Task 1.2: Implement Real-time Error Display**
    *   **Objective:** Ensure backend errors are clearly visible in the UI for debugging.
    *   **Action (Backend):** Modify the `AGUI_Handler` to catch exceptions and broadcast a `SYSTEM_ERROR` message.
    *   **Action (Frontend):** Update the `WebSocketService` to handle `SYSTEM_ERROR` messages and push them to the `LogStore`.

*   **Task 1.3: Display Real-time Agent Messages**
    *   **Objective:** Display the stream of messages from the agent workflow in the UI.
    *   **Action:** Refactor the main chat/log view to clear mock data and render live messages from the `LogStore`.

*   **Task 1.4: Final Verification**
    *   **Objective:** Verify the full end-to-end functionality.
    *   **Action:** Use the Playwright testing process to start a workflow and capture a screenshot of real agent messages appearing in the UI.
