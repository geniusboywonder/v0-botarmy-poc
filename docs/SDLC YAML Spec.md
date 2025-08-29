Based on my review of the codebase, here is the information you requested:

1. Agent Roles
The system is designed with the following specialized agent roles, as defined in the README.md and the backend/agents/ directory:

- Analyst: Analyzes project requirements.
- Architect: Designs the system architecture.
- Developer: Implements the core features and writes code.
- Tester: Handles quality assurance and creates test plans.
- Deployer: Manages the deployment strategy and execution.

2. Process Steps/Stages of the SDLC
The frontend is structured around a clear, process-based view of the Software Development Life Cycle (SDLC). The stages are reflected in the sidebar navigation (components/sidebar.tsx):

- Requirements: Gathering and defining what the project needs to do.
- Design: Planning the technical architecture, database schemas, and API contracts.
- Dev (Development): The actual coding and implementation phase.
- Test: Verifying the software for bugs, performance, and quality.
- Deploy: Preparing the application for release and deploying it to servers.

3. Artifacts Produced Through the Process/Per Stage
Artifacts are the tangible outputs of each stage. Based on the type definitions in lib/types.ts and the details in the mockup files, here are the typical artifacts produced at each stage:

- Requirements Stage:
  - Project Plan
  - Software Requirements Specification (SRS) Document
  - Use Case Diagrams
  - Risk Analysis

- Design Stage:
  - Architecture Design Document
  - Database Schema
  - API Specifications

- Development Stage:
  - Source Code
  - Build Scripts
  - Unit Test Files

- Test Stage:
  - Test Plans & Test Cases
  - Bug Reports
  - QA Sign-off Documents

- Deploy Stage:
  - Deployment Scripts (e.g., Dockerfile)
  - Compiled Application/Executables

Release Notes

I have completed my analysis of the backend. Here is a summary of how the workflow and LLM interactions are managed:

1. Workflow Management (backend/workflow.py)
The core of the application's logic is a workflow-driven system that orchestrates the different AI agents.

Orchestration: The system uses the Prefect library to define and manage a dataflow. The main entry point is the @prefect.flow decorated function botarmy_workflow.
Sequential Task Execution: The workflow operates on a predefined list of agents (AGENT_TASKS). It iterates through this list, executing each agent's task sequentially.
Chained Inputs/Outputs: The output from one agent's task is passed as the input to the next agent in the sequence. This creates a continuous flow of information through the SDLC stages.
Human-in-the-Loop (HITL): The workflow has built-in checkpoints where it can pause and request human approval before proceeding. This is configurable for each agent task.
Status Broadcasting: Throughout the workflow, it uses an AgentStatusBroadcaster to send real-time progress updates to the frontend, allowing users to see what's happening.
2. LLM and Agent Interactions (llm_service.py & base_agent.py)
The interaction between the AI agents and the Large Language Models (LLMs) is handled by a dedicated, centralized service to ensure modularity and resilience.

Centralized LLM Service: All communication with LLMs is routed through a singleton service defined in backend/services/llm_service.py. This service abstracts away the complexity of dealing with different LLM APIs.
Multi-Provider Support & Fallback: The LLMService is designed to work with multiple providers (Google Gemini, OpenAI, Anthropic). It has a priority list and will automatically fall back to the next provider if one fails, making the system more robust.
Rate Limiting: The service includes a rate limiter to prevent sending too many requests to the LLM APIs in a short period, avoiding API errors and potential blocks.
Base Agent Logic: Each specialized agent (Analyst, Developer, etc.) inherits from a BaseAgent class (backend/agents/base_agent.py). This base class contains the main execute logic.
Agent Execution Flow: When an agent's turn comes in the workflow, its execute method is called. This method takes the current data, combines it with the agent's specific system_prompt (which defines its role and instructions), and sends the final prompt to the LLMService. The agent then receives the text response from the service to complete its task.
This architecture effectively decouples the high-level workflow from the low-level details of LLM communication, creating a clean and maintainable backend system.
