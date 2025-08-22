# Architecting Role-Based AI Agents with Model Context Protocol (MCP)

## Concept Overview

This document outlines a paradigm for building AI systems by creating specialized, role-constrained agents as MCP servers and orchestrating them into automated workflows. The goal is to move beyond monolithic prompts to a modular, service-oriented architecture for AI.

## Core Principle: Specialized MCP Servers

Each agent is a standalone MCP server with a predefined role, defined primarily by its **system prompt** and a set of role-specific **tools**.

### Example: Business Analyst Service

**Server:** `business_analyst_service`

* **System Prompt (Baked-In):**

    ```plaintext
    "You are an expert Business Analyst. Your sole purpose is to analyze business requirements. You excel at:
    - Identifying and elaborating user stories and epics.
    - Defining clear acceptance criteria.
    - Creating process flow diagrams (e.g., using Mermaid.js syntax).
    - Asking clarifying questions to resolve ambiguities in requirements.

    You must refuse to answer questions outside your domain, such as code implementation, infrastructure setup, or marketing strategy. Your communication is always structured, professional, and precise."
    ```

* **Exposed MCP Tools:**
  * `analyze_requirement(requirement: str) -> str`: Takes a raw requirement and returns a structured analysis.
  * `generate_user_story(actor: str, goal: str, reason: str) -> str`: Returns a well-formed user story.
  * `create_process_flow(process_description: str) -> str`: Returns a Mermaid.js diagram code block.

## Orchestration: The Conductor Model

Specialized agents are useless in isolation. An **Orchestrator** (a separate process or agent) manages the flow of work between them based on a pre-defined process, eliminating the need for detailed step-by-step user prompts.

### Example Workflow: "From Idea to Design"

**Process:** User Requirement -> Business Analysis -> Technical Design

1. **User Input:** "We need a user login system for our web app with social auth."

2. **Orchestrator Action:**
    * **Rule:** `ON new_requirement DO CALL business_analyst.analyze_requirement(<input>)`
    * **Action:** The Orchestrator, following its internal logic, packages the user input and calls the `analyze_requirement` tool on the `business_analyst_service` MCP server.
    * **No detailed prompt is needed.** The service's predefined role dictates its behavior.

3. **Analysis Result:** The BA Service returns structured output:

    ```markdown
    **Analysis of Login System Requirement:**
    - **User Stories Identified:**
      1. **US01:** As a new user, I want to register with my email and password so that I can access the app.
      2. **US02:** As a user, I want to log in with Google so that I don't have to remember a password.
    - **Acceptance Criteria for US02:**
      - Given I am on the login page, I should see a "Login with Google" button.
      - When I click the button, I should be redirected to Google's authentication service.
      - Upon successful authentication, I should be redirected to the app's dashboard.
    - **Process Flow:**
      ```mermaid
      graph LR
        A[User Clicks Login] --> B{Auth Provider?};
        B -->|Email| C[Internal Auth];
        B -->|Google| D[OAuth with Google];
        C --> E[Verify Credentials];
        D --> E;
        E --> F[Grant Access];
      ```

    ```

4. **Orchestrator Action:**
    * **Rule:** `ON successful_analysis DO CALL software_architect.create_design(<analysis_output>)`
    * **Action:** The Orchestrator takes the BA's output and calls the `create_design` tool on a `software_architect_service` MCP server.

5. **Design Result:** The Architect Service returns its output (e.g., technology choices, API design, database schema).

6. **Final Output:** The Orchestrator compiles the results from all called services and presents a final, comprehensive package to the user.

## Technical Architecture

```mermaid
graph TB
    subgraph "External Dependencies"
        LLM[LLM e.g., Claude, GPT]
    end

    subgraph "Orchestrator Layer"
        O[Orchestrator]
        OP[("Orchestration Logic<br/>e.g., State Machine /<br/>Orchestrator LLM with Prompt")]
        O <-.-> OP
    end

    subgraph "MCP Agent Layer (Role-Specific Servers)"
        BA[BusinessAnalystService]
        SA[SoftwareArchitectService]
        QA[QAAnalystService]
        Dev[DeveloperService]
    end

    User[User/Client App] -- "Initial Request" --> O
    O -- "Calls Tools via MCP" --> BA
    O -- "Calls Tools via MCP" --> SA
    O -- "Calls Tools via MCP" --> QA
    O -- "Calls Tools via MCP" --> Dev
    O -- "Final Response" --> User

    BA -.-> LLM
    SA -.-> LLM
    QA -.-> LLM
    Dev -.-> LLM

    style BA fill:#e6f3ff
    style SA fill:#ffe6e6
    style QA fill:#f9e6ff
    style Dev fill:#e6ffec
