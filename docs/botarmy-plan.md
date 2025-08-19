
# BotArmy Development Plan (v2 - Library-Aware) - FINAL

## 1. Overall Goal

To implement the core backend architecture for BotArmy by integrating the `ControlFlow` library for orchestration and the `AG-UI` protocol for communication. This plan is the definitive roadmap for building the agentic backend.

---

## Phase 1: Foundational Integration (`ControlFlow` + `AG-UI`) - ✅ COMPLETED

**Objective:** To establish a working connection between the `ControlFlow` orchestration engine and the `AG-UI` frontend communication protocol.

*(Tasks omitted for brevity as phase is complete)*

---

## Phase 2: Agent Implementation - ✅ COMPLETED

**Objective:** To replace the placeholder tasks with real, LLM-powered agents that perform the SDLC functions.

*(Tasks omitted for brevity as phase is complete)*

---

## Phase 3: Human-in-the-Loop (HITL) Integration - 🛑 HALTED

**Objective:** To leverage `ControlFlow`'s user interaction features to implement the required HITL functionality.

**Status:** Work on this phase has been halted as per user instruction. The project is being finalized in its current state.

---

## Phase 4: Feature Migration & Finalization - 🛑 HALTED

**Objective:** To migrate the existing features (Artifacts, etc.) to be compatible with the new event-driven, `ControlFlow`-based architecture.

**Status:** Work on this phase has been halted.
=======
# BotArmy Implementation Plan

## 1. Introduction

This document outlines the plan to complete the implementation of the BotArmy project, based on the Product Specification Document (`docs/botarmy-psd.md`) and the current state of the codebase. The plan is divided into phases, with specific tasks and objectives for each phase.

## 2. Overall Project Status

* **Estimated Completion:** 15%
* **Next Steps:** The immediate focus is on implementing the core agent functionalities and integrating the frontend and backend to create a functional end-to-end user experience.

## 3. Phase 1: Core Functionality (Current Focus)

This phase focuses on bringing the application to a state where a user can initiate a project and see the agents collaborating in real-time.

| Module | Task | Est. Completion |
| :--- | :--- | :--- |
| **Backend: Agent Orchestration** | 1. Implement the `Orchestrator` agent to manage the SDLC workflow. | 10% |
| | 2. Develop the `AnalystAgent` to process initial user input. | 5% |
| | 3. Implement the `ArchitectAgent` to create a technical design. | 5% |
| | 4. Implement the `DeveloperAgent` to generate code. | 5% |
| | 5. Implement basic handoff mechanism between agents. | 10% |
| **Backend: WebSocket Integration** | 1. Integrate agent actions with the WebSocket to stream updates to the UI. | 20% |
| | 2. Implement real-time logging of agent interactions. | 15% |
| **Frontend: Real-time Updates** | 1. Connect the agent status cards to the WebSocket to display real-time status. | 30% |
| | 2. Connect the chat interface to the WebSocket to display agent conversations. | 20% |
| **Human-in-the-Loop (HITL)** | 1. Implement a basic "pause/resume" functionality for the orchestrator. | 10% |
| | 2. Create a simple UI notification for when user input is required. | 5% |

## 4. Phase 2: Advanced Features and Refinement

This phase will focus on enhancing the core functionality with more advanced features, as outlined in the PSD.

| Module | Task | Est. Completion |
| :--- | :--- | :--- |
| **Backend: Advanced Agents**| 1. Implement the `TesterAgent` for automated testing. | 0% |
| | 2. Implement the `DeploymentAgent` for deployment tasks. | 0% |
| | 3. Implement conflict resolution logic between agents. | 0% |
| **Backend: Data Persistence**| 1. Store conversation logs in JSONL files. | 0% |
| | 2. Manage project specifications using JSON Patch. | 0% |
| **Frontend: UI Enhancements** | 1. Implement the "Artifacts" page. | 10% |
| | 2. Implement the "Settings" page. | 10% |
| | 3. Add filtering capabilities to the "Logs" page. | 5% |
| **HITL** | 1. Develop a priority-based action queue for the user. | 0% |
| | 2. Implement modal interfaces for complex user decisions. | 0% |
| **Testing** | 1. Implement unit tests for backend agents. | 5% |
| | 2. Implement component tests for the frontend. | 5% |

## 5. Phase 3: Production Readiness

This phase will focus on preparing the application for a production environment.

| Module | Task | Est. Completion |
| :--- | :--- | :--- |
| **Backend: LLM Management**| 1. Implement multi-provider support for LLMs. | 0% |
| | 2. Add rate limiting and cost management features. | 0% |
| **Backend: Scalability** | 1. Optimize WebSocket performance. | 10% |
| | 2. Implement connection pooling and other performance enhancements. | 5% |
| **Frontend: Performance** | 1. Implement message virtualization for large conversation histories. | 0% |
| | 2. Optimize UI rendering performance. | 10% |
| **Deployment** | 1. Create a Dockerfile for production deployment. | 50% (initial Dockerfile exists) |
| | 2. Develop a comprehensive deployment guide. | 0% |
| **Testing** | 1. Implement end-to-end tests with Playwright. | 0% |
| | 2. Conduct performance and stress testing. | 0% |

## 6. Human-in-the-Loop (HITL) Strategy

The HITL system is a critical component of BotArmy. The plan is to implement it iteratively:

1. **Basic Controls:** Start with simple pause/resume functionality to give the user basic control over the agent workflow.
2. **Explicit Approval:** Introduce points in the workflow where the agents must seek explicit approval from the user before proceeding. This will be managed via UI notifications and simple "approve/reject" actions.
3. **Advanced Decision Support:** Develop a more sophisticated action queue that provides the user with context and recommendations for complex decisions.
4. **Direct Intervention:** Allow the user to directly communicate with and re-task individual agents.

By phasing the implementation of HITL, we can ensure that the user remains in control at every stage of the development process.
