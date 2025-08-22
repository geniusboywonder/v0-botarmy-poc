# MCP Service Architecture - Detailed Implementation

**Part of:** MCP-Based Role-Constrained Agent Orchestration  
**Focus:** Core MCP service implementation patterns and role definitions

---

## MCP Service Architecture for Role-Based Agents

Each role becomes a specialized MCP service with built-in constraints and domain expertise:

### Business Analyst MCP Service

```python
# Business Analyst MCP Service
class BusinessAnalystMCP:
    def __init__(self):
        self.role_context = {
            "persona": "Senior Business Analyst with 10+ years experience",
            "constraints": [
                "Only provide analysis, not implementation advice",
                "Focus on business requirements and stakeholder needs",
                "Always ask clarifying questions about business context"
            ],
            "tools": ["requirements_analysis", "stakeholder_mapping", "process_modeling"]
        }
    
    @mcp_tool
    def analyze_requirements(self, input_text: str) -> Dict:
        # Constrained to only analysis tasks
        prompt = f"""
        As a Business Analyst, analyze the following request focusing ONLY on:
        - Business requirements identification
        - Stakeholder impact analysis  
        - Success criteria definition
        
        Do NOT provide technical implementation details.
        
        Input: {input_text}
        """
        return self.llm_call(prompt)
    
    @mcp_tool
    def create_user_stories(self, requirements: Dict) -> Dict:
        prompt = f"""
        Based on the requirements analysis, create user stories following this format:
        - As a [user type], I want [goal] so that [benefit]
        - Include acceptance criteria for each story
        - Prioritize stories by business value
        
        Requirements: {requirements}
        """
        return self.llm_call(prompt)
```

### Technical Architect MCP Service  

```python
class TechnicalArchitectMCP:
    def __init__(self):
        self.role_context = {
            "persona": "Senior Technical Architect",
            "constraints": [
                "Only provide technical architecture and design",
                "Assume business requirements are already defined",
                "Focus on scalability, performance, security"
            ]
        }
    
    @mcp_tool
    def design_architecture(self, requirements: Dict) -> Dict:
        prompt = f"""
        As a Technical Architect, design system architecture for:
        Requirements: {requirements}
        
        Focus ONLY on:
        - System architecture and design patterns
        - Technology stack recommendations
        - Scalability and performance considerations
        - Security architecture
        
        Do NOT include business logic or user experience details.
        """
        return self.llm_call(prompt)
    
    @mcp_tool
    def select_tech_stack(self, architecture: Dict) -> Dict:
        prompt = f"""
        Based on the architecture design, recommend specific technologies:
        - Frontend framework and libraries
        - Backend services and APIs
        - Database and storage solutions
        - Infrastructure and deployment platforms
        
        Architecture: {architecture}
        """
        return self.llm_call(prompt)
```

### Developer MCP Service

```python
class DeveloperMCP:
    def __init__(self):
        self.role_context = {
            "persona": "Senior Full-Stack Developer",
            "constraints": [
                "Only provide implementation details and code",
                "Assume architecture is already defined", 
                "Focus on code quality, testing, deployment"
            ]
        }
    
    @mcp_tool
    def implement_solution(self, architecture: Dict) -> Dict:
        prompt = f"""
        As a Developer, create implementation plan for:
        Architecture: {architecture}
        
        Focus ONLY on:
        - Code structure and organization
        - Implementation details and algorithms
        - Testing strategies and test cases
        - Deployment and CI/CD pipelines
        
        Provide concrete code examples where appropriate.
        """
        return self.llm_call(prompt)
    
    @mcp_tool
    def generate_code_scaffolding(self, implementation_plan: Dict) -> Dict:
        prompt = f"""
        Generate code scaffolding and key implementation files:
        - Directory structure
        - Main application files
        - Configuration files
        - Database schemas
        - API endpoint definitions
        
        Implementation Plan: {implementation_plan}
        """
        return self.llm_call(prompt)
```

---

## Role Constraint Enforcement

### Constraint Validation System

```python
class RoleConstraintValidator:
    def __init__(self, role_config: dict):
        self.role_config = role_config
        self.forbidden_topics = role_config.get("constraints", {}).get("forbidden_topics", [])
        self.required_outputs = role_config.get("constraints", {}).get("required_outputs", [])
        
    def validate_input(self, user_input: str) -> bool:
        """Validate that input is appropriate for this role"""
        for forbidden_topic in self.forbidden_topics:
            if self.contains_forbidden_content(user_input, forbidden_topic):
                raise ConstraintViolationError(
                    f"Input contains forbidden topic '{forbidden_topic}' for role {self.role_config['role_id']}"
                )
        return True
    
    def validate_output(self, agent_output: dict) -> bool:
        """Validate that output meets role requirements"""
        for required_output in self.required_outputs:
            if required_output not in agent_output:
                raise ConstraintViolationError(
                    f"Required output '{required_output}' missing from {self.role_config['role_id']} response"
                )
        return True
    
    def contains_forbidden_content(self, text: str, forbidden_topic: str) -> bool:
        """Check if text contains forbidden content using semantic analysis"""
        # Use lightweight model for semantic similarity check
        similarity_score = self.semantic_similarity(text, forbidden_topic)
        return similarity_score > 0.7  # Threshold for constraint violation
```

### Role-Specific LLM Configuration

```python
class RoleBasedLLMService:
    def __init__(self):
        self.model_mappings = {
            "business_analyst": {
                "primary": "gpt-4o-mini",  # Cost-effective for analysis
                "fallback": "claude-3-haiku",
                "max_tokens": 2000,
                "temperature": 0.3
            },
            "technical_architect": {
                "primary": "claude-3-sonnet",  # Better technical reasoning
                "fallback": "gpt-4o",
                "max_tokens": 3000,
                "temperature": 0.2
            },
            "developer": {
                "primary": "gpt-4o",  # Best for code generation
                "fallback": "claude-3-sonnet",
                "max_tokens": 4000,
                "temperature": 0.1
            },
            "qa_tester": {
                "primary": "gpt-4o-mini",  # Pattern recognition
                "fallback": "claude-3-haiku",
                "max_tokens": 2000,
                "temperature": 0.2
            }
        }
    
    async def call_role_optimized_llm(self, role: str, prompt: str) -> str:
        """Call LLM optimized for specific role"""
        config = self.model_mappings.get(role, self.model_mappings["business_analyst"])
        
        try:
            # Try primary model
            response = await self.call_llm(
                model=config["primary"],
                prompt=prompt,
                max_tokens=config["max_tokens"],
                temperature=config["temperature"]
            )
            return response
        except Exception as e:
            # Fallback to secondary model
            logger.warning(f"Primary model failed for {role}, using fallback: {e}")
            response = await self.call_llm(
                model=config["fallback"],
                prompt=prompt,
                max_tokens=config["max_tokens"],
                temperature=config["temperature"]
            )
            return response
```

---

## MCP Service Registry and Discovery

```python
class MCPServiceRegistry:
    def __init__(self):
        self.registered_services = {}
        self.service_health = {}
        
    def register_service(self, role_id: str, service_config: dict):
        """Register a new MCP service"""
        service_instance = {
            "role_id": role_id,
            "service_url": service_config["mcp_service_url"],
            "capabilities": service_config.get("tools", []),
            "constraints": service_config.get("constraints", {}),
            "health_check_url": f"{service_config['mcp_service_url']}/health",
            "last_health_check": None,
            "status": "unknown"
        }
        
        self.registered_services[role_id] = service_instance
        return role_id
    
    async def discover_available_agents(self) -> List[dict]:
        """Discover all available agents and their capabilities"""
        available_agents = []
        
        for role_id, service in self.registered_services.items():
            # Check service health
            health_status = await self.check_service_health(service["service_url"])
            
            if health_status["status"] == "healthy":
                available_agents.append({
                    "role_id": role_id,
                    "capabilities": service["capabilities"],
                    "constraints": service["constraints"],
                    "service_url": service["service_url"],
                    "response_time": health_status["response_time"]
                })
        
        return available_agents
    
    async def get_service(self, role_id: str):
        """Get MCP service instance for specific role"""
        if role_id not in self.registered_services:
            raise ServiceNotFoundError(f"Role {role_id} not registered")
        
        service_config = self.registered_services[role_id]
        
        # Check if service is healthy
        health_status = await self.check_service_health(service_config["service_url"])
        if health_status["status"] != "healthy":
            raise ServiceUnavailableError(f"Service {role_id} is not healthy")
        
        return MCPServiceClient(service_config)
    
    async def check_service_health(self, service_url: str) -> dict:
        """Check health of MCP service"""
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{service_url}/health", timeout=5) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        return {
                            "status": "healthy",
                            "response_time": response_time,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "status": "unhealthy",
                            "response_time": response_time,
                            "error": f"HTTP {response.status}"
                        }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
```

---

## Agent Communication Patterns

### Handoff Protocol

```python
class AgentHandoffManager:
    def __init__(self):
        self.handoff_validators = {}
        
    async def execute_handoff(self, from_agent: str, to_agent: str, context: dict):
        """Execute handoff between agents with validation"""
        
        # Validate handoff conditions are met
        handoff_valid = await self.validate_handoff_conditions(from_agent, context)
        if not handoff_valid:
            raise HandoffValidationError(f"Handoff conditions not met for {from_agent}")
        
        # Transform context for receiving agent
        transformed_context = await self.transform_context_for_agent(context, to_agent)
        
        # Log handoff event
        await self.log_handoff_event(from_agent, to_agent, transformed_context)
        
        # Stream handoff notification to UI
        await self.notify_handoff(from_agent, to_agent)
        
        return transformed_context
    
    async def validate_handoff_conditions(self, agent_role: str, context: dict) -> bool:
        """Validate that agent has completed required outputs"""
        agent_config = await self.get_agent_config(agent_role)
        required_outputs = agent_config.get("required_outputs", [])
        
        for output in required_outputs:
            if output not in context:
                logger.warning(f"Missing required output '{output}' from {agent_role}")
                return False
            
            # Validate output quality
            if not await self.validate_output_quality(output, context[output]):
                logger.warning(f"Poor quality output '{output}' from {agent_role}")
                return False
        
        return True
    
    async def transform_context_for_agent(self, context: dict, target_agent: str) -> dict:
        """Transform context to match target agent's input requirements"""
        agent_config = await self.get_agent_config(target_agent)
        expected_inputs = agent_config.get("expected_inputs", [])
        
        transformed_context = {}
        
        for expected_input in expected_inputs:
            if expected_input in context:
                # Direct mapping
                transformed_context[expected_input] = context[expected_input]
            else:
                # Try to derive from available context
                derived_value = await self.derive_input_from_context(expected_input, context)
                if derived_value:
                    transformed_context[expected_input] = derived_value
        
        return transformed_context
```

---

## Error Handling and Recovery

```python
class AgentErrorHandler:
    def __init__(self):
        self.retry_policies = {
            "network_error": {"max_retries": 3, "backoff": "exponential"},
            "llm_rate_limit": {"max_retries": 5, "backoff": "linear"},
            "constraint_violation": {"max_retries": 1, "backoff": "none"},
            "service_unavailable": {"max_retries": 2, "backoff": "exponential"}
        }
    
    async def handle_agent_error(self, agent_role: str, error: Exception, context: dict):
        """Handle agent errors with appropriate recovery strategies"""
        
        error_type = self.classify_error(error)
        retry_policy = self.retry_policies.get(error_type, {"max_retries": 1, "backoff": "none"})
        
        if retry_policy["max_retries"] > 0:
            # Attempt retry with backoff
            return await self.retry_agent_execution(agent_role, context, retry_policy)
        else:
            # Escalate to human or alternative agent
            return await self.escalate_error(agent_role, error, context)
    
    async def retry_agent_execution(self, agent_role: str, context: dict, retry_policy: dict):
        """Retry agent execution with backoff strategy"""
        for attempt in range(retry_policy["max_retries"]):
            try:
                if retry_policy["backoff"] == "exponential":
                    delay = 2 ** attempt
                elif retry_policy["backoff"] == "linear":
                    delay = attempt + 1
                else:
                    delay = 0
                
                if delay > 0:
                    await asyncio.sleep(delay)
                
                # Retry agent execution
                result = await self.execute_agent(agent_role, context)
                return result
                
            except Exception as e:
                if attempt == retry_policy["max_retries"] - 1:
                    # Final attempt failed, escalate
                    return await self.escalate_error(agent_role, e, context)
                continue
    
    async def escalate_error(self, agent_role: str, error: Exception, context: dict):
        """Escalate error to human or alternative handling"""
        escalation_data = {
            "agent": agent_role,
            "error": str(error),
            "error_type": self.classify_error(error),
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "suggested_actions": self.suggest_recovery_actions(error)
        }
        
        # Send to human intervention queue
        await self.send_to_human_queue(escalation_data)
        
        # Try alternative agent if available
        alternative_agent = await self.find_alternative_agent(agent_role)
        if alternative_agent:
            return await self.execute_alternative_agent(alternative_agent, context)
        
        # Return error state for workflow handling
        return {"status": "error", "escalated": True, "error_data": escalation_data}
```

This MCP service architecture provides the foundation for truly role-constrained agents that can work together seamlessly while maintaining their specialized expertise domains.