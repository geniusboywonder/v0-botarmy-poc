# BotArmy Project Plan - Interactive Workflow Frontend

**Date**: September 5, 2025 (Updated)
**Previous**: September 2, 2025 (Jules - Senior Front-End Developer)
**Role**: AI Senior Full-Stack Developer  
**Project**: v0-botarmy-poc
**Branch**: botarmy-v2.5
**Following**: CODEPROTOCOL, STYLEGUIDE

This plan documents the frontend implementation progress for the interactive workflow and the comprehensive HITL system fixes completed on September 5, 2025.

---

## 1. **Setup and Documentation Update:**

    *   I will first align the project's documentation with the current task. I will overwrite the contents of `docs/PLAN.md` with this new plan.
    *   I will then reset `docs/PROGRESS.md` to indicate the start of the interactive workflow frontend implementation, marking Phase 1 and 2 as complete on the backend.

## 2.  **Phase 3: UI State Integration:**

    *   **Artifact Scaffolding Store:** I will create the `lib/stores/artifact-scaffolding-store.ts` file using Zustand, as specified in `FINALTEST.md`. This store will manage the state of scaffolded artifacts displayed in the UI.
    *   **Interactive Chat Component:** I will create the `components/chat/requirements-gathering-interface.tsx` component. This component will be responsible for handling the interactive question-and-answer session with the user during the requirements gathering phase.

## 3.  **Phase 4: Human-In-the-Loop (HITL) Integration:**

    *   **Approval Notification System:** I will identify the existing notification system and extend it to manage approval requests for HITL checkpoints, including handling timeouts.
    *   **User Approval UI:** I will implement the UI components necessary for the user to view and act on these approval requests (e.g., an "Approve" button in the chat or a notification).

**Implementation Details (Completed on 2025-09-04):**

* **Core HITL Infrastructure:**
  * Created a new Zustand store for managing HITL requests at `lib/stores/hitl-store.ts`.
  * Created the `HITLApprovalComponent` at `components/hitl/hitl-approval.tsx` to be rendered in the chat for approval requests.
  * Integrated the `HITLApprovalComponent` with CopilotKit's `useCopilotAction` and `renderAndWaitForResponse` in `components/chat/copilot-chat.tsx`.
  * Enhanced the agent status card to display a "HITL" badge for pending requests, with navigation to the relevant chat context.

* **User Experience Polish:**
  * Implemented a header alert system (`components/hitl/hitl-alerts.tsx`) to notify users of pending HITL requests.
  * Added "kill switch" controls (`components/controls/kill-switch.tsx`) for pausing, resuming, and stopping agents.
  * Implemented context-aware chat filtering to automatically show messages from the relevant agent when a HITL request is active.

## 4.  **Phase 5: Artifact Management UI:**

    *   **Artifact Display:** I will enhance the UI to display both scaffolded and completed artifacts, organized by their respective stages in the workflow. This will likely involve modifications to the process summary or artifacts page.
    *   **Artifact Interaction:** I will add functionality for users to view and download the generated artifacts.

## 5.  **Testing and Verification:**

    *   As I implement the above features, I will write unit and integration tests for the new components and stores to ensure they are working correctly, following the guidance in `FINALTEST.md`.

## 6.  **Frontend Verification:**

    *   Once the implementation is complete and manually verified, I will use the `frontend_verification_instructions` tool to write a Playwright script, test the end-to-end flow, and generate a screenshot to confirm the UI changes.

---

## **September 5, 2025 - HITL System Comprehensive Fixes**

### **Priority Goal:**

Fix critical HITL system errors and ensure seamless front-end/back-end integration with agent-filtered functionality.

### **Implementation Plan:**

#### **Step 1: Diagnose and Fix Core Error**

* **Issue**: `setAgentFilter is not a function` error preventing HITL alert interactions

* **Root Cause Analysis**: Missing agent filtering functionality in agent store
* **Solution**: Enhance agent store with comprehensive filtering capabilities
* **Code Requirements**:

  ```typescript
  // lib/stores/agent-store.ts enhancements
  interface AgentStore {
    agent: Agent | null              // Currently selected agent
    agentFilter: string             // Current filter string
    setAgentFilter: (filter: string) => void  // Filter setter function
  }
  ```

* **Standards**: Follow existing Zustand patterns, maintain type safety

* **Interdependencies**: Must integrate with existing HITL store and chat components

#### **Step 2: Enhanced HITL Alert Integration**

* **Requirement**: HITL alerts must trigger proper agent filtering and navigation

* **Code Modifications**: Update `components/hitl/hitl-alerts-bar.tsx`
* **Implementation Standards**:
  * Import and use agent store alongside HITL store
  * Maintain existing UI/UX patterns
  * Preserve alert dismissal functionality
* **User Flow**: Click HITL alert → Set agent filter → Navigate to request → Show in chat

#### **Step 3: HITL Badge Enhancement**  

* **Requirement**: Artifact Summary HITL badges must link to agent-specific chat

* **Code Modifications**: Update `components/mockups/enhanced-process-summary.tsx`
* **Implementation Standards**:
  * Integrate agent store without disrupting existing artifact functionality
  * Maintain semantic color classes and design consistency
  * Follow existing badge interaction patterns

#### **Step 4: System Integration Verification**

* **Requirements**: Ensure all HITL system requirements are met:
  1. HITL creation and tracking logged to appropriate stores ✅
  2. Each HITL prompt linked to specific agents ✅  
  3. HITL alerts shown in Alert Bar ✅
  4. HITL badges shown in Artifact Summary ✅
  5. HITL prompts visible in chat only with correct agent filter ✅
  6. No HITL prompts in general/unfiltered chat ✅

### **Technical Architecture:**

**Agent Filtering Flow:**

```
HITL Alert/Badge Click → setAgentFilter(agentName) → navigateToRequest(id) → Chat displays filtered HITL prompt
```

**Cross-Component State Management:**

* HITL Store: Manages request lifecycle and navigation
* Agent Store: Manages agent filtering and selection
* Chat Component: Responds to agent filter changes for HITL display

**File Modifications Required:**

1. `lib/stores/agent-store.ts` - Add agent filtering functionality
2. `components/hitl/hitl-alerts-bar.tsx` - Integrate agent filtering
3. `components/mockups/enhanced-process-summary.tsx` - Integrate agent filtering

### **Quality Standards:**

* **Modularity**: Each component maintains single responsibility

* **Type Safety**: Full TypeScript typing for all new functionality  
* **Error Handling**: Graceful fallbacks for missing data
* **Performance**: Minimal re-renders and efficient state updates
* **UX Consistency**: Follow existing design patterns and interactions

### **Verification Criteria:**

* ✅ No console errors on page load

* ✅ HITL alerts clickable and navigate properly  
* ✅ HITL badges link to correct agent-filtered chat
* ✅ Agent filtering isolates HITL prompts correctly
* ✅ All existing functionality preserved

---

## **September 8, 2025 - SDLC Execution Plan Enhancement**

**Date**: September 8, 2025
**Role**: AI Senior Full-Stack Developer
**Following**: CODEPROTOCOL, STYLEGUIDE
**Goal**: Enhance SDLC.yaml to include mandatory Execution Plans for each phase

### **Task Requirements:**

Adjust the `backend/configs/processes/sdlc.yaml` configuration so that the first artifact produced in each phase is an **Execution Plan** for that phase. The Execution Plan should:

1. **Summarize the artifacts to be produced in that phase**
2. **Detail a step-by-step guide to produce the remaining artifacts required**
3. **Be completed before any other artifacts can be produced in that phase**
4. **Be required as input for all other artifacts in that phase**

### **Implementation Plan:**

#### **Step 1: Analysis of Current SDLC Structure**

* **Current Phases**: Analyze → Design → Build → Validate → Launch

* **Current Flow**: Each phase produces one artifact directly
* **Required Change**: Each phase must first produce an Execution Plan, then use that plan to produce the main artifact

#### **Step 2: YAML Structure Enhancement**

* **Standards**: Maintain existing YAML structure and validation

* **Enhancement**: Add Execution Plan tasks as first step in each phase
* **Dependencies**: Create proper dependency chains (Execution Plan → Main Artifact)

#### **Step 3: Orchestrator Integration**

* **Code Requirements**: Update `openai_agents_orchestrator.py` to handle new task structure

* **Implementation Standards**:
  * Parse enhanced YAML configuration with multiple tasks per stage
  * Execute tasks in proper dependency order
  * Maintain existing agent role assignments
* **Interdependencies**: Must work with current LLMService and status broadcasting

#### **Step 4: Agent Role Enhancement**

* **Requirement**: Each agent must be capable of producing both Execution Plans and main artifacts

* **Implementation**: Update agent descriptions to handle planning and execution phases
* **Quality Standards**: Maintain role-specific expertise while adding planning capabilities

### **Technical Architecture:**

**Enhanced YAML Structure:**

```yaml
stages:
  Analyze:
    description: "Analyze the project brief and create a requirements document."
    tasks:
      - name: "Create Analysis Execution Plan"
        role: "Analyst"
        input_artifacts: ["Project Brief"]
        output_artifacts: ["Analysis Execution Plan"]
      - name: "Execute Requirements Analysis"
        role: "Analyst"  
        input_artifacts: ["Project Brief", "Analysis Execution Plan"]
        output_artifacts: ["Requirements Document"]
        depends_on: ["Create Analysis Execution Plan"]
```

**Orchestrator Enhancement Flow:**

```
Phase Start → Create Execution Plan → Execute Plan → Produce Main Artifact → Next Phase
```

### **File Modifications Required:**

1. **`backend/configs/processes/sdlc.yaml`**
   * Add Execution Plan tasks to each stage
   * Update artifact definitions
   * Establish proper dependency chains

2. **`backend/workflow/openai_agents_orchestrator.py`**
   * Enhance to handle multiple tasks per stage
   * Implement dependency resolution
   * Maintain agent role assignments

3. **Agent Role Descriptions** (within YAML)
   * Update each role to handle both planning and execution
   * Maintain role-specific expertise
   * Add execution plan creation capabilities

### **Quality Standards:**

* **YAML Validation**: Must pass existing schema validation

* **Backward Compatibility**: Existing orchestrator patterns preserved
* **Agent Expertise**: Role-specific knowledge maintained in both planning and execution
* **Dependency Management**: Clear task ordering and artifact flow
* **Error Handling**: Graceful handling of missing execution plans

### **Verification Criteria:**

* ✅ YAML configuration validates successfully

* ✅ Orchestrator processes enhanced workflow correctly
* ✅ Each phase produces Execution Plan before main artifact
* ✅ Execution Plans contain detailed step-by-step guides
* ✅ Main artifacts reference and utilize their Execution Plans
* ✅ All existing functionality preserved
* ✅ Agent status broadcasting works with enhanced workflow

### **Implementation Steps:**

1. **Analyze Current YAML Structure** - Understand existing configuration format
2. **Design Enhanced YAML Schema** - Plan new structure with Execution Plans
3. **Update SDLC Configuration** - Implement enhanced YAML with proper dependencies  
4. **Enhance Orchestrator Logic** - Update to handle multiple tasks per stage
5. **Test and Verify** - Ensure workflow executes properly with new structure
6. **Documentation Update** - Update progress and plan documentation

### **Assumptions:**

* Existing agent roles (Analyst, Architect, Developer, Tester, Deployer) remain unchanged

* Current orchestrator architecture can be enhanced rather than replaced
* YAML configuration format supports nested task structures
* LLMService integration remains the same for individual agent callsa
