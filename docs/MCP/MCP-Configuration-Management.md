# Configuration Management - YAML Configs and Database Schemas

**Part of:** MCP-Based Role-Constrained Agent Orchestration  
**Focus:** Configuration systems, YAML templates, and data persistence

---

## Three-Tier Configuration Strategy

### Tier 1: Role Definitions

Individual agent role configurations stored as YAML files:

```yaml
# /mcp-configs/roles/business_analyst.yaml
role_id: "business_analyst"
name: "Business Analyst"
description: "Specializes in requirements gathering and business analysis"
mcp_service_url: "mcp://localhost:3001/business-analyst"

constraints:
  domain: "business_analysis"
  forbidden_topics: 
    - "technical_implementation"
    - "code_review"
    - "system_architecture"
  required_outputs: 
    - "requirements_doc"
    - "stakeholder_map"
    - "success_criteria"
  
persona:
  experience: "10+ years business analysis"
  communication_style: "structured, questioning"
  focus_areas: 
    - "requirements"
    - "process_optimization"
    - "stakeholder_management"
  
tools:
  - name: "requirements_extraction"
    description: "Extract and structure business requirements"
  - name: "stakeholder_analysis"  
    description: "Identify and analyze project stakeholders"
  - name: "process_mapping"
    description: "Map and optimize business processes"

llm_config:
  model: "gpt-4o-mini"  # Cost-optimized for analysis tasks
  temperature: 0.3
  max_tokens: 2000
  
handoff_conditions:
  - "requirements_complete"
  - "stakeholders_identified"
  - "acceptance_criteria_defined"
```

```yaml
# /mcp-configs/roles/technical_architect.yaml
role_id: "technical_architect"
name: "Technical Architect"
description: "Designs system architecture and technical solutions"
mcp_service_url: "mcp://localhost:3002/technical-architect"

constraints:
  domain: "technical_architecture"
  forbidden_topics: 
    - "business_requirements"
    - "user_experience"
    - "marketing_strategy"
  required_outputs: 
    - "architecture_diagram"
    - "tech_stack"
    - "scalability_plan"
    - "security_architecture"
    
persona:
  experience: "15+ years system architecture"
  communication_style: "technical, detailed"
  focus_areas: 
    - "scalability"
    - "security"
    - "performance"
    - "maintainability"
    
tools:
  - name: "architecture_modeling"
    description: "Create system architecture diagrams and models"
  - name: "technology_assessment"
    description: "Evaluate and recommend technology stacks"
  - name: "performance_analysis"
    description: "Analyze performance requirements and constraints"

llm_config:
  model: "claude-3-sonnet"  # Better for technical reasoning
  temperature: 0.2
  max_tokens: 3000
  
handoff_conditions:
  - "architecture_approved"
  - "tech_stack_selected"
  - "performance_requirements_defined"
```

```yaml
# /mcp-configs/roles/developer.yaml
role_id: "developer"
name: "Full-Stack Developer"
description: "Implements solutions based on architectural designs"
mcp_service_url: "mcp://localhost:3003/developer"

constraints:
  domain: "software_development"
  forbidden_topics: 
    - "business_strategy"
    - "market_analysis"
    - "user_research"
  required_outputs: 
    - "implementation_plan"
    - "code_artifacts"
    - "testing_strategy"
    - "deployment_plan"
    
persona:
  experience: "8+ years full-stack development"
  communication_style: "practical, code-focused"
  focus_areas: 
    - "clean_code"
    - "testing"
    - "deployment"
    - "optimization"
    
tools:
  - name: "code_generation"
    description: "Generate application code and components"
  - name: "testing_framework"
    description: "Create comprehensive test suites"
  - name: "deployment_automation"
    description: "Set up CI/CD and deployment pipelines"

llm_config:
  model: "gpt-4o"  # Best for code generation
  temperature: 0.1
  max_tokens: 4000
  
handoff_conditions:
  - "implementation_complete"
  - "tests_passing"
  - "deployment_ready"
```

```yaml
# /mcp-configs/roles/qa_tester.yaml
role_id: "qa_tester"
name: "QA Tester"
description: "Quality assurance and testing specialist"
mcp_service_url: "mcp://localhost:3004/qa-tester"

constraints:
  domain: "quality_assurance"
  forbidden_topics:
    - "business_requirements"
    - "system_architecture"
    - "marketing_strategy"
  required_outputs:
    - "test_plan"
    - "test_cases"
    - "quality_report"
    - "bug_report"

persona:
  experience: "6+ years QA and testing"
  communication_style: "detail-oriented, systematic"
  focus_areas:
    - "test_automation"
    - "quality_metrics"
    - "bug_prevention"
    - "user_acceptance"

tools:
  - name: "test_case_generation"
    description: "Generate comprehensive test cases"
  - name: "automation_framework"
    description: "Set up automated testing frameworks"
  - name: "quality_analysis"
    description: "Analyze code and system quality"

llm_config:
  model: "gpt-4o-mini"
  temperature: 0.2
  max_tokens: 2500

handoff_conditions:
  - "testing_complete"
  - "quality_validated"
  - "bugs_documented"
```

---

## Tier 2: Workflow Templates

Pre-defined workflow configurations for common use cases:

```yaml
# /mcp-configs/workflows/product_development.yaml
workflow_id: "product_development"
name: "Product Development Workflow"
description: "End-to-end product development from idea to deployment"
version: "1.0"

trigger_keywords: 
  - "build"
  - "create"
  - "develop"
  - "product"
  - "application"
  - "system"

agents:
  - role: "business_analyst"
    position: 1
    inputs: ["user_request"]
    outputs: ["requirements_analysis", "stakeholder_map", "success_criteria"]
    timeout_minutes: 10
    
  - role: "technical_architect"
    position: 2
    inputs: ["requirements_analysis", "success_criteria"]
    outputs: ["technical_design", "architecture_diagram", "tech_stack"]
    timeout_minutes: 15
    
  - role: "developer"
    position: 3
    inputs: ["technical_design", "architecture_diagram", "tech_stack"]
    outputs: ["implementation_plan", "code_artifacts", "testing_strategy"]
    timeout_minutes: 20
    
  - role: "qa_tester"
    position: 4
    inputs: ["implementation_plan", "code_artifacts", "testing_strategy"]
    outputs: ["test_results", "quality_report", "deployment_validation"]
    timeout_minutes: 15

approval_gates:
  - after_agent: "business_analyst"
    title: "Requirements Approval"
    description: "Review business requirements and stakeholder analysis"
    
  - after_agent: "technical_architect"
    title: "Architecture Review"
    description: "Approve technical architecture and technology choices"

estimated_duration: "45-60 minutes"
success_criteria:
  - "All agents complete successfully"
  - "Human approvals obtained at gates"
  - "Quality score > 0.8"
```

```yaml
# /mcp-configs/workflows/marketing_campaign.yaml
workflow_id: "marketing_campaign"
name: "Marketing Campaign Development"
description: "Complete marketing campaign from research to media planning"
version: "1.0"

trigger_keywords: 
  - "campaign"
  - "marketing"
  - "promotion"
  - "advertising"
  - "launch"

agents:
  - role: "market_researcher"
    position: 1
    inputs: ["user_request"]
    outputs: ["market_analysis", "competitor_research", "target_audience"]
    timeout_minutes: 12
    
  - role: "campaign_strategist"
    position: 2
    inputs: ["market_analysis", "target_audience"]
    outputs: ["campaign_strategy", "messaging_framework", "channel_mix"]
    timeout_minutes: 15
    
  - role: "creative_director"
    position: 3
    inputs: ["campaign_strategy", "messaging_framework"]
    outputs: ["creative_concepts", "asset_specifications", "brand_guidelines"]
    timeout_minutes: 18
    
  - role: "media_planner"
    position: 4
    inputs: ["campaign_strategy", "creative_concepts", "channel_mix"]
    outputs: ["media_plan", "budget_allocation", "timeline"]
    timeout_minutes: 12

approval_gates:
  - after_agent: "creative_director"
    title: "Creative Approval"
    description: "Review and approve creative concepts and brand guidelines"

estimated_duration: "50-70 minutes"
```

```yaml
# /mcp-configs/workflows/technical_support.yaml
workflow_id: "technical_support"
name: "Technical Issue Resolution"
description: "Systematic approach to technical problem diagnosis and resolution"
version: "1.0"

trigger_keywords: 
  - "bug"
  - "error"
  - "issue"
  - "problem"
  - "troubleshoot"
  - "fix"

agents:
  - role: "system_analyst"
    position: 1
    inputs: ["user_request", "system_logs"]
    outputs: ["problem_analysis", "affected_systems", "initial_findings"]
    timeout_minutes: 8
    
  - role: "specialist_agent"  # Dynamic selection based on problem type
    position: 2
    inputs: ["problem_analysis", "affected_systems"]
    outputs: ["detailed_diagnosis", "solution_options", "recommendations"]
    timeout_minutes: 15
    
  - role: "solution_implementer"
    position: 3
    inputs: ["detailed_diagnosis", "solution_options"]
    outputs: ["implementation_plan", "testing_results", "deployment_steps"]
    timeout_minutes: 20

flow_type: "adaptive"  # Can modify based on problem complexity
estimated_duration: "30-45 minutes"
```

---

## Tier 3: Dynamic Runtime Configuration

```yaml
# /mcp-configs/dynamic/runtime_workflow_<session_id>.yaml
# Generated dynamically based on user input
workflow_id: "dynamic_<timestamp>"
generated_from: "user_intent_analysis"
user_request: "I need help analyzing customer feedback and improving our API performance"
generated_at: "2025-08-21T15:30:00Z"

intent_analysis:
  primary_domain: "technical_analysis"
  complexity: "medium"
  confidence: 0.92
  keywords: ["analyze", "customer feedback", "API performance"]

selected_agents:
  - role: "data_analyst"
    reason: "Customer feedback analysis requires data analysis skills"
    confidence: 0.95
  - role: "technical_architect"  
    reason: "API performance improvement requires technical architecture expertise"
    confidence: 0.88

flow_type: "parallel_then_merge"
estimated_duration: "15-20 minutes"
optimization_notes:
  - "Parallel execution possible for first two agents"
  - "Results can be merged for comprehensive recommendations"
```

---

## Database Schema for Production

### Role Management Tables

```sql
-- Role definitions with version control
CREATE TABLE mcp_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    version INTEGER NOT NULL DEFAULT 1,
    config JSONB NOT NULL,
    constraints JSONB NOT NULL,
    persona JSONB NOT NULL,
    tools JSONB NOT NULL,
    llm_config JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

-- Index for fast role lookups
CREATE INDEX idx_mcp_roles_role_id ON mcp_roles(role_id);
CREATE INDEX idx_mcp_roles_active ON mcp_roles(is_active);

-- Workflow templates with A/B testing support
CREATE TABLE workflow_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    version INTEGER NOT NULL DEFAULT 1,
    config JSONB NOT NULL,
    trigger_keywords TEXT[] DEFAULT '{}',
    success_rate DECIMAL(5,2),
    avg_completion_time INTEGER, -- in seconds
    usage_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for workflow discovery
CREATE INDEX idx_workflow_templates_workflow_id ON workflow_templates(workflow_id);
CREATE INDEX idx_workflow_templates_keywords ON workflow_templates USING GIN(trigger_keywords);
```

### Execution Tracking Tables

```sql
-- Runtime workflow execution logs
CREATE TABLE workflow_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(100) NOT NULL,
    workflow_id VARCHAR(50) NOT NULL,
    workflow_config JSONB NOT NULL,
    execution_log JSONB NOT NULL,
    status VARCHAR(20) NOT NULL, -- pending, running, completed, failed
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    total_duration INTEGER, -- in seconds
    user_id VARCHAR(100),
    user_feedback JSONB,
    cost_breakdown JSONB,
    performance_metrics JSONB
);

-- Agent execution details
CREATE TABLE agent_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_execution_id UUID REFERENCES workflow_executions(id),
    agent_role VARCHAR(50) NOT NULL,
    position INTEGER NOT NULL,
    inputs JSONB,
    outputs JSONB,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration INTEGER, -- in seconds
    token_usage JSONB,
    cost DECIMAL(10,4),
    retry_count INTEGER DEFAULT 0,
    quality_score DECIMAL(3,2),
    error_message TEXT,
    status VARCHAR(20) NOT NULL -- pending, running, completed, failed
);

-- Index for performance analytics
CREATE INDEX idx_workflow_executions_session ON workflow_executions(session_id);
CREATE INDEX idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX idx_agent_executions_workflow ON agent_executions(workflow_execution_id);
CREATE INDEX idx_agent_executions_role ON agent_executions(agent_role);
```

### Configuration Management Functions

```sql
-- Function to get latest role configuration
CREATE OR REPLACE FUNCTION get_latest_role_config(role_name VARCHAR(50))
RETURNS JSONB AS $$
DECLARE
    role_config JSONB;
BEGIN
    SELECT config INTO role_config
    FROM mcp_roles
    WHERE role_id = role_name 
    AND is_active = true
    ORDER BY version DESC
    LIMIT 1;
    
    RETURN role_config;
END;
$$ LANGUAGE plpgsql;

-- Function to get optimal workflow template
CREATE OR REPLACE FUNCTION get_optimal_workflow(keywords TEXT[])
RETURNS TABLE(workflow_id VARCHAR(50), config JSONB, success_rate DECIMAL(5,2)) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        wt.workflow_id,
        wt.config,
        wt.success_rate
    FROM workflow_templates wt
    WHERE wt.is_active = true
    AND wt.trigger_keywords && keywords  -- Array overlap operator
    ORDER BY wt.success_rate DESC, wt.usage_count DESC
    LIMIT 5;
END;
$$ LANGUAGE plpgsql;

-- Function to track workflow performance
CREATE OR REPLACE FUNCTION update_workflow_performance(
    wf_id VARCHAR(50), 
    duration_seconds INTEGER, 
    success BOOLEAN
)
RETURNS VOID AS $$
BEGIN
    UPDATE workflow_templates
    SET 
        usage_count = usage_count + 1,
        avg_completion_time = (
            COALESCE(avg_completion_time * usage_count, 0) + duration_seconds
        ) / (usage_count + 1),
        success_rate = CASE 
            WHEN success THEN 
                (COALESCE(success_rate * usage_count, 0) + 100) / (usage_count + 1)
            ELSE 
                (COALESCE(success_rate * usage_count, 0)) / (usage_count + 1)
        END
    WHERE workflow_id = wf_id;
END;
$$ LANGUAGE plpgsql;
```

---

## Environment-Based Configuration

### Development Environment

```yaml
# /mcp-configs/environments/development.yaml
environment: "development"
debug: true

overrides:
  llm_config:
    default_model: "gpt-4o-mini"  # Cost-effective for development
    rate_limits:
      requests_per_minute: 100
      tokens_per_minute: 50000
    timeout_seconds: 30
    
  monitoring:
    log_level: "DEBUG"
    trace_enabled: true
    metrics_collection: false
    
  agents:
    response_timeout: 60  # seconds
    max_retry_attempts: 2
    enable_constraint_validation: true
    
  database:
    connection_pool_size: 5
    query_timeout: 30
    enable_query_logging: true
    
  security:
    require_authentication: false
    enable_rate_limiting: false
    cors_origins: ["http://localhost:3000", "http://localhost:5173"]
```

### Production Environment

```yaml
# /mcp-configs/environments/production.yaml
environment: "production"
debug: false

overrides:
  llm_config:
    default_model: "gpt-4o"  # Higher quality for production
    rate_limits:
      requests_per_minute: 1000
      tokens_per_minute: 500000
    timeout_seconds: 60
    
  monitoring:
    log_level: "INFO"
    trace_enabled: true
    metrics_collection: true
    alerting_enabled: true
    
  agents:
    response_timeout: 120  # seconds
    max_retry_attempts: 3
    enable_constraint_validation: true
    health_check_interval: 30
    
  database:
    connection_pool_size: 20
    query_timeout: 60
    enable_query_logging: false
    backup_enabled: true
    
  security:
    require_authentication: true
    enable_rate_limiting: true
    cors_origins: ["https://botarmy.com", "https://app.botarmy.com"]
    session_timeout: 3600
```

---

## Configuration Loading and Validation

```python
class ConfigurationManager:
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.config_cache = {}
        self.last_reload = {}
        
    def load_role_config(self, role_id: str) -> dict:
        """Load role configuration with environment overrides"""
        cache_key = f"role_{role_id}"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            return self.config_cache[cache_key]
        
        # Load base configuration
        base_config = self._load_yaml_config(f"roles/{role_id}.yaml")
        
        # Apply environment overrides
        env_overrides = self._load_yaml_config(f"environments/{self.environment}.yaml")
        merged_config = self._merge_configs(base_config, env_overrides)
        
        # Validate configuration
        self._validate_role_config(merged_config)
        
        # Cache and return
        self.config_cache[cache_key] = merged_config
        self.last_reload[cache_key] = datetime.now()
        
        return merged_config
    
    def load_workflow_config(self, workflow_id: str) -> dict:
        """Load workflow configuration"""
        cache_key = f"workflow_{workflow_id}"
        
        if self._is_cache_valid(cache_key):
            return self.config_cache[cache_key]
        
        workflow_config = self._load_yaml_config(f"workflows/{workflow_id}.yaml")
        
        # Validate workflow configuration
        self._validate_workflow_config(workflow_config)
        
        self.config_cache[cache_key] = workflow_config
        self.last_reload[cache_key] = datetime.now()
        
        return workflow_config
    
    def _validate_role_config(self, config: dict):
        """Validate role configuration against schema"""
        required_fields = ["role_id", "constraints", "persona", "tools", "llm_config"]
        
        for field in required_fields:
            if field not in config:
                raise ConfigValidationError(f"Missing required field '{field}' in role config")
        
        # Validate constraints
        constraints = config["constraints"]
        if "domain" not in constraints:
            raise ConfigValidationError("Role constraints must specify domain")
        
        # Validate LLM config
        llm_config = config["llm_config"]
        if "model" not in llm_config:
            raise ConfigValidationError("LLM config must specify model")
        
        return True
    
    def _validate_workflow_config(self, config: dict):
        """Validate workflow configuration"""
        required_fields = ["workflow_id", "agents", "trigger_keywords"]
        
        for field in required_fields:
            if field not in config:
                raise ConfigValidationError(f"Missing required field '{field}' in workflow config")
        
        # Validate agents sequence
        agents = config["agents"]
        if not agents:
            raise ConfigValidationError("Workflow must have at least one agent")
        
        # Validate agent positions are sequential
        positions = [agent.get("position", 0) for agent in agents]
        if sorted(positions) != list(range(1, len(positions) + 1)):
            raise ConfigValidationError("Agent positions must be sequential starting from 1")
        
        return True
    
    def _load_yaml_config(self, config_path: str) -> dict:
        """Load YAML configuration file"""
        full_path = os.path.join(self.config_directory, config_path)
        
        try:
            with open(full_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {config_path}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in {config_path}: {e}")
    
    def _merge_configs(self, base_config: dict, overrides: dict) -> dict:
        """Merge base configuration with environment overrides"""
        merged = base_config.copy()
        
        if "overrides" in overrides:
            for key, value in overrides["overrides"].items():
                if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key].update(value)
                else:
                    merged[key] = value
        
        return merged
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached configuration is still valid"""
        if cache_key not in self.config_cache:
            return False
        
        last_reload = self.last_reload.get(cache_key)
        if not last_reload:
            return False
        
        # Cache valid for 5 minutes
        return (datetime.now() - last_reload).total_seconds() < 300

class ConfigValidationError(Exception):
    """Raised when configuration validation fails"""
    pass

class ConfigurationError(Exception):
    """Raised when configuration loading fails"""
    pass
```

---

## File Structure Organization

```
/mcp-configs/
├── roles/                          # Individual agent role definitions
│   ├── business_analyst.yaml
│   ├── technical_architect.yaml
│   ├── developer.yaml
│   ├── qa_tester.yaml
│   ├── market_researcher.yaml
│   ├── campaign_strategist.yaml
│   ├── creative_director.yaml
│   ├── media_planner.yaml
│   ├── data_analyst.yaml
│   └── project_manager.yaml
├── workflows/                      # Predefined workflow templates
│   ├── product_development.yaml
│   ├── marketing_campaign.yaml
│   ├── technical_support.yaml
│   ├── business_analysis.yaml
│   ├── content_creation.yaml
│   └── data_analysis.yaml
├── dynamic/                        # Runtime-generated workflows
│   ├── session_<id>_workflow.yaml
│   └── temp_workflows/
├── environments/                   # Environment-specific settings
│   ├── development.yaml
│   ├── staging.yaml
│   └── production.yaml
└── global/                         # Global settings
    ├── llm_providers.yaml
    ├── rate_limits.yaml
    └── monitoring.yaml
```

This configuration management system provides a robust foundation for managing role definitions, workflow templates, and environment-specific settings while maintaining flexibility for dynamic workflow generation and runtime optimization.