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

---

## 2025-01-09 14:30:00 UTC - Generic BotArmy Implementation Plan

**Goal:** Transform the BotArmy application from a hardcoded SDLC workflow system to a generic, configuration-driven process engine that can handle any well-defined process with specialized roles and artifacts through YAML configuration files.

**Current Architecture Analysis:**
- **Backend**: FastAPI with ControlFlow + Prefect orchestration
- **Frontend**: Next.js with React 19, TypeScript, Zustand state management
- **Agent System**: Hardcoded specialist agents (Analyst, Architect, Developer, Tester, Deployer)
- **Workflow**: Fixed 5-stage SDLC process (Analyze, Design, Build, Validate, Launch)
- **Communication**: WebSocket-based real-time messaging with AG-UI protocol
- **Multi-LLM**: OpenAI, Anthropic Claude, Google Gemini support

**Key Assumptions:**
- The 5-stage process framework (Analyze, Design, Build, Validate, Launch) remains constant
- Only roles and artifacts become configurable/dynamic
- Existing WebSocket infrastructure and agent orchestration patterns are preserved
- YAML configuration will define process patterns, roles, and artifacts
- Backward compatibility with existing SDLC workflow is maintained

---

### **Phase 1: YAML Schema Design & Configuration Parser (2025-01-09 15:00:00 UTC)**

**Objective:** Create a robust, extensible YAML schema for defining processes and implement backend parsing infrastructure.

#### **Step 1.1: Define Process Configuration Schema**
- **Timestamp:** 2025-01-09 15:00:00 UTC
- **What:** Design comprehensive YAML schema for generic process definitions
- **How:** Create formal JSON schema validation for process configurations
- **Location:** `backend/schemas/process_schema.json`
- **Schema Structure:**
  ```yaml
  process_name: string
  description: string
  version: string
  metadata: object
  
  roles:
    - name: string
      description: string (system prompt)
      capabilities: array[string] (tools/skills)
      llm_preferences: object
      stage_involvement: array[string]
  
  artifacts:
    - name: string  
      description: string
      type: string (document|code|data|media)
      path_template: string
      validation_rules: object
      metadata: object
  
  stages:
    Analyze:
      active_roles: array[string]
      input_artifacts: array[string]
      output_artifacts: array[string]
      stage_config: object
    # Similar for Design, Build, Validate, Launch
  
  workflow_config:
    parallel_execution: boolean
    approval_gates: array[string]
    timeout_settings: object
  ```

#### **Step 1.2: Implement Configuration Loader Service**  
- **Timestamp:** 2025-01-09 15:30:00 UTC
- **What:** Create service to load, validate, and manage process configurations
- **How:** Build `ProcessConfigLoader` service with validation and caching
- **Location:** `backend/services/process_config_loader.py`
- **Features:**
  - YAML file parsing and validation
  - Schema compliance checking
  - Configuration caching and hot-reloading
  - Error handling with detailed validation messages
  - Support for configuration inheritance/templates

#### **Step 1.3: Create Default SDLC Configuration**
- **Timestamp:** 2025-01-09 16:00:00 UTC  
- **What:** Convert existing hardcoded SDLC workflow to YAML configuration
- **How:** Extract current agent definitions and workflow logic into `sdlc.yaml`
- **Location:** `backend/configs/processes/sdlc.yaml`
- **Purpose:** Ensure backward compatibility and provide reference implementation

---

### **Phase 2: Backend Architecture Refactoring (2025-01-09 16:30:00 UTC)**

**Objective:** Transform hardcoded workflow engine into generic, configuration-driven orchestration system.

#### **Step 2.1: Create Generic Agent Executor**
- **Timestamp:** 2025-01-09 16:30:00 UTC
- **What:** Replace specific agent classes with configurable generic executor
- **How:** Build `GenericAgentExecutor` class that adapts based on role configuration
- **Location:** `backend/agents/generic_agent_executor.py`
- **Architecture:**
  ```python
  class GenericAgentExecutor:
      def __init__(self, role_config, llm_service, tools_registry):
          self.role_config = role_config
          self.system_prompt = role_config.description
          self.capabilities = tools_registry.get_tools(role_config.capabilities)
          
      async def execute_task(self, context, stage_config):
          # Dynamic task execution based on role configuration
  ```

#### **Step 2.2: Implement Dynamic Workflow Orchestrator**
- **Timestamp:** 2025-01-09 17:00:00 UTC
- **What:** Create generic workflow engine that executes any configured process
- **How:** Build `GenericWorkflowOrchestrator` that processes YAML-defined stages
- **Location:** `backend/workflow/generic_orchestrator.py`
- **Features:**
  - Stage-by-stage execution based on configuration
  - Dynamic agent instantiation per role
  - Artifact dependency resolution
  - Parallel execution support where configured
  - Progress tracking and status broadcasting

#### **Step 2.3: Refactor Data Models**
- **Timestamp:** 2025-01-09 17:30:00 UTC
- **What:** Update database models to support generic processes
- **How:** Modify existing models to store process configuration references
- **Location:** `backend/models/`
- **Changes:**
  - `ProcessRun`: Add config_reference, process_type fields
  - `AgentExecution`: Link to role_name instead of hardcoded agent type
  - `Artifact`: Add type, validation_status, metadata fields
  - Add `ProcessConfiguration` model for configuration management

---

### **Phase 3: Frontend Adaptation (2025-01-09 18:00:00 UTC)**

**Objective:** Transform hardcoded UI into generic interface that adapts to any configured process.

#### **Step 3.1: Create Dynamic Process UI Components**
- **Timestamp:** 2025-01-09 18:00:00 UTC
- **What:** Build configurable UI components that render based on process data
- **How:** Create generic components that populate from backend configuration
- **Location:** `components/process/`
- **Components:**
  - `DynamicRoleCard.tsx` - Displays any configured role
  - `GenericArtifactList.tsx` - Shows artifacts from any process
  - `ConfigurableStageProgress.tsx` - Progress tracking for any workflow
  - `ProcessSelectorModal.tsx` - UI for selecting/uploading process configs

#### **Step 3.2: Update State Management**
- **Timestamp:** 2025-01-09 18:30:00 UTC
- **What:** Modify Zustand stores to handle generic process data
- **How:** Update existing stores to work with dynamic process configurations
- **Location:** `lib/stores/`
- **Changes:**
  - `agent-store.ts`: Support dynamic role lists and statuses
  - `process-store.ts`: New store for managing process configurations
  - `artifact-store.ts`: Enhanced to handle any artifact type

#### **Step 3.3: Implement Process Configuration UI**
- **Timestamp:** 2025-01-09 19:00:00 UTC
- **What:** Create interface for managing and selecting process configurations
- **How:** Build process management page with upload/select/edit capabilities
- **Location:** `app/processes/`
- **Features:**
  - Process template gallery
  - YAML configuration upload
  - Real-time validation feedback
  - Process preview before execution

---

### **Phase 4: Testing and Validation (2025-01-09 19:30:00 UTC)**

**Objective:** Ensure system reliability, backward compatibility, and true genericity.

#### **Step 4.1: Backward Compatibility Validation**
- **Timestamp:** 2025-01-09 19:30:00 UTC
- **What:** Test that existing SDLC workflow functions identically
- **How:** Run comprehensive tests using `sdlc.yaml` configuration
- **Validation Criteria:**
  - All 5 agents execute in proper sequence
  - Generated artifacts match expected output
  - WebSocket communication remains stable
  - UI displays correctly with legacy workflow

#### **Step 4.2: Generic Process Validation**  
- **Timestamp:** 2025-01-09 20:00:00 UTC
- **What:** Prove system works with completely different domain
- **How:** Create and test alternative process configurations
- **Test Cases:**
  - `marketing_campaign.yaml` - Marketing workflow test
  - `research_project.yaml` - Research methodology test  
  - `content_creation.yaml` - Content production workflow
- **Success Metrics:**
  - UI adapts correctly to new roles/artifacts
  - Agents execute tasks according to new configurations
  - No hardcoded assumptions break the system

#### **Step 4.3: Performance and Integration Testing**
- **Timestamp:** 2025-01-09 20:30:00 UTC
- **What:** Ensure system performance and stability with new architecture
- **How:** Load testing and integration validation
- **Tests:**
  - Multiple concurrent processes with different configurations
  - Large configuration file handling
  - WebSocket message throughput with dynamic data
  - Memory usage with cached configurations

---

### **Phase 5: Documentation and Examples (2025-01-09 21:00:00 UTC)**

**Objective:** Provide comprehensive documentation and example configurations for users.

#### **Step 5.1: Configuration Documentation**
- **Timestamp:** 2025-01-09 21:00:00 UTC
- **What:** Create comprehensive guide for creating process configurations
- **Location:** `docs/CONFIGURATION_GUIDE.md`
- **Content:**
  - YAML schema reference
  - Role definition best practices
  - Artifact type specifications
  - Stage configuration options
  - Common patterns and templates

#### **Step 5.2: Example Process Library**
- **Timestamp:** 2025-01-09 21:30:00 UTC
- **What:** Create library of example process configurations
- **Location:** `backend/configs/examples/`
- **Examples:**
  - Software Development (SDLC)
  - Marketing Campaign Planning
  - Research Project Management
  - Content Creation Workflow
  - Customer Support Process
  - Product Launch Planning

---

### **Implementation Notes:**

**New Components to Create:**
1. `ProcessConfigLoader` service for configuration management
2. `GenericAgentExecutor` for role-based agent execution
3. `GenericWorkflowOrchestrator` for process orchestration  
4. Dynamic UI components for process rendering
5. Process configuration management interface

**Files to Modify:**
1. `backend/main.py` - Add process configuration endpoints
2. `backend/workflow.py` - Replace with generic orchestration
3. Frontend stores - Update for dynamic process support
4. Agent-related components - Make them configuration-driven

**Database Changes:**
1. Add process configuration storage
2. Update agent execution tracking
3. Enhance artifact metadata support

**Testing Strategy:**
1. Unit tests for all new configuration handling
2. Integration tests with multiple process types
3. End-to-end tests validating full generic workflows
4. Performance tests for configuration loading and caching

**Rollout Plan:**
1. Implement configuration system alongside existing hardcoded system
2. Test thoroughly with SDLC configuration matching current behavior
3. Gradually migrate UI components to use dynamic data
4. Phase out hardcoded agent implementations
5. Deploy with feature flag for gradual rollout
