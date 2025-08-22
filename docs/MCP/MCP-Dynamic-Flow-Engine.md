# Dynamic Flow Assembly Engine

**Part of:** MCP-Based Role-Constrained Agent Orchestration  
**Focus:** Runtime workflow generation and intelligent agent selection

---

## Dynamic Flow Assembly Architecture

The Dynamic Flow Assembly Engine creates workflows on-the-fly based on user intent, available agents, and optimization patterns.

### Core Assembly Engine

```python
class DynamicFlowAssembler:
    def __init__(self):
        self.available_agents = self.discover_mcp_agents()
        self.capability_matcher = CapabilityMatcher()
        self.flow_optimizer = FlowOptimizer()
        self.intent_classifier = IntentClassifier()
        
    async def assemble_flow(self, user_request: str):
        """Dynamically create workflow based on user intent"""
        
        # 1. Analyze what capabilities are needed
        required_capabilities = await self.analyze_capabilities_needed(user_request)
        
        # 2. Match capabilities to available MCP agents
        selected_agents = []
        for capability in required_capabilities:
            best_agent = await self.match_capability_to_agent(capability)
            if best_agent:
                selected_agents.append(best_agent)
        
        # 3. Determine optimal execution order
        optimized_sequence = self.flow_optimizer.optimize_sequence(
            selected_agents, 
            user_request
        )
        
        # 4. Generate workflow configuration
        workflow_config = self.create_dynamic_workflow_config(
            optimized_sequence,
            user_request
        )
        
        return workflow_config
    
    async def analyze_capabilities_needed(self, user_request: str) -> List[str]:
        """Analyze user request to determine needed capabilities"""
        analysis_prompt = f"""
        Analyze this user request and identify the key capabilities needed:
        
        Request: {user_request}
        
        Available capability types:
        - business_analysis: Requirements gathering, stakeholder analysis
        - technical_architecture: System design, technology selection
        - software_development: Code implementation, testing
        - data_analysis: Data processing, insights, reporting
        - market_research: Market analysis, competitive research
        - content_creation: Writing, documentation, creative content
        - project_management: Planning, coordination, tracking
        - quality_assurance: Testing, validation, quality control
        
        Return a JSON list of needed capabilities in order of execution.
        Example: ["business_analysis", "technical_architecture", "software_development"]
        """
        
        response = await self.analysis_llm.complete(analysis_prompt)
        return json.loads(response)
```

### Capability Matching System

```python
class CapabilityMatcher:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.capability_embeddings = {}
        self.agent_capability_cache = {}
        
    async def compute_similarity(self, required_capability: str, agent_capabilities: List[str]) -> float:
        """Compute semantic similarity between required capability and agent capabilities"""
        
        # Get embedding for required capability
        req_embedding = self.get_capability_embedding(required_capability)
        
        # Get embeddings for all agent capabilities
        agent_embeddings = [self.get_capability_embedding(cap) for cap in agent_capabilities]
        
        # Compute maximum similarity score
        similarities = [cosine_similarity([req_embedding], [agent_emb])[0][0] 
                       for agent_emb in agent_embeddings]
        
        return max(similarities) if similarities else 0.0
    
    def get_capability_embedding(self, capability: str) -> np.ndarray:
        """Get or compute embedding for capability"""
        if capability not in self.capability_embeddings:
            self.capability_embeddings[capability] = self.embedding_model.encode(capability)
        return self.capability_embeddings[capability]
    
    async def match_capability_to_agent(self, capability: str, available_agents: List[dict]) -> dict:
        """Match required capability to best available MCP agent"""
        best_match = None
        best_score = 0
        
        for agent in available_agents:
            # Check agent availability
            if not await self.check_agent_availability(agent):
                continue
            
            # Compute similarity score
            similarity_score = await self.compute_similarity(
                capability, 
                agent.get("capabilities", [])
            )
            
            # Consider agent performance history
            performance_score = await self.get_agent_performance_score(agent["role_id"])
            
            # Combined scoring (70% similarity, 30% performance)
            combined_score = (similarity_score * 0.7) + (performance_score * 0.3)
            
            if combined_score > best_score:
                best_match = agent
                best_score = combined_score
        
        # Only return if similarity is above threshold
        return best_match if best_score > 0.7 else None
    
    async def check_agent_availability(self, agent: dict) -> bool:
        """Check if agent is currently available"""
        try:
            health_status = await self.health_checker.check_agent_health(agent["service_url"])
            return health_status["status"] == "healthy"
        except Exception:
            return False
    
    async def get_agent_performance_score(self, agent_role: str) -> float:
        """Get historical performance score for agent"""
        try:
            # Query recent performance metrics
            recent_executions = await self.analytics_db.get_recent_agent_performance(
                agent_role, 
                days=7
            )
            
            if not recent_executions:
                return 0.5  # Default score for new agents
            
            # Calculate performance score based on multiple factors
            success_rate = recent_executions["success_rate"]
            avg_duration = recent_executions["avg_duration"]
            user_satisfaction = recent_executions["avg_user_rating"]
            
            # Weighted performance score
            performance_score = (
                success_rate * 0.4 +
                (1.0 - min(avg_duration / 120, 1.0)) * 0.3 +  # Normalize duration to 2 minutes
                user_satisfaction * 0.3
            )
            
            return min(performance_score, 1.0)
            
        except Exception:
            return 0.5  # Default score on error
```

### Flow Optimization Engine

```python
class FlowOptimizer:
    def __init__(self):
        self.dependency_resolver = DependencyResolver()
        self.parallel_executor = ParallelExecutionPlanner()
        
    def optimize_sequence(self, selected_agents: List[dict], user_request: str) -> List[dict]:
        """Optimize agent execution sequence for efficiency and quality"""
        
        # 1. Analyze dependencies between agents
        dependencies = self.analyze_agent_dependencies(selected_agents)
        
        # 2. Identify opportunities for parallel execution
        parallel_groups = self.identify_parallel_opportunities(selected_agents, dependencies)
        
        # 3. Optimize for minimal total execution time
        optimized_sequence = self.minimize_execution_time(parallel_groups, dependencies)
        
        # 4. Add quality gates and checkpoints
        final_sequence = self.add_quality_gates(optimized_sequence)
        
        return final_sequence
    
    def analyze_agent_dependencies(self, agents: List[dict]) -> dict:
        """Analyze input/output dependencies between agents"""
        dependencies = {}
        
        for agent in agents:
            agent_role = agent["role_id"]
            agent_inputs = agent.get("expected_inputs", [])
            dependencies[agent_role] = []
            
            # Find agents that produce required inputs
            for other_agent in agents:
                if other_agent["role_id"] == agent_role:
                    continue
                    
                other_outputs = other_agent.get("primary_outputs", [])
                
                # Check if other agent produces inputs we need
                for required_input in agent_inputs:
                    if required_input in other_outputs:
                        dependencies[agent_role].append(other_agent["role_id"])
        
        return dependencies
    
    def identify_parallel_opportunities(self, agents: List[dict], dependencies: dict) -> List[List[dict]]:
        """Identify agents that can run in parallel"""
        parallel_groups = []
        remaining_agents = agents.copy()
        
        while remaining_agents:
            # Find agents with no unfulfilled dependencies
            parallel_group = []
            
            for agent in remaining_agents[:]:
                agent_role = agent["role_id"]
                agent_deps = dependencies.get(agent_role, [])
                
                # Check if all dependencies are satisfied
                unsatisfied_deps = [dep for dep in agent_deps 
                                  if dep in [a["role_id"] for a in remaining_agents]]
                
                if not unsatisfied_deps:
                    parallel_group.append(agent)
                    remaining_agents.remove(agent)
            
            if parallel_group:
                parallel_groups.append(parallel_group)
            else:
                # Break circular dependencies by prioritizing based on complexity
                priority_agent = min(remaining_agents, 
                                   key=lambda a: len(dependencies.get(a["role_id"], [])))
                parallel_groups.append([priority_agent])
                remaining_agents.remove(priority_agent)
        
        return parallel_groups
    
    def minimize_execution_time(self, parallel_groups: List[List[dict]], dependencies: dict) -> List[dict]:
        """Optimize execution order within parallel groups"""
        optimized_sequence = []
        
        for group in parallel_groups:
            if len(group) == 1:
                # Single agent, add directly
                optimized_sequence.extend(group)
            else:
                # Multiple agents in parallel, sort by estimated execution time
                sorted_group = sorted(group, 
                                    key=lambda a: self.estimate_execution_time(a["role_id"]))
                optimized_sequence.extend(sorted_group)
        
        return optimized_sequence
    
    def estimate_execution_time(self, agent_role: str) -> int:
        """Estimate execution time for agent based on historical data"""
        # Default estimates (in seconds)
        default_times = {
            "business_analyst": 300,    # 5 minutes
            "technical_architect": 600, # 10 minutes
            "developer": 900,          # 15 minutes
            "qa_tester": 450,          # 7.5 minutes
            "project_manager": 240     # 4 minutes
        }
        
        # Try to get actual historical average
        try:
            historical_avg = self.analytics_db.get_avg_execution_time(agent_role)
            return historical_avg if historical_avg else default_times.get(agent_role, 600)
        except Exception:
            return default_times.get(agent_role, 600)
```

### Intent Classification Engine

```python
class IntentClassifier:
    def __init__(self):
        self.classification_model = self.load_classification_model()
        self.predefined_patterns = self.load_classification_patterns()
        
    async def classify_user_intent(self, user_request: str) -> dict:
        """Classify user intent to determine workflow type and complexity"""
        
        # 1. Extract keywords and entities
        keywords = await self.extract_keywords(user_request)
        entities = await self.extract_entities(user_request)
        
        # 2. Classify primary domain
        primary_domain = await self.classify_domain(user_request)
        
        # 3. Determine complexity level
        complexity = await self.assess_complexity(user_request, keywords, entities)
        
        # 4. Identify required agent types
        required_agents = await self.identify_required_agents(
            user_request, primary_domain, complexity
        )
        
        return {
            "primary_domain": primary_domain,
            "complexity": complexity,
            "required_agents": required_agents,
            "keywords": keywords,
            "entities": entities,
            "confidence": self.calculate_confidence(user_request, primary_domain)
        }
    
    async def classify_domain(self, user_request: str) -> str:
        """Classify the primary domain of the user request"""
        classification_prompt = f"""
        Classify this user request into the most appropriate primary domain:
        
        Available domains:
        - product_development: Building applications, software, systems
        - marketing_campaign: Marketing, advertising, promotional campaigns
        - technical_support: Troubleshooting, debugging, system issues
        - business_analysis: Analysis, research, strategy, planning
        - content_creation: Writing, documentation, creative content
        - data_analysis: Data processing, insights, reporting
        - project_management: Planning, coordination, resource management
        
        User request: {user_request}
        
        Return only the domain name (e.g., "product_development").
        """
        
        domain = await self.lightweight_llm.complete(classification_prompt)
        return domain.strip().lower()
    
    async def assess_complexity(self, user_request: str, keywords: List[str], entities: List[str]) -> str:
        """Assess the complexity level of the request"""
        complexity_indicators = {
            "simple": [
                "quick", "simple", "basic", "straightforward", "easy",
                "small", "minimal", "prototype", "poc"
            ],
            "medium": [
                "standard", "typical", "normal", "regular", "moderate",
                "professional", "business", "production"
            ],
            "complex": [
                "enterprise", "scalable", "complex", "advanced", "comprehensive",
                "full-featured", "production-ready", "high-performance"
            ]
        }
        
        # Count indicators for each complexity level
        complexity_scores = {}
        for level, indicators in complexity_indicators.items():
            score = sum(1 for indicator in indicators 
                       if any(indicator in keyword.lower() for keyword in keywords))
            complexity_scores[level] = score
        
        # Return complexity with highest score, default to medium
        if complexity_scores:
            return max(complexity_scores.keys(), key=lambda k: complexity_scores[k])
        else:
            return "medium"
    
    async def identify_required_agents(self, user_request: str, domain: str, complexity: str) -> List[str]:
        """Identify which agent types are needed for this request"""
        
        # Domain-based agent mappings
        domain_agents = {
            "product_development": ["business_analyst", "technical_architect", "developer", "qa_tester"],
            "marketing_campaign": ["market_researcher", "campaign_strategist", "creative_director", "media_planner"],
            "technical_support": ["system_analyst", "technical_specialist", "solution_architect"],
            "business_analysis": ["business_analyst", "data_analyst", "strategy_consultant"],
            "content_creation": ["content_strategist", "writer", "editor", "seo_specialist"],
            "data_analysis": ["data_analyst", "statistician", "visualization_specialist"],
            "project_management": ["project_manager", "resource_coordinator", "timeline_planner"]
        }
        
        base_agents = domain_agents.get(domain, ["business_analyst", "project_manager"])
        
        # Adjust based on complexity
        if complexity == "simple":
            # Reduce to essential agents
            return base_agents[:2]
        elif complexity == "complex":
            # Add additional specialist agents
            if domain == "product_development":
                base_agents.extend(["security_specialist", "performance_engineer"])
            elif domain == "marketing_campaign":
                base_agents.extend(["analytics_specialist", "automation_engineer"])
        
        return base_agents
```

### Workflow Configuration Generator

```python
class WorkflowConfigGenerator:
    def __init__(self):
        self.template_engine = Jinja2Environment()
        
    def create_dynamic_workflow_config(self, agents: List[dict], user_request: str, intent_data: dict) -> dict:
        """Create workflow configuration from selected agents and intent"""
        
        workflow_config = {
            "workflow_id": f"dynamic_{int(time.time())}",
            "name": f"Dynamic Workflow - {intent_data['primary_domain'].title()}",
            "description": f"Dynamically generated workflow for: {user_request[:50]}...",
            "generated_at": datetime.now().isoformat(),
            "complexity": intent_data["complexity"],
            "estimated_duration": self.estimate_total_duration(agents),
            "agents": []
        }
        
        # Generate agent configurations
        for i, agent in enumerate(agents):
            agent_config = {
                "role": agent["role_id"],
                "position": i + 1,
                "inputs": self.determine_inputs(agent, i, agents),
                "outputs": self.determine_outputs(agent),
                "timeout_minutes": self.calculate_timeout(agent, intent_data["complexity"]),
                "handoff_conditions": self.generate_handoff_conditions(agent),
                "retry_policy": self.generate_retry_policy(agent)
            }
            
            workflow_config["agents"].append(agent_config)
        
        # Add approval gates for complex workflows
        if intent_data["complexity"] == "complex":
            workflow_config["approval_gates"] = self.generate_approval_gates(agents)
        
        return workflow_config
    
    def determine_inputs(self, agent: dict, position: int, all_agents: List[dict]) -> List[str]:
        """Determine input requirements for agent based on position and dependencies"""
        if position == 0:
            return ["user_request"]
        
        # Look at previous agents' outputs
        inputs = []
        for prev_agent in all_agents[:position]:
            prev_outputs = prev_agent.get("primary_outputs", [])
            agent_expected_inputs = agent.get("expected_inputs", [])
            
            # Add matching outputs as inputs
            for output in prev_outputs:
                if output in agent_expected_inputs:
                    inputs.append(output)
        
        # Ensure at least basic context is passed
        if not inputs:
            inputs = ["user_request"]
            
        return inputs
    
    def determine_outputs(self, agent: dict) -> List[str]:
        """Determine expected outputs from agent"""
        return agent.get("primary_outputs", [f"{agent['role_id']}_output"])
    
    def calculate_timeout(self, agent: dict, complexity: str) -> int:
        """Calculate timeout based on agent type and complexity"""
        base_timeouts = {
            "business_analyst": 8,
            "technical_architect": 12,
            "developer": 20,
            "qa_tester": 10,
            "project_manager": 6
        }
        
        complexity_multipliers = {
            "simple": 0.7,
            "medium": 1.0,
            "complex": 1.5
        }
        
        base_timeout = base_timeouts.get(agent["role_id"], 10)
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        return int(base_timeout * multiplier)
    
    def generate_handoff_conditions(self, agent: dict) -> List[str]:
        """Generate conditions that must be met before handoff"""
        return [
            f"{agent['role_id']}_task_complete",
            f"{agent['role_id']}_quality_validated",
            f"{agent['role_id']}_outputs_generated"
        ]
```

This Dynamic Flow Assembly Engine provides the intelligence needed to create optimal workflows on-the-fly, matching user needs with available agent capabilities while optimizing for efficiency and quality.