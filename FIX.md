# FIX.md: A Plan to Refactor and Stabilize the v0-botarmy-poc Application

This document outlines a comprehensive plan to address the ongoing issues with the v0-botarmy-poc application. The primary focus is on refactoring the WebSocket architecture, simplifying state management, and clarifying the real-time communication strategy.

## 1. Simplify the WebSocket Architecture

The current WebSocket implementation is overly complex. We will simplify it by adopting a more modular and single-responsibility approach.

### 1.1. Backend Refactoring

-   **Consolidate to a Single WebSocket Endpoint:**
    -   Eliminate the multiple WebSocket endpoints (`/api/ws`, `/api/copilotkit-ws`, `/ws/{session_type}/{session_id}`).
    -   Create a single endpoint, `/ws`, that handles all WebSocket connections.
    -   Use a clear and consistent message protocol to differentiate between message types (e.g., general chat, CopilotKit messages, agent status updates).

-   **Simplify `ConnectionManager`:**
    -   Create a new, simpler `ConnectionManager` class that is only responsible for managing WebSocket connections (connecting, disconnecting, sending messages).
    -   Remove all other functionality (heartbeats, message queuing, rate limiting) from this class.

-   **Create a `HeartbeatService`:**
    -   Implement a new `HeartbeatService` that is solely responsible for sending pings and managing connection health.
    -   This service will periodically send pings to all connected clients. If a client does not respond with a pong within a specified timeout, the connection will be considered stale and closed.

-   **Refactor `AgentStatusBroadcaster`:**
    -   The `AgentStatusBroadcaster` should not hold agent state. Its only responsibility should be to broadcast messages to connected clients.
    -   Agent state should be managed by a separate, dedicated state management service (see section 2).

### 1.2. Frontend Refactoring

-   **Simplify `EnhancedWebSocketService`:**
    -   Create a new, simpler `WebSocketService` that is only responsible for establishing and maintaining a WebSocket connection.
    -   Remove all the complex logic for reconnection, message batching, and heartbeats.
    -   Consider using a lightweight, battle-tested library like `react-use-websocket` to handle the boilerplate of WebSocket management.

-   **Implement a Client-Side Heartbeat:**
    -   The new `WebSocketService` will be responsible for sending `pong` messages in response to the server's `ping` messages.
    -   It will also periodically send its own `ping` messages to the server to ensure the connection is alive.

## 2. Centralize and Simplify State Management

The current state management is fragmented and unpredictable. We will centralize state management on the backend and create a clear, unidirectional data flow.

### 2.1. Backend State Management

-   **Create a `StateService`:**
    -   Implement a new `StateService` that will be the single source of truth for all application state (agent status, workflow progress, artifacts, etc.).
    -   This service will be responsible for persisting state (e.g., in memory for the POC, but designed to be easily swappable with a database).
    -   All changes to the application state must go through this service.

-   **Update Flow:**
    1.  A user action (e.g., sending a chat message) triggers a workflow on the backend.
    2.  As the workflow progresses, it updates the application state by calling methods on the `StateService`.
    3.  The `StateService` updates its internal state and then uses the `AgentStatusBroadcaster` to notify all connected clients of the state change.

### 2.2. Frontend State Management

-   **Unidirectional Data Flow:**
    -   The frontend will receive state updates from the backend via WebSockets.
    -   The `WebSocketService` will receive these updates and pass them to a central `StateStore` (a single Zustand store).
    -   React components will subscribe to changes in the `StateStore` and re-render accordingly.

-   **Single `StateStore`:**
    -   Consolidate the multiple Zustand stores into a single, normalized `StateStore`.
    -   This will provide a single source of truth for all frontend state and make it easier to manage and debug.

## 3. Clarify the Chat and Workflow Architecture

The current chat and workflow logic is confusing. We will simplify it by fully embracing CopilotKit and defining a clear process for triggering workflows.

### 3.1. Embrace CopilotKit

-   **Single Chat Interface:**
    -   Use the CopilotKit chat interface as the one and only chat interface for the application.
    -   Remove all the legacy custom chat components and logic.

-   **Backend for CopilotKit:**
    -   The backend will expose the necessary endpoints and services for CopilotKit to function.
    -   This includes providing a way for CopilotKit to send messages to the backend and receive responses.

### 3.2. Workflow Triggering

-   **Explicit Workflow Triggers:**
    -   Workflows will be triggered by explicit user actions, such as clicking a "Start Project" button or using a specific command in the chat interface (e.g., `/startproject <brief>`).
    -   This will eliminate the confusing logic that tries to automatically determine whether a chat message should trigger a workflow.

## 4. Address Other Issues

### 4.1. HITL Workflow and Breakpoints

-   The simplification of the WebSocket and state management architecture should make the HITL (Human-in-the-Loop) workflow easier to implement and debug.
-   With a clearer data flow, it will be easier to trace the events that are supposed to trigger HITL prompts and breakpoints.

### 4.2. Testing and Verification

-   **Unit Tests:**
    -   Write unit tests for the new, simplified services (`ConnectionManager`, `HeartbeatService`, `StateService`, etc.).
-   **Integration Tests:**
    -   Write integration tests to verify the end-to-end flow of data from the frontend to the backend and back.
-   **Manual Testing:**
    -   Thoroughly test the application to ensure that all the original issues have been resolved.

By following this plan, we will create a more stable, maintainable, and scalable application. The simplified architecture will make it easier to add new features and debug existing ones.
