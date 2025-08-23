# Frontend Integration Guide for Enhanced Agent Status

**Author**: Jules
**Date**: August 23, 2025
**Context**: This document outlines the frontend changes required to integrate with the new, unified `agent_status` WebSocket message from the backend.

---

## 1. Overview of Changes

The backend has been updated to send a single, unified `agent_status` message type that includes all information about an agent's state, including progress and errors. The previous `agent_progress` and `agent_error` message types have been deprecated.

The frontend needs to be updated to handle this new message schema and display the richer information in the UI.

---

## 2. New `agent_status` Message Schema

All agent status updates will now arrive as a WebSocket message with `type: "agent_status"`. The `data` payload will have the following structure:

```typescript
interface AgentStatusData {
  agent_name: string;
  status: 'starting' | 'working' | 'completed' | 'error' | 'skipped' | 'idle';
  current_task?: string;
  progress_percentage?: number; // A value from 0 to 100
  estimated_completion?: string; // e.g., "2 minutes"
  error_message?: string; // Only present if status is 'error'
  session_id: string;
  metadata?: Record<string, any>;
}

interface AgentStatusMessage {
  type: 'agent_status';
  timestamp: string; // ISO 8601
  data: AgentStatusData;
}
```

---

## 3. Frontend Implementation Steps

### Step 3.1: Update WebSocket Service (`lib/websocket/websocket-service.ts`)

The main WebSocket message handler needs to be updated to correctly parse the new `agent_status` message.

**File to modify**: `lib/websocket/websocket-service.ts`

1.  Locate the `handleMessage` function (or equivalent).
2.  Ensure the case for `type === 'agent_status'` correctly routes the `message.data` to the agent store.
3.  Remove any handlers for the old `agent_progress` or `agent_error` message types if they exist.

**Example:**
```typescript
// Inside your WebSocket message handler
if (message.type === 'agent_status') {
  // Get the agent store
  const agentStore = useAgentStore.getState();
  // Call a new method on the store to update the agent's status
  agentStore.updateAgentStatus(message.data);
}
```

### Step 3.2: Update Agent Store (`lib/stores/agent-store.ts`)

The Zustand store for agents needs to be updated to hold the new, richer state for each agent.

**File to modify**: `lib/stores/agent-store.ts`

1.  **Update the AgentState interface**: The state for each agent should be updated to match the fields in the `AgentStatusData` interface above.

    ```typescript
    interface AgentState {
      name: string;
      status: 'starting' | 'working' | 'completed' | 'error' | 'skipped' | 'idle';
      currentTask?: string;
      progressPercentage?: number;
      estimatedCompletion?: string;
      errorMessage?: string;
      // ... any other fields
    }
    ```

2.  **Create an `updateAgentStatus` action**: This action will take the `AgentStatusData` from the WebSocket message and update the state of the corresponding agent.

    ```typescript
    // Inside your Zustand store definition
    updateAgentStatus: (statusData: AgentStatusData) =>
      set((state) => ({
        agents: state.agents.map((agent) =>
          agent.name === statusData.agent_name
            ? {
                ...agent,
                status: statusData.status,
                currentTask: statusData.current_task,
                progressPercentage: statusData.progress_percentage,
                errorMessage: statusData.error_message,
              }
            : agent
        ),
      })),
    ```

### Step 3.3: Update Agent Status Card Component (`components/agent-status-card.tsx`)

This is the main UI component that needs to be updated to display the new information.

**File to modify**: `components/agent-status-card.tsx`

1.  **Display `current_task`**: Show the `agent.currentTask` string prominently in the card.
2.  **Implement a Progress Bar**: Use a UI component (like ShadCN's `Progress`) to display the `agent.progressPercentage`. The progress bar should only be visible when the agent's status is `working`.
3.  **Show Error Messages**: When `agent.status` is `error`, display the `agent.errorMessage` clearly. You could use a different color or an icon to indicate the error state.
4.  **Use Status for Styling**: The `agent.status` can be used to dynamically change the styling of the card (e.g., border color, background color) to reflect the agent's state.
    *   `working`: Blue border, show progress bar.
    *   `completed`: Green border.
    *   `error`: Red border, show error message.
    *   `skipped`: Gray border.

**Example JSX Structure:**
```tsx
const AgentStatusCard = ({ agent }: { agent: AgentState }) => {
  return (
    <Card className={`status-${agent.status}`}>
      <CardHeader>
        <CardTitle>{agent.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{agent.currentTask || 'Waiting...'}</p>

        {agent.status === 'working' && agent.progressPercentage !== undefined && (
          <Progress value={agent.progressPercentage} className="mt-2" />
        )}

        {agent.status === 'error' && (
          <div className="text-red-500 mt-2">
            <strong>Error:</strong> {agent.errorMessage}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
```

---

## 4. Summary

By following these steps, the frontend will be able to fully utilize the enhanced, real-time agent status updates from the backend, providing a much richer and more informative user experience.
