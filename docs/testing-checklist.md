# MVP Demo - Testing Checklist

This document outlines the steps to test the stability and functionality of the BotArmy MVP.

## 1. Setup

- [ ] Ensure all backend dependencies are installed (`pip install -r backend/requirements.txt`).
- [ ] Ensure all frontend dependencies are installed (`npm install` or `pnpm install`).
- [ ] Set the `OPENAI_API_KEY` environment variable.
- [ ] Start the backend server: `python backend/main.py`.
- [ ] Start the frontend development server: `npm run dev`.
- [ ] Open the application in your browser (usually `http://localhost:3000`).

## 2. Backend Reliability Testing

### ✅ Task 1 & 6: Connection Stability & Heartbeats
- [ ] **Test 1.1:** Verify the "Connected" status appears in the UI shortly after loading.
- [ ] **Test 1.2:** Stop the backend server. Verify the UI status changes to "Connecting..." or "Disconnected".
- [ ] **Test 1.3:** Restart the backend server. Verify the UI automatically reconnects and the status returns to "Connected".
- [ ] **Test 1.4:** Leave the application idle for > 90 seconds. Verify the connection remains active (due to heartbeats).

### ✅ Task 4 & 5: LLM Service Robustness (Retries & Rate Limiting)
- [ ] **Test 2.1:** Click the "Test OpenAI" button. Verify a success message appears in the log.
- [ ] **Test 2.2 (If possible):** Temporarily set an invalid `OPENAI_API_KEY`. Click "Test OpenAI". Verify a user-friendly error ("AI service configuration needed...") appears in the log.
- [ ] **Test 2.3 (Hard to test):** The rate limiter and retry logic are built-in. A successful project run without rate-limiting errors is a pass.

### ✅ Task 2, 7, 8: Workflow Error Handling & Status Broadcasting
- [ ] **Test 3.1:** Click "Start Test Project".
- [ ] **Test 3.2:** Observe the Agent Status cards. Verify that each agent's status changes in real-time (e.g., `started` -> `thinking` -> `completed`).
- [ ] **Test 3.3:** Observe the Agent Command & Log. Verify that status messages are broadcast throughout the process.
- [ ] **Test 3.4 (If possible):** Introduce an error in one of the agent prompts (e.g., in `backend/agents/developer_agent.py`). Run a project. Verify the workflow reports the error for that agent but *continues* to the next agent.

## 3. Frontend Reliability Testing

### ✅ Task 9: Message Queuing
- [ ] **Test 4.1:** Start a project. While it's running, stop the backend server.
- [ ] **Test 4.2:** Type a new project brief and click "Send". The UI should appear to accept it.
- [ ] **Test 4.3:** Restart the backend server. Verify that once the connection is re-established, the queued project is automatically started.

### ✅ Task 10, 13, 14: UI Polish & Real-time Updates
- [ ] **Test 5.1:** While a project is running, verify the "Send" button in the chat interface is disabled and shows a loading state.
- [ ] **Test 5.2:** Verify the `ConnectionStatus` component accurately reflects the connection state at all times.
- [ ] **Test 5.3:** Verify the Agent Status cards have a blue ring and a typing indicator when an agent is working.
- [ ] **Test 5.4:** If an agent encounters an error, verify its card gets a red ring.

### ✅ Task 12: Error Boundary
- [ ] **Test 6.1 (Requires code change):** Introduce a deliberate rendering error in `app/page.tsx` (e.g., `throw new Error("Test UI Crash")` inside the component).
- [ ] **Test 6.2:** Reload the page. Verify that the user-friendly "Something went wrong" error fallback is displayed instead of a crashed white screen.
- [ ] **Test 6.3:** Click the "Try again" button in the fallback UI. Verify the error state is cleared and the component re-renders.

---
**SUCCESS DEFINITION:** A user can start a project, see all 5 agents respond in sequence through OpenAI, with zero technical errors visible to the user.
