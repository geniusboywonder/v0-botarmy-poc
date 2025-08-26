# Project Polish Plan for v0-botarmy-poc

## Role and Expertise

- You are a **senior solution architect** with **deep full-stack experience**, adhering to **best practice standards** for architecture, coding standards, and **modularized code**.

## Codebase and Branch

- Work in the codebase at **/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc**.
- Use the **feature/multi-task-update-1** branch.

## Communication & Documentation

- Refer to **ClaudeProgress.md** to track and understand progress.
- Update **docs/4Jules.md** with planned next steps and coding guidelines.

## Preparation & Context-gathering

- **Scan** the project’s files and folder structure to fully understand its functionality before starting.
- **Understand the product spec document** - found at **Psd/botarmy-psd.md** to understand context if needed.

## Goal

- **Polish the project** to ensure it is **robust and fully functional**.
- Replace **all mock functions** with **real functions**.
- Replace **all mock data** with **real data**.

## Coding Guidelines

- Avoid including actual code in the plan unless demonstrating a **new pattern, method, or example**.
- Ensure code follows **modular design**, adheres to **best practices**, and is **production-ready**.
- Maintain **consistency** in status tags and colors across components (e.g., Queued, WIP, Waiting, Error, Done).
- Use **real-time data** for all dynamic components, replacing any static or mock data.
- Ensure **UI elements** are responsive, aligned, and optimized for screen space (no scrolling where avoidable).

## Specific Tasks

The following tasks address specific issues to make the project production-ready. Each task will be executed sequentially, with progress updated in **ClaudeProgress.md** and confirmation sought before proceeding to the next task.

### Task 1: Dashboard Page - Chat Interactions

- **Objective**: Ensure interactions to and from **agents/roles** and **HITL** appear in the chat window with the agent/role name and their message/update.
- **Steps**:
  - Review the current chat window implementation to confirm data sources and rendering logic.
  - Verify that **agent/role names** and **messages/updates** are displayed correctly.
  - Check that **HITL interactions** are integrated and visible in the chat window.
  - If mock data or functions are used, replace them with real data sources (e.g., agent logs or API calls).
  - Test for real-time updates to ensure messages reflect the latest interactions.
- **Next Steps**:
  - Update **ClaudeProgress.md** with findings and changes.
  - Confirm with you before proceeding to Task 2.

### Task 2: Dashboard Page - Agent Status Box

- **Objective**: Redesign the Agent Status Box to match the mockup, optimize space, and ensure functionality.
- **Requirements**:
  - Position the Agent Status Box **above the chat window**.
  - Condense agent boxes to fit the chat window on the screen without scrolling (adjust chat window height if needed).
  - Include:
    - **Line 1**: Agent/Role name, Play/Pause button.
    - **Line 2**: Current task status (same tags/colors as Tasks page: Queued, WIP, Waiting, Error, Done), with a short task description.
    - **Line 3**: Current task number and total tasks (e.g., 1/5, 2/5).
  - **Functionality**:
    - Play/Pause button toggles the agent’s task and updates status to **Waiting** (and back to previous state on re-toggle).
    - Send pause/continue instructions to the agent.
    - Status in Line 2 must update dynamically with matching colors.
    - Each agent box must have its own **border**, with the pause button inside and task description text **cut off or scrolling** (no wrapping) if it doesnot fit within the border.
- **Steps**:
  - Review the mockup (**Screenshot 2025-08-21 at 11.44.06**) and current Agent Status Box code.
  - Adjust CSS to condense boxes and ensure proper alignment (pause button inside borders, text truncation/scrolling).
  - Update the status update logic to sync with Tasks page tags/colors.
  - Implement Play/Pause toggle functionality with agent communication (e.g., via API or event system).
  - Replace any mock data with real-time task data.
  - Test responsiveness to ensure no scrolling is needed.
- **Next Steps**:
  - Update **ClaudeProgress.md** with changes and test results.
  - Confirm with you before proceeding to Task 3.

### Task 3: Sidebar - System Health Position

- **Objective**: Reposition **System Health** to the bottom of the sidebar, visible above the fold without scrolling.
- **Steps**:
  - Review the current sidebar layout and CSS.
  - Adjust spacing below **Settings** to accommodate **System Health** section at the bottom of the screen.
  - Ensure System Health is fully visible without scrolling on standard screen sizes.
- **Next Steps**:
  - Update **ClaudeProgress.md** with changes.
  - Confirm with you before proceeding to Task 4.

### Task 4: Tasks Page

- **Objective**: Ensure tasks reflect the **SDLC**, are displayed in **chronological order**, and sync with agent task statuses.
- **Requirements**:
  - Tasks must be based on **agent-specific SDLC tasks**.
  - Display tasks in **chronological order**.
  - Each task must have a **status tag** (Queued, WIP, Waiting, Error, Done) with matching colors from the Dashboard.
  - Statuses must stay **in sync** with agent activities.
- **Steps**:
  - Review the Tasks page code to identify task data sources.
  - Replace any mock task data with real SDLC tasks from agents.
  - Ensure tasks are sorted according to the SDLC process.
  - Sync status tags with agent states using real-time data (e.g., API or event-driven updates).
  - Verify color consistency with Dashboard page.
  - Test for real-time updates and correct ordering.
- **Next Steps**:
  - Update **ClaudeProgress.md** with changes.
  - Confirm with you before proceeding to Task 5.

### Task 5: Analytics Page

- **Objective**: Replace static/mock metrics with **real and live metrics**.
- **Steps**:
  - Review the Analytics page code to identify static or mock data.
  - Identify or create functions to fetch **real-time metrics** (e.g., API calls, database queries).
  - Replace all static numbers with dynamic data.
  - Test metrics for accuracy and real-time updates.
- **Next Steps**:
  - Update **ClaudeProgress.md** with changes.
  - Confirm with you before proceeding to Task 6.

### Task 6: Artifacts Page

- **Objective**: Add a **checklist section** above the Artifacts Repository for managing artifacts per project phase.
- **Requirements**:
  - Include a **list of possible artifacts** for each SDLC phase.
  - Use a **Y/N checklist** where items can be toggled.
  - Toggling an artifact indicates to the agent whether to **produce or skip** it.
  - **Critical/base artifacts** (e.g., product spec for architectural plan) cannot be unchecked if required by other checked artifacts.
  - Prevent unchecking of critical artifacts through UI logic (e.g., disable toggle).
- **Steps**:
  - Review the Artifacts page code and existing repository structure.
  - Define artifacts for each SDLC phase (e.g., requirements, design, code, tests).
  - Implement a checklist UI component with Y/N toggles.
  - Add logic to communicate artifact toggles to relevant agents (e.g., via API or events).
  - Implement dependency logic to prevent unchecking critical artifacts.
  - Test checklist functionality and agent communication.
- **Next Steps**:
  - Update **ClaudeProgress.md** with changes.
  - Confirm with you before proceeding to additional tasks.

## Task 7: Additional Production-Ready Improvements

- **Identify** other areas needing polish (e.g., screen layout, error handling, performance optimization).
- **Steps**:
  - Conduct a full codebase review to identify mock functions/data, performance bottlenecks, or incomplete features.
  - Check for **error handling** across all pages and APIs.
  - Optimize **performance** (e.g., reduce API calls, lazy-load components).
  - Document findings in **ClaudeProgress.md** and propose solutions in **4Jules.md**.
-

## Execution Plan

- **Sequential Execution**: Address each task one at a time, starting with the plan.
- **Progress Tracking**: Continuously update **ClaudeProgress.md** after each task with detailed changes and test results.
- **Confirmation**: Seek your confirmation before moving to the next task.
- **Documentation**: Continuously update **/docs/4Jules.md** with plans, clarifications, and coding guidelines.

## Next Immediate Steps

- **Start with the Plan**:
  - Plan and document the next steps in a file called **docs/4Jules.md**

- Document findings and proposed changes in **ClaudeProgress.md** at each task.
  
- **Seek Clarifications** to any questions to remove ambiguity and check any assumptions while you plan.
  
- **Await my confirmation** between each step.
