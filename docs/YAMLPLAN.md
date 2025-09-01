# BotArmy Project Plan

This document outlines the development plan for the BotArmy project.

---

## 2024-08-28 12:00:00 UTC - Initial Plan: Generic Process Engine

**Goal:** Refactor the BotArmy application to be a generic process engine driven by a configuration file (YAML). This will allow it to manage any well-defined process, not just the hardcoded SDLC workflow. The core stages (Analyze, Design, Build, Validate, Launch) will remain constant, but the roles and artifacts will become dynamic.

**Assumptions:**

- The backend is built with Python and likely uses a workflow orchestrator like Prefect.
- The frontend is a Next.js application.
- The current SDLC process, roles, and artifacts are largely hardcoded in the application logic.
- The application will be refactored to read a `process.yaml` file at the start of a new job, which will define the specifics of the workflow.

---

### **Phase 1: Configuration Definition & Parsing**

**Objective:** Define a clear, extensible YAML schema for processes and implement the backend logic to parse and validate it.

- **Step 1.1: Define YAML Schema**
  - **Timestamp:** 2024-08-28 12:05:00 UTC
  - **What:** Design the structure for `process.yaml`. It must define `roles` and `artifacts`. Each role should have a `name`, `description` (prompt), and a list of allowed `tools`. Each artifact should have a `name`, `description`, and `path` or storage location. The schema should also map which roles are active and which artifacts are produced in each of the five core stages.
  - **How:** Create a formal schema definition (e.g., using JSON Schema) to enforce structure. The design should be modular.
  - **Scaffolding Example (`process-schema.json` and `sdlc.yaml`):**

    ```yaml
    # Example: sdlc.yaml
    process_name: Software Development Lifecycle
    description: A standard process for building and deploying software.

    roles:
      - name: Product Manager
        description: "You are a Product Manager. Your goal is to define the product requirements clearly."
        tools: [Read, Write, WebSearch]
      - name: Software Engineer
        description: "You are a Software Engineer. Your goal is to write high-quality, functional code based on the requirements."
        tools: [Read, Write, Edit, Bash, Grep]
      - name: QA Engineer
        description: "You are a QA Engineer. Your goal is to test the software and find bugs."
        tools: [Read, Bash, Grep]

    artifacts:
      - name: Requirements Document
        description: "A markdown file detailing the project requirements."
        path: "docs/requirements.md"
      - name: Source Code
        description: "The application source code."
        path: "src/"
      - name: Test Report
        description: "A report summarizing test results."
        path: "reports/test_report.md"

    stages:
      Analyze:
        active_roles: [Product Manager]
        output_artifacts: [Requirements Document]
      Design:
        active_roles: [Software Engineer]
        input_artifacts: [Requirements Document]
        output_artifacts: [] # e.g., architecture diagram, could be an artifact
      Build:
        active_roles: [Software Engineer]
        input_artifacts: [Requirements Document]
        output_artifacts: [Source Code]
      Validate:
        active_roles: [QA Engineer]
        input_artifacts: [Source Code]
        output_artifacts: [Test Report]
      Launch:
        active_roles: [Software Engineer]
        input_artifacts: [Source Code]
        output_artifacts: [] # e.g., deployment scripts
    ```

  - **New Features:** A formal, versioned schema for process definitions.

- **Step 1.2: Implement Backend YAML Parser**
  - **Timestamp:** 2024-08-28 12:10:00 UTC
  - **What:** Create a new service/module in the backend (e.g., `process_loader.py`). This service will be responsible for:
    1. Reading a specified YAML file.
    2. Validating it against the defined schema.
    3. Loading it into a structured, in-memory Python object (e.g., using Pydantic models for type safety).
  - **How:** Use a standard library like `PyYAML` for parsing and `Pydantic` for validation and data modeling. The service should raise clear errors for invalid configurations. This service will be a core dependency for the new generic workflow engine.
  - **Interdependencies:** This module will be called at the beginning of any new process run.

---

### **Phase 2: Backend Refactoring for Dynamic Processes**

**Objective:** Decouple the core application logic from any specific process, allowing it to execute workflows based on the loaded configuration.

- **Step 2.1: Generalize Data Models and Workflows**
  - **Timestamp:** 2024-08-28 12:15:00 UTC
  - **What:** Refactor database models and workflow definitions (e.g., Prefect flows).
    - `ProcessRun` model: Should store a reference to the configuration used, the current stage, and the status.
    - `AgentRun` model: Should link to a `ProcessRun` and the `role` definition from the config it's embodying.
    - `Artifact` model: Should store metadata based on the artifact definitions in the config, including its path and creation stage.
  - **How:** Use migrations to update the database schema. The Prefect flows should be parameterized to accept the loaded process configuration object as an input. Instead of a hardcoded `sdlc_flow`, create a `generic_process_flow`.
  - **Interdependencies:** This is a foundational change affecting the entire backend.

- **Step 2.2: Create a Generic Agent Executor**
  - **Timestamp:** 2024-08-28 12:20:00 UTC
  - **What:** The current agent logic likely instantiates specific agent classes (e.g., `EngineerAgent`). This needs to be replaced with a generic executor.
  - **How:** Create a single `AgentExecutor` class or function that takes a `role` definition from the configuration. It will use the `description` from the role to construct the agent's system prompt and the `tools` list to grant it specific capabilities. The core reasoning loop of the agent remains, but its personality and capabilities are now dynamic.
  - **New Features:** A single, reusable agent executor that can embody any role defined in the YAML.

- **Step 2.3: Adapt the Main Process Orchestrator**
  - **Timestamp:** 2024-08-28 12:25:00 UTC
  - **What:** The main orchestrator that moves the process from Analyze -> Design -> ... -> Launch needs to be updated.
  - **How:** The orchestrator will loop through the `stages` defined in the loaded configuration. In each stage, it will:
    1. Identify the `active_roles` for that stage.
    2. Instantiate `AgentExecutor`s for each of those roles.
    3. Provide the agents with the specified `input_artifacts`.
    4. Monitor for the creation of the required `output_artifacts` to determine stage completion.
  - **Interdependencies:** This orchestrator will be the main entry point for the `generic_process_flow`.

---

### **Phase 3: Frontend Adaptation**

**Objective:** Update the UI to be a generic interface for any configured process.

- **Step 3.1: Implement Dynamic UI Rendering**
  - **Timestamp:** 2024-08-28 12:30:00 UTC
  - **What:** Refactor UI components to render dynamically based on data from the backend.
  - **How:** The backend API/WebSocket events will now send the generic process state, including the list of roles, artifacts, and their statuses. The frontend will have generic components like `RoleCard`, `ArtifactList`, and `StageProgress` that populate themselves with this data, rather than containing hardcoded labels and logic for "Engineer" or "Requirements.md".
  - **Interdependencies:** Requires changes to the API contract between frontend and backend.

- **Step 3.2: Create a "New Process" UI**
  - **Timestamp:** 2024-08-28 12:35:00 UTC
  - **What:** Add a new screen or modal where a user can start a new process.
  - **How:** This UI should allow the user to either select from a list of predefined process templates (e.g., "Software Development", "Content Creation") or upload their own `process.yaml` file. This initiates the workflow on the backend.
  - **New Features:** User-driven process initiation with custom configurations.

---

### **Phase 4: Testing and Validation**

**Objective:** Ensure the refactored system is robust, backward-compatible with the SDLC case, and truly generic.

- **Step 4.1: End-to-End Test with SDLC YAML**
  - **Timestamp:** 2024-08-28 12:40:00 UTC
  - **What:** Conduct a full end-to-end test of the system using the `sdlc.yaml` file created in Phase 1.
  - **How:** The expected outcome is that the application functions identically to the old, hardcoded version. This validates that the refactoring was successful and no functionality was lost.

- **Step 4.2: Prove Genericity with a New Process**
  - **Timestamp:** 2024-08-28 12:45:00 UTC
  - **What:** Create a new `content_creation.yaml` for a different domain.
  - **How:**
    - **YAML Definition:** Define roles like `Writer`, `Editor` and artifacts like `Draft Article`, `Published Article`.
    - **Execution:** Run the application with this new YAML file.
    - **Validation:** Verify that the UI correctly displays the new roles and artifacts, and that the agents perform their tasks according to the new process definition, all without any new code deployment. This is the critical success metric for the entire project.
