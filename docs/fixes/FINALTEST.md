# FINALTEST.md - Interactive SDLC Workflow Implementation Plan

**Date**: September 2, 2025  
**Role**: Backend Engineer  
**Project**: v0-botarmy-poc  
**Following**: CODEPROTOCOL compliance - No code written during planning phase

---

## Progress Update (As of 2025-09-02)

The backend implementation for the interactive workflow is largely complete. The following key components have been developed and tested:

*   **Database and Migrations:** A SQLite database with `Alembic` for migrations has been set up. The necessary tables (`workflow_sessions`, `hitl_checkpoints`, `artifacts_scaffolded`) have been created.
*   **Enhanced YAML Configuration:** The configuration system now supports template and role inheritance. New schemas have been created and the main process schema has been extended. The `interactive_sdlc.yaml` has been created.
*   **Interactive Backend Logic:** The `InteractiveWorkflowOrchestrator` and `InteractiveAgentExecutor` have been implemented to handle the new interactive flow. A new WebSocket endpoint (`/ws/interactive/{session_id}`) has been added to trigger this workflow.
*   **Backend Testing:** Unit and integration tests for the new components have been created and are passing. Several broken tests in the existing test suite have also been repaired.

**Outstanding Work:**

*   **Frontend Integration (Phase 3-5):** The UI for requirements gathering, user approvals, and artifact display needs to be built.
*   **Full HITL Implementation:** The backend logic for handling user responses to HITL checkpoints needs to be fully implemented.
*   **Full Test Suite Pass:** A persistent caching issue in the test environment is preventing a full `pytest` run. The new components have been tested individually.

---

## Executive Summary

Implementation plan for the 10-step interactive workflow that **extends** the existing sophisticated YAML-driven architecture discovered through proper codebase analysis.

---

## Architecture Discovery Results ✅

### **Existing YAML-Driven System (Must Preserve & Extend)**

**Process Configuration System:**
- `/backend/configs/processes/sdlc.yaml` - Complete role/stage/task definitions
- `/backend/services/process_config_loader.py` - Dynamic YAML loading with caching
- `/backend/schemas/process_schema.json` - JSON Schema validation
- `/backend/workflow/generic_orchestrator.py` - YAML-based workflow execution

**Agent Execution System:**
- `/backend/agents/generic_agent_executor.py` - Role-agnostic agent with security
- Role definitions loaded from YAML with flexible prompts
- Input sanitization and security pattern detection
- Multi-LLM provider support with connection pooling

**Current Workflow Flow:**
1. Load YAML config via `ProcessConfigLoader`
2. Execute stages via `generic_orchestrator.py`
3. Each task uses `GenericAgentExecutor` with role-specific prompts
4. Artifacts created based on YAML `output_artifacts` definitions
5. Real-time updates via `AgentStatusBroadcaster`

---

## Complete 10-Step Interactive Workflow Process

### **Detailed Step-by-Step Flow**

**Step 1: User Project Submission**
- User submits project prompt through chat interface
- System receives prompt and validates input using existing InputSanitizer
- Session ID generated and workflow initiated with selected process configuration
- Status: "Project submitted, analyzing requirements..."

**Step 2: Interactive Requirements Gathering**
- Analyst agent analyzes project brief using YAML-defined prompts
- System generates 3-5 clarifying questions based on project complexity
- Questions sent to chat interface with timeout mechanism (10 minutes default)
- User responds to questions in real-time through chat
- If timeout occurs: System proceeds with stated assumptions
- Status: "Requirements gathering in progress..."

**Step 3: Product Spec Document (PSD) Generation**
- Analyst processes user responses and generates comprehensive PSD.md
- PSD includes: Executive Summary, User Stories, Functional Requirements, Non-Functional Requirements
- PSD.md artifact appears in Plan Stage with real-time progress updates
- Document saved to session-specific directory: `artifacts/{session_id}/psd.md`
- Status: "Product specification document created"

**Step 4: Execution Plan & Artifact Scaffolding**
- System analyzes PSD and determines required artifacts for all stages
- Execution Plan generated showing all stages and their deliverables
- UI populates with scaffolded artifacts across all stages (Plan, Design, Build, Test, Deploy)
- Each stage shows placeholder artifacts that will be created
- Artifact placeholders include: Architecture Document, Implementation Plan, Test Plan, Deployment Plan
- Status: "Execution plan created, artifacts scaffolded"

**Step 5: User Approval Checkpoint**
- System pauses workflow and requests user confirmation in chat
- User reviews PSD and execution plan through UI
- Chat message: "Please review the Product Specification and Execution Plan. Type 'approve' to continue or provide feedback for changes."
- User can: Approve, Request modifications, or Ask questions
- If approved: Workflow continues to stage execution
- If modifications requested: Return to appropriate step for refinement
- Status: "Awaiting user approval to begin execution..."

**Step 6: Sequential Stage Execution**
- Workflow proceeds through stages using existing orchestrator: Plan → Design → Build → Test → Deploy
- Each stage agent receives PSD and execution plan as context
- Real-time artifact creation with progress tracking
- Each completed artifact updates UI immediately
- Stage progression follows YAML-defined dependencies
- Status updates: "Design stage in progress...", "Build stage completed...", etc.

**Step 7: Real-Time UI Synchronization**
- WebSocket broadcasts every stage transition and artifact update
- Process Summary shows current active stage with connecting lines
- Activity Timeline displays real-time agent actions and completions
- Artifact panels update with download links as documents are completed
- Progress bars show completion percentage for each stage
- Status: Continuous real-time updates throughout execution

**Step 8: Process Completion Notification**
- When final stage (Deploy) completes, system generates completion notification
- Notification appears in notification area: "Project completed successfully"
- Chat receives final message: "Your project has been completed. All artifacts are available for download."
- Process Summary shows all stages as completed with success indicators
- Final status: "Project completed - all deliverables ready"

**Step 9: HITL Intervention Capabilities (Available Throughout)**
- At ANY point during execution, agents can request human assistance
- Intervention triggers appear in notification area with stage context
- Examples: "Architect needs clarification on database requirements", "Tester requires additional test scenarios"
- Chat receives agent questions with full context
- User can provide guidance or request workflow pause
- Workflow resumes after HITL resolution
- Status: "Workflow paused - awaiting human input" (when interventions occur)

**Step 10: Complete Artifact Availability**
- All generated artifacts accessible through UI download links
- Artifacts organized by stage in Process Summary interface
- Complete artifact set includes:
  - Product Specification Document (PSD.md)
  - Architecture Design Document
  - Implementation Plan with code examples
  - Comprehensive Test Plan
  - Deployment Strategy and scripts
- File system storage: `artifacts/{session_id}/` with stage subdirectories
- Artifacts remain available for session lifetime plus retention period
- Status: "All artifacts available for download"

### **Process Flow Visualization**

```
User Input → Requirements Q&A → PSD Generation → Execution Planning → User Approval
    ↓                                                                        ↓
Artifact Access ← Completion Notify ← Real-time Updates ← Stage Execution ←─┘
    ↑                                        ↑
HITL Available Throughout ──────────────────┘
```

### **Key Integration Points with Existing Architecture**

- **YAML Configuration**: Process behavior defined in `interactive_sdlc.yaml`
- **Existing Agents**: All stage agents (Analyst, Architect, Developer, Tester, Deployer) used unchanged
- **Security**: All user inputs processed through existing InputSanitizer
- **Real-time Updates**: Existing AgentStatusBroadcaster handles all UI synchronization
- **Artifact Storage**: Uses existing artifact management with YAML-defined path templates
- **Error Handling**: Existing error recovery and graceful degradation mechanisms maintained

## Configuring Alternative Workflow Patterns

### **The 10-Step Process is NOT Mandatory - Complete Flexibility via YAML**

The interactive 10-step process is just **one configuration option**. The YAML-driven architecture supports any workflow pattern:

### **1. Simplified 3-Step Process (Quick Turnaround)**

```yaml
# backend/configs/processes/quick_analysis.yaml
process_name: "Quick Analysis Workflow"
version: "1.0.0"

# DISABLE interactive features entirely
interactive_config:
  requirements_gathering:
    enabled: false                    # No Q&A session
  hitl_checkpoints: []               # No approval gates
  artifact_scaffolding:
    auto_create_placeholders: false   # No UI scaffolding

stages:
  Analyze:
    description: "Direct analysis from brief"
    tasks:
      - name: "Analyze Brief"
        role: "Analyst"
        input_artifacts: ["Project Brief"]
        output_artifacts: ["Analysis Report"]
        
  Recommend:
    description: "Generate recommendations"  
    tasks:
      - name: "Create Recommendations"
        role: "Consultant"
        depends_on: ["Analyze Brief"]
        
  Deliver:
    description: "Package final deliverable"
    tasks:
      - name: "Final Report"
        role: "Report Generator"
        depends_on: ["Create Recommendations"]

# Result: Simple linear workflow, no interaction, no scaffolding
```

### **2. Research-Only Process (No Development Stages)**

```yaml  
# backend/configs/processes/market_research.yaml
process_name: "Market Research Analysis"

interactive_config:
  requirements_gathering:
    enabled: true
    max_questions: 2              # Minimal Q&A
    timeout_minutes: 5            # Quick timeout
  hitl_checkpoints:
    - stage: "Validation"         # Single checkpoint only
      required: true

stages:
  Research:
    description: "Market data collection"
    tasks:
      - name: "Data Collection"
        role: "Research Analyst"
        
  Analysis:
    description: "Data analysis and insights"
    tasks:
      - name: "Statistical Analysis"
        role: "Data Analyst"
        
  Validation:
    description: "Expert review"
    tasks:
      - name: "Expert Review"
        role: "Senior Analyst"

# Result: Research workflow with minimal interaction
```

### **3. Human-Heavy Process (Maximum HITL)**

```yaml
# backend/configs/processes/legal_review.yaml
process_name: "Legal Document Review"

interactive_config:
  requirements_gathering:
    enabled: true
    max_questions: 10             # Extensive Q&A
    timeout_minutes: 60           # Long timeout for complex cases
    auto_proceed_on_timeout: false # NEVER proceed without human input
    
  hitl_checkpoints:
    - stage: "Initial_Review"     # Checkpoint after every stage
      required: true
      timeout_minutes: 240        # 4 hours for review
    - stage: "Legal_Analysis" 
      required: true
      timeout_minutes: 480        # 8 hours for complex analysis
    - stage: "Risk_Assessment"
      required: true
      timeout_minutes: 120
    - stage: "Final_Approval"
      required: true
      timeout_minutes: 1440       # 24 hours for final approval

# Result: Human-controlled workflow with extensive oversight
```

### **4. Automated Pipeline (Zero Interaction)**

```yaml
# backend/configs/processes/automated_deployment.yaml
process_name: "Automated CI/CD Pipeline"

# COMPLETELY DISABLE all interactive features
interactive_config:
  requirements_gathering:
    enabled: false
  hitl_checkpoints: []
  artifact_scaffolding:
    auto_create_placeholders: false

workflow_config:
  parallel_execution: true        # Enable parallel stages
  auto_progress: true            # No human input required
  error_handling: "continue"     # Continue on non-critical errors

stages:
  Build:
    tasks:
      - name: "Compile Code"
        role: "Build Agent"
  Test:  
    tasks:
      - name: "Run Tests"
        role: "Test Agent"
  Deploy:
    tasks:
      - name: "Deploy to Production"
        role: "Deploy Agent"

# Result: Fully automated pipeline, no human interaction
```

### **5. Creative Process (Different Agent Types)**

```yaml
# backend/configs/processes/content_creation.yaml
process_name: "Content Creation Workflow"

interactive_config:
  requirements_gathering:
    enabled: true
    max_questions: 3
    context_prompt: |
      You are helping create content. Ask about target audience, 
      tone, and key messaging requirements.
  
  hitl_checkpoints:
    - stage: "Creative_Review"
      required: true
      timeout_minutes: 30

roles:
  - name: "Content Strategist"
    description: "Develops content strategy and messaging framework..."
    stage_involvement: ["Strategy"]
    
  - name: "Copywriter" 
    description: "Creates engaging written content..."
    stage_involvement: ["Writing"]
    
  - name: "Creative Director"
    description: "Reviews and approves creative work..."
    stage_involvement: ["Review"]

stages:
  Strategy:
    tasks:
      - name: "Content Strategy"
        role: "Content Strategist"
  Writing:
    tasks:
      - name: "Draft Content"  
        role: "Copywriter"
  Review:
    tasks:
      - name: "Creative Review"
        role: "Creative Director"

# Result: Creative workflow with different agents and review gates
```

## **Flexibility Configuration Matrix**

| Feature | Disable Method | Use Case |
|---------|---------------|----------|
| **Requirements Q&A** | `requirements_gathering.enabled: false` | Pre-defined requirements |
| **HITL Checkpoints** | `hitl_checkpoints: []` | Fully automated workflows |
| **Artifact Scaffolding** | `auto_create_placeholders: false` | Simple output processes |
| **10-Step Process** | Use different `stages` configuration | Any non-SDLC workflow |
| **Interactive Features** | Don't use `interactive_sdlc.yaml` | Legacy/existing processes |

## **Process Selection Implementation**

### **Frontend Process Selection**

```typescript
// app/components/process-selector.tsx
const processOptions = [
  {
    id: 'interactive_sdlc',
    name: 'Interactive Software Development',
    description: 'Full 10-step SDLC with Q&A and approvals',
    complexity: 'high',
    duration: '30-60 minutes'
  },
  {
    id: 'quick_analysis', 
    name: 'Quick Analysis',
    description: 'Fast 3-step analysis workflow',
    complexity: 'low',
    duration: '5-10 minutes'
  },
  {
    id: 'market_research',
    name: 'Market Research',
    description: 'Research-focused workflow',
    complexity: 'medium', 
    duration: '15-30 minutes'
  },
  {
    id: 'automated_deployment',
    name: 'Automated Pipeline',
    description: 'Zero-interaction CI/CD process',
    complexity: 'low',
    duration: '2-5 minutes'
  }
]

// User selects process type before starting
function ProcessSelector({ onSelect }: { onSelect: (processId: string) => void }) {
  return (
    <div className="grid grid-cols-2 gap-4">
      {processOptions.map(process => (
        <ProcessCard 
          key={process.id}
          process={process}
          onClick={() => onSelect(process.id)}
        />
      ))}
    </div>
  )
}
```

### **Backend Process Routing**

```python
# backend/main.py - Enhanced routing
@app.websocket("/ws/{process_type}/{session_id}")
async def dynamic_websocket_endpoint(
    websocket: WebSocket, 
    process_type: str,
    session_id: str
):
    # Route to appropriate orchestrator based on process type
    if process_type in ['interactive_sdlc', 'legal_review', 'market_research']:
        # Use interactive orchestrator
        orchestrator = InteractiveWorkflowOrchestrator(config_loader, broadcaster)
        await orchestrator.execute_interactive_workflow(process_type, brief, session_id)
    else:
        # Use standard orchestrator for simple processes  
        await generic_workflow(process_type, brief, session_id, broadcaster)
```

## **Migration Strategy for Existing Projects**

### **Gradual Adoption Path**

```bash
# Phase 1: Add to existing projects without changing behavior
1. Deploy enhanced system with feature flags OFF
2. Existing workflows continue using standard orchestrator
3. New interactive processes available as opt-in

# Phase 2: Selective enablement  
4. Enable interactive features for specific project types
5. Marketing teams use content_creation.yaml
6. Engineering teams can choose interactive_sdlc.yaml or standard sdlc.yaml

# Phase 3: Full flexibility
7. All teams have access to full process library
8. Custom processes can be created per project needs
9. Template inheritance allows rapid process creation
```

**Key Point**: The 10-step interactive process is **one option** in a flexible system. Teams can use:
- **Standard SDLC** (existing workflow, unchanged)
- **Interactive SDLC** (new 10-step process) 
- **Quick Analysis** (3-step simplified)
- **Custom Processes** (any configuration needed)

The YAML architecture ensures any workflow pattern is possible while maintaining the same underlying orchestration engine.

---

## Enhanced Flexibility & Extensibility Design

### **Multi-Process & Multi-Industry Support**

The implementation ensures maximum flexibility for different industries, roles, and workflows:

**1. Process Template Inheritance System**

```yaml
# backend/configs/templates/base_interactive.yaml
template_name: "Interactive Process Template"
extends: null
default_interactive_config:
  requirements_gathering:
    enabled: true
    max_questions: 5
    timeout_minutes: 10
  hitl_checkpoints: []
  artifact_scaffolding:
    auto_create_placeholders: true

# Industry-specific processes can extend base templates
# backend/configs/processes/marketing_campaign.yaml
extends: "base_interactive"
process_name: "Marketing Campaign Launch"
interactive_config:
  hitl_checkpoints:
    - stage: "Creative Review"
      required: true
      timeout_minutes: 30
```

**2. Role Behavior Profiles**

```yaml
# backend/configs/role_profiles/strategic_role.yaml
profile_name: "Strategic Role"
question_patterns:
  - "What are the key objectives for..."
  - "What constraints should we consider..."
  - "What success metrics should we track..."
default_timeout: 15
escalation_behavior: "request_approval"

# Roles inherit behavior patterns
roles:
  - name: "Marketing Strategist"
    extends: "strategic_role"
    custom_prompt: "Focus on brand positioning and market penetration..."
```

**3. Industry Process Libraries**

```
backend/configs/industry_packs/
├── software_development/
│   ├── agile_sdlc.yaml
│   ├── devops_pipeline.yaml
│   └── security_review.yaml
├── marketing/
│   ├── campaign_launch.yaml
│   ├── brand_strategy.yaml
│   └── content_calendar.yaml
├── legal/
│   ├── contract_review.yaml
│   ├── compliance_audit.yaml
│   └── ip_analysis.yaml
└── finance/
    ├── budget_planning.yaml
    ├── risk_assessment.yaml
    └── audit_process.yaml
```

## Implementation Strategy (Extending YAML Architecture)

### **Phase 1: Enhanced YAML Configuration & Flexibility (Week 1) [COMPLETED]**

**Task 1.1: Create Interactive YAML Config**
```yaml
# backend/configs/processes/interactive_sdlc.yaml
process_name: "Interactive SDLC with Requirements Gathering"
version: "2.0.0"

# NEW: Interactive behaviors section
interactive_config:
  requirements_gathering:
    enabled: true
    max_questions: 5
    timeout_minutes: 10
    auto_proceed_on_timeout: true
    
  hitl_checkpoints:
    - stage: "Analyze" 
      required: true
      timeout_minutes: 30
    - stage: "Design"
      required: false
      
  artifact_scaffolding:
    auto_create_placeholders: true
    ui_integration: true

# Enhanced artifact definitions with UI integration
artifacts:
  - name: "Product Spec Document (PSD)"
    description: "Interactive requirements gathering output"
    type: "document" 
    path_template: "artifacts/{{session_id}}/psd.md"
    ui_stage: "Plan"
    scaffold_template: "templates/psd_scaffold.md"
```

**Task 1.2: Template Inheritance System**

Create template loading and inheritance capability in ProcessConfigLoader:

```python
# backend/services/enhanced_process_config_loader.py
class EnhancedProcessConfigLoader(ProcessConfigLoader):
    def __init__(self):
        super().__init__()
        self.template_dir = "backend/configs/templates"
        self.role_profiles_dir = "backend/configs/role_profiles"
    
    def load_with_inheritance(self, config_name: str):
        # Load base config
        config = self.get_config(config_name)
        
        # Check for 'extends' property
        if 'extends' in config:
            template = self._load_template(config['extends'])
            config = self._merge_configs(template, config)
            
        # Process role inheritance
        if 'roles' in config:
            config['roles'] = self._process_role_inheritance(config['roles'])
            
        return config
```

**Task 1.3: Update JSON Schema for Flexibility**

- Extend `/backend/schemas/process_schema.json` to support:
  - `extends` property for template inheritance
  - `interactive_config` with flexible checkpoint definitions
  - Role profile references and inheritance
  - Industry pack validation
- Add new schemas:
  - `/backend/schemas/template_schema.json` - Template validation
  - `/backend/schemas/role_profile_schema.json` - Role profile validation

**Task 1.4: Industry Process Library Structure**

Create organized process library with validation:

```bash
backend/configs/
├── templates/           # Base templates
├── role_profiles/       # Reusable role behaviors  
├── industry_packs/      # Industry-specific processes
│   ├── software_development/
│   ├── marketing/
│   ├── legal/
│   └── finance/
└── processes/          # Active process configurations
```

### **Phase 2: Interactive Agent Enhancement (Week 1-2) [COMPLETED]**

**Task 2.1: Extend GenericAgentExecutor**
```python
# backend/agents/interactive_agent_executor.py
class InteractiveAgentExecutor(GenericAgentExecutor):
    """Extends existing GenericAgentExecutor with interactive capabilities"""
    
    def __init__(self, role_config: dict, status_broadcaster, interactive_config: dict = None):
        super().__init__(role_config, status_broadcaster)
        self.interactive_config = interactive_config or {}
    
    async def execute_requirements_gathering(self, project_brief: str, session_id: str):
        # Use existing LLM service + security sanitization
        # Add Q&A session management
        # Generate PSD using YAML-defined role prompts
        pass
    
    async def scaffold_artifacts(self, artifact_configs: list, session_id: str):
        # Create UI-visible artifact placeholders
        # Use existing status_broadcaster for real-time updates
        pass
```

**Task 2.2: Enhance Workflow Orchestrator** 
```python
# backend/workflow/interactive_orchestrator.py  
class InteractiveWorkflowOrchestrator:
    """Extends existing generic_orchestrator with interactive features"""
    
    def __init__(self, config_loader: ProcessConfigLoader, status_broadcaster):
        self.config_loader = config_loader  # Use existing loader
        self.status_broadcaster = status_broadcaster
        
    async def execute_interactive_workflow(self, config_name: str, project_brief: str, session_id: str):
        # Load config using existing ProcessConfigLoader
        config = self.config_loader.get_config(config_name)
        
        # Step 1: User input (received)
        # Step 2: Interactive requirements gathering
        if config.get('interactive_config', {}).get('requirements_gathering', {}).get('enabled'):
            await self._handle_requirements_gathering(config, project_brief, session_id)
            
        # Step 3-10: Continue with existing orchestrator pattern
        return await self._execute_standard_workflow(config, session_id)
```

### **Phase 3: UI State Integration (Week 2-3)**

**Task 3.1: Artifact Scaffolding System**
```typescript
// lib/stores/artifact-scaffolding-store.ts
interface ScaffoldedArtifact {
  id: string
  name: string
  stage: string
  status: 'scaffolded' | 'in_progress' | 'completed'
  progress: number
  session_id: string
}

export const useArtifactScaffoldingStore = create<ArtifactScaffoldingState>((set, get) => ({
  artifacts: {},
  createScaffold: (artifact: ScaffoldedArtifact) => {
    // Real-time artifact placeholder creation
  },
  updateProgress: (artifactId: string, progress: number) => {
    // Real-time progress updates
  }
}))
```

**Task 3.2: Interactive Chat Enhancement**
```typescript
// components/chat/requirements-gathering-interface.tsx
export function RequirementsGatheringInterface() {
  // Interactive Q&A session management
  // Integration with existing WebSocket service
  // Real-time question/response handling
}
```

### **Phase 4: HITL Integration (Week 3-4)**

**Task 4.1: Enhanced Notification System**
- Extend existing notification system with approval workflows  
- Add timeout handling for HITL checkpoints
- Integrate with existing WebSocket broadcasting

**Task 4.2: User Control Enhancement**
- Build on existing pause/resume agent functionality
- Add approval checkpoint UI components
- Maintain existing stop/start workflow controls

### **Phase 5: Artifact Management (Week 4-5)**  

**Task 5.1: File System Integration**
- Use YAML-defined path_templates for artifact storage
- Create artifacts in session-specific directories
- Integrate with existing artifact serving endpoints

**Task 5.2: UI Artifact Display**
- Real-time artifact creation in Process Summary
- Stage-specific artifact organization 
- Download/view functionality for completed artifacts

### **Phase 6: Testing & Integration (Week 5-6)**

**Task 6.1: YAML Configuration Testing**
- Validate interactive_sdlc.yaml against schema
- Test backward compatibility with existing sdlc.yaml
- End-to-end workflow testing

**Task 6.2: Integration Testing**  
- Test with existing WebSocket system
- Validate real-time UI updates
- Test HITL intervention scenarios

---

## Key Implementation Principles

### **1. Preserve Existing Architecture**
- **NO REPLACEMENT** of existing YAML system
- **EXTEND** GenericAgentExecutor, don't rebuild
- **REUSE** ProcessConfigLoader and validation system
- **MAINTAIN** existing WebSocket/broadcasting infrastructure

### **2. YAML-First Configuration**
- All interactive behaviors defined in YAML
- JSON Schema validation for new properties
- Backward compatibility with existing configs
- Dynamic loading using existing ProcessConfigLoader

### **3. Security & Performance**
- Use existing InputSanitizer for all user inputs
- Leverage existing connection pooling
- Maintain existing rate limiting
- Extend existing error handling patterns

### **4. UI Integration Strategy**
- Build on existing Zustand stores
- Use existing WebSocket service
- Extend existing shadcn/ui components
- Maintain existing responsive design patterns

---

## Risk Mitigation

### **Technical Risks**
- **Breaking Existing Workflow**: Maintain strict backward compatibility
- **YAML Complexity**: Use JSON Schema validation for safety
- **Performance Impact**: Leverage existing connection pooling and optimization

### **Integration Risks**  
- **WebSocket Stability**: Build on existing EnhancedConnectionManager
- **State Management**: Extend existing Zustand patterns
- **Component Integration**: Use existing component library

### **User Experience Risks**
- **Session Management**: Use existing session handling patterns
- **Error Recovery**: Build on existing error handling system
- **Timeout Handling**: Implement graceful fallbacks with existing notification system

---

## Success Metrics

### **Functional Requirements Met**
- ✅ Interactive requirements gathering with Q&A
- ✅ Real-time artifact scaffolding in UI  
- ✅ HITL approval checkpoints
- ✅ Complete workflow execution
- ✅ Artifact availability and download

### **Technical Requirements Met**
- ✅ YAML-driven configuration preserved and extended
- ✅ Existing security and performance features maintained
- ✅ Backward compatibility with current workflows
- ✅ Real-time UI updates via existing WebSocket system

### **Quality Metrics**
- **Configuration Validation**: 100% YAML configs pass JSON Schema validation
- **Backward Compatibility**: Existing sdlc.yaml workflow unchanged
- **Performance**: No degradation in existing workflow execution times
- **Security**: All new inputs validated using existing InputSanitizer

---

## Comprehensive Developer Implementation Guide

### **Pre-Implementation Setup**

**Environment Preparation:**

```bash
# 1. Create feature branch
git checkout -b feature/interactive-workflow-system

# 2. Backup existing configs
cp -r backend/configs backend/configs.backup

# 3. Verify existing system works
python backend/main.py  # Test existing workflow
npm run test           # Run existing tests
```

**Development Dependencies:**

```bash
# Backend - Add to requirements.txt if needed
pip install jsonschema>=4.0.0  # Already exists for validation
pip install pyyaml>=6.0        # Already exists for YAML parsing

# Frontend - Already exists in package.json
npm install zustand             # State management
npm install @radix-ui/react-*   # UI components
```

### **Implementation Phase Details**

**Phase 1 Implementation Checklist:**

```bash
# Week 1 - Day 1-2: Schema & Template System
[ ] Create template_schema.json with inheritance validation
[ ] Create role_profile_schema.json for role behavior validation  
[ ] Extend process_schema.json with interactive_config properties
[ ] Test schema validation with sample configs

# Week 1 - Day 3-4: Enhanced Config Loader
[ ] Implement EnhancedProcessConfigLoader inheritance logic
[ ] Add template loading and merging functionality
[ ] Add role profile inheritance processing
[ ] Create unit tests for config inheritance

# Week 1 - Day 5-7: Industry Process Library
[ ] Create directory structure for industry_packs
[ ] Implement sample processes (marketing, legal, finance)
[ ] Create base templates (interactive, analytical, creative)
[ ] Validate all configs against schemas
```

**Phase 2 Implementation Checklist:**

```bash
# Week 2 - Day 1-3: Agent Enhancement
[ ] Create InteractiveAgentExecutor extending GenericAgentExecutor
[ ] Implement requirements gathering with Q&A session management
[ ] Add artifact scaffolding capabilities with real-time broadcasting
[ ] Test with existing LLM service and security features

# Week 2 - Day 4-5: Workflow Orchestrator
[ ] Create InteractiveWorkflowOrchestrator extending generic_orchestrator
[ ] Implement 10-step workflow execution logic
[ ] Add HITL checkpoint handling with timeouts
[ ] Integration with existing AgentStatusBroadcaster

# Week 2 - Day 6-7: Integration Testing
[ ] End-to-end testing of interactive workflow
[ ] Backward compatibility testing with existing sdlc.yaml
[ ] Performance testing with multiple concurrent sessions
```

### **Critical Integration Points**

**1. Existing System Integration:**

```python
# main.py integration point
from backend.workflow.interactive_orchestrator import InteractiveWorkflowOrchestrator
from backend.services.enhanced_process_config_loader import EnhancedProcessConfigLoader

# Maintain existing endpoints while adding new ones
@app.websocket("/ws/interactive/{session_id}")
async def interactive_websocket_endpoint(websocket: WebSocket, session_id: str):
    # Use enhanced orchestrator for interactive processes
    pass

@app.websocket("/ws/{session_id}")  # Keep existing endpoint unchanged
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    # Existing functionality unchanged
    pass
```

**2. Database Integration Requirements:**

```sql
-- New tables for session management
CREATE TABLE workflow_sessions (
    id UUID PRIMARY KEY,
    process_name VARCHAR(100),
    session_type ENUM('standard', 'interactive'),
    current_stage VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE hitl_checkpoints (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES workflow_sessions(id),
    stage_name VARCHAR(50),
    status ENUM('pending', 'approved', 'rejected', 'timeout'),
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);

CREATE TABLE artifacts_scaffolded (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES workflow_sessions(id),
    artifact_name VARCHAR(200),
    stage_name VARCHAR(50),
    status ENUM('scaffolded', 'in_progress', 'completed'),
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**3. Frontend Integration Points:**

```typescript
// New store integration
// lib/stores/interactive-workflow-store.ts
interface InteractiveWorkflowState {
  currentSession: WorkflowSession | null
  pendingApprovals: HITLCheckpoint[]
  scaffoldedArtifacts: ScaffoldedArtifact[]
  requirementQuestions: Question[]
  userResponses: Record<string, string>
}

// Component integration points
// app/page.tsx - Add process selection
const processOptions = [
  { value: 'sdlc', label: 'Standard SDLC' },
  { value: 'interactive_sdlc', label: 'Interactive SDLC' },
  { value: 'marketing_campaign', label: 'Marketing Campaign' },
]
```

### **Testing Strategy Implementation**

**1. Unit Tests (Required):**

```bash
# Backend tests to create
backend/tests/services/test_enhanced_process_config_loader.py
backend/tests/agents/test_interactive_agent_executor.py
backend/tests/workflow/test_interactive_orchestrator.py
backend/tests/schemas/test_config_inheritance.py

# Frontend tests to create
components/chat/requirements-gathering-interface.test.tsx
lib/stores/interactive-workflow-store.test.ts
hooks/use-interactive-session.test.ts
```

**2. Integration Tests (Critical):**

```bash
# Full workflow integration
backend/tests/integration/test_interactive_workflow_end_to_end.py
backend/tests/integration/test_backward_compatibility.py
backend/tests/integration/test_multi_process_support.py

# Frontend integration  
tests/e2e/interactive-workflow.spec.ts
tests/e2e/process-selection.spec.ts
tests/e2e/hitl-approval-flow.spec.ts
```

### **Deployment Considerations**

**1. Feature Flags Implementation:**

```python
# backend/feature_flags.py
class FeatureFlags:
    INTERACTIVE_WORKFLOWS = os.getenv('ENABLE_INTERACTIVE_WORKFLOWS', 'false').lower() == 'true'
    PROCESS_TEMPLATES = os.getenv('ENABLE_PROCESS_TEMPLATES', 'false').lower() == 'true'
    INDUSTRY_PACKS = os.getenv('ENABLE_INDUSTRY_PACKS', 'false').lower() == 'true'

# Gradual rollout strategy
if FeatureFlags.INTERACTIVE_WORKFLOWS:
    # Load interactive features
    pass
```

**2. Migration Strategy:**

```bash
# Database migrations
alembic revision -m "Add interactive workflow tables"
alembic upgrade head

# Config migration
python scripts/migrate_existing_configs.py  # Ensure existing configs work
python scripts/validate_all_configs.py      # Validate against new schemas
```

**3. Monitoring & Observability:**

```python
# Add metrics for new features
metrics = {
    'interactive_sessions_started': 0,
    'hitl_checkpoints_created': 0,
    'hitl_approval_rate': 0.0,
    'template_inheritance_usage': 0,
    'process_library_usage': {}
}
```

### **Risk Mitigation Checklist**

**Pre-Release Validation:**

```bash
[ ] All existing workflows continue to function unchanged
[ ] New schemas validate correctly without breaking existing configs
[ ] Performance benchmarks show no regression
[ ] Security audit passes for new input handling
[ ] End-to-end testing covers all 10 workflow steps
[ ] Load testing with concurrent interactive sessions
[ ] Rollback plan tested and documented
```

**Production Deployment Steps:**

```bash
1. Deploy with feature flags DISABLED
2. Validate existing functionality in production
3. Enable PROCESS_TEMPLATES feature flag
4. Test template inheritance with safe configs
5. Enable INTERACTIVE_WORKFLOWS for limited users
6. Monitor metrics and error rates
7. Full rollout after validation period
```

---

## Next Steps

### **Immediate Actions Required**

1. **Team Assignment**: Assign 2-3 developers familiar with existing YAML system
2. **Schema Design Review**: Validate proposed schema extensions with team
3. **Development Timeline**: Confirm 6-week timeline is realistic
4. **Infrastructure**: Ensure database migration capabilities are ready

### **Implementation Order Priority**

1. **Schema & Templates** (Week 1) - Foundation must be solid
2. **Backend Extensions** (Week 2) - Core functionality implementation  
3. **UI Integration** (Week 3-4) - User-facing features
4. **Testing & Validation** (Week 5) - Quality assurance
5. **Deployment & Monitoring** (Week 6) - Production readiness

---

**Document Status**: ✅ COMPLETE - Following CODEPROTOCOL  
**Architecture Approach**: ✅ EXTENDS existing YAML-driven system  
**Implementation Ready**: ✅ Pending stakeholder approval  
**Next Review**: September 9, 2025