from .base_agent import BaseAgent, AgentStatus
from typing import Dict, Any
import controlflow as cf
import openai
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AnalystAgent(BaseAgent):
    """Requirements analysis and project planning agent"""
    
    def __init__(self):
        super().__init__(
            name="Analyst",
            description="Analyzes requirements and creates project specifications",
            instructions="""
            You are a senior business analyst specializing in software requirements.
            Your role is to:
            1. Analyze user requirements and business needs
            2. Create detailed project specifications
            3. Identify potential risks and constraints
            4. Define success criteria and acceptance criteria
            5. Communicate findings clearly to technical teams
            
            Always be thorough, ask clarifying questions, and provide structured output.
            Format your responses in clear sections with actionable recommendations.
            """
        )
    
    async def analyze_requirements(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze user requirements and create structured specifications"""
        analysis_prompt = f"""
        Analyze the following user requirements and provide a structured analysis:
        
        User Input: {user_input}
        Context: {context or {}}
        
        Please provide:
        1. Requirements Summary
        2. Functional Requirements
        3. Non-functional Requirements
        4. Assumptions and Constraints
        5. Success Criteria
        6. Potential Risks
        7. Recommended Next Steps
        """
        
        return await self.execute_task(analysis_prompt, context)
    
    async def create_user_stories(self, requirements: str) -> Dict[str, Any]:
        """Convert requirements into user stories"""
        story_prompt = f"""
        Convert the following requirements into well-structured user stories:
        
        Requirements: {requirements}
        
        Format each user story as:
        - As a [user type], I want [functionality] so that [benefit]
        - Acceptance Criteria: [specific criteria]
        - Priority: [High/Medium/Low]
        """
        
        return await self.execute_task(story_prompt)

class ArchitectAgent(BaseAgent):
    """System architecture and design agent"""
    
    def __init__(self):
        super().__init__(
            name="Architect",
            description="Designs system architecture and technical specifications",
            instructions="""
            You are a senior software architect with expertise in modern web technologies.
            Your role is to:
            1. Design scalable system architectures
            2. Choose appropriate technologies and frameworks
            3. Create technical specifications and diagrams
            4. Define API contracts and data models
            5. Ensure security and performance considerations
            
            Focus on best practices, maintainability, and scalability.
            Provide detailed technical recommendations with justifications.
            """
        )
    
    async def design_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design system architecture based on requirements"""
        architecture_prompt = f"""
        Design a system architecture for the following requirements:
        
        Requirements: {requirements}
        
        Please provide:
        1. High-level Architecture Overview
        2. Technology Stack Recommendations
        3. Database Design
        4. API Design
        5. Security Considerations
        6. Performance Considerations
        7. Deployment Architecture
        """
        
        return await self.execute_task(architecture_prompt, requirements)
    
    async def create_api_specification(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed API specifications"""
        api_prompt = f"""
        Create detailed API specifications based on this architecture:
        
        Architecture: {architecture}
        
        Include:
        1. Endpoint definitions
        2. Request/Response schemas
        3. Authentication methods
        4. Error handling
        5. Rate limiting
        """
        
        return await self.execute_task(api_prompt, architecture)

class DeveloperAgent(BaseAgent):
    """Code development and implementation agent"""
    
    def __init__(self):
        super().__init__(
            name="Developer",
            description="Implements features and writes production-ready code",
            instructions="""
            You are a senior full-stack developer with expertise in React, Node.js, and Python.
            Your role is to:
            1. Write clean, maintainable, and well-documented code
            2. Implement features according to specifications
            3. Follow coding standards and best practices
            4. Create unit tests for your code
            5. Optimize for performance and security
            
            Always write production-ready code with proper error handling.
            Include comments and documentation for complex logic.
            """
        )
    
    async def implement_feature(self, specification: Dict[str, Any], technology_stack: str) -> Dict[str, Any]:
        """Implement a feature based on specifications"""
        implementation_prompt = f"""
        Implement the following feature using {technology_stack}:
        
        Specification: {specification}
        
        Provide:
        1. Complete code implementation
        2. Unit tests
        3. Documentation
        4. Error handling
        5. Performance considerations
        """
        
        return await self.execute_task(implementation_prompt, specification)
    
    async def review_code(self, code: str, standards: Dict[str, Any] = None) -> Dict[str, Any]:
        """Review code for quality and best practices"""
        review_prompt = f"""
        Review the following code for quality, security, and best practices:
        
        Code: {code}
        Standards: {standards or {}}
        
        Provide:
        1. Code quality assessment
        2. Security vulnerabilities
        3. Performance issues
        4. Improvement suggestions
        5. Compliance with standards
        """
        
        return await self.execute_task(review_prompt, {"code": code, "standards": standards})

class TesterAgent(BaseAgent):
    """Quality assurance and testing agent"""
    
    def __init__(self):
        super().__init__(
            name="Tester",
            description="Performs testing and quality assurance",
            instructions="""
            You are a senior QA engineer specializing in automated and manual testing.
            Your role is to:
            1. Create comprehensive test plans and test cases
            2. Perform functional, integration, and performance testing
            3. Identify bugs and quality issues
            4. Verify that requirements are met
            5. Ensure accessibility and usability standards
            
            Be thorough and detail-oriented in your testing approach.
            Provide clear bug reports with reproduction steps.
            """
        )
    
    async def create_test_plan(self, requirements: Dict[str, Any], features: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive test plan"""
        test_plan_prompt = f"""
        Create a comprehensive test plan for:
        
        Requirements: {requirements}
        Features: {features}
        
        Include:
        1. Test Strategy
        2. Test Cases (Functional)
        3. Test Cases (Non-functional)
        4. Integration Tests
        5. Performance Tests
        6. Security Tests
        7. Acceptance Criteria Validation
        """
        
        return await self.execute_task(test_plan_prompt, {"requirements": requirements, "features": features})
    
    async def execute_tests(self, test_plan: Dict[str, Any], implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tests and report results"""
        test_execution_prompt = f"""
        Execute the following test plan against the implementation:
        
        Test Plan: {test_plan}
        Implementation: {implementation}
        
        Provide:
        1. Test Results Summary
        2. Passed Tests
        3. Failed Tests with Details
        4. Bug Reports
        5. Quality Assessment
        6. Recommendations
        """
        
        return await self.execute_task(test_execution_prompt, {"test_plan": test_plan, "implementation": implementation})

class DeployerAgent(BaseAgent):
    """Deployment and DevOps agent"""
    
    def __init__(self):
        super().__init__(
            name="Deployer",
            description="Handles deployment and infrastructure management",
            instructions="""
            You are a senior DevOps engineer specializing in cloud deployments.
            Your role is to:
            1. Set up CI/CD pipelines
            2. Configure deployment environments
            3. Manage infrastructure as code
            4. Ensure security and compliance
            5. Monitor deployment health and performance
            
            Focus on automation, reliability, and security.
            Provide detailed deployment procedures and rollback plans.
            """
        )
    
    async def create_deployment_plan(self, architecture: Dict[str, Any], environment: str) -> Dict[str, Any]:
        """Create deployment plan for specific environment"""
        deployment_prompt = f"""
        Create a deployment plan for {environment} environment:
        
        Architecture: {architecture}
        
        Include:
        1. Infrastructure Requirements
        2. CI/CD Pipeline Configuration
        3. Environment Configuration
        4. Security Setup
        5. Monitoring Setup
        6. Rollback Procedures
        7. Health Checks
        """
        
        return await self.execute_task(deployment_prompt, {"architecture": architecture, "environment": environment})
    
    async def deploy_application(self, deployment_plan: Dict[str, Any], code: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy application according to plan"""
        deploy_prompt = f"""
        Deploy the application using this plan:
        
        Deployment Plan: {deployment_plan}
        Code: {code}
        
        Provide:
        1. Deployment Steps
        2. Configuration Files
        3. Infrastructure Setup
        4. Verification Procedures
        5. Monitoring Configuration
        """
        
        return await self.execute_task(deploy_prompt, {"plan": deployment_plan, "code": code})

class MonitorAgent(BaseAgent):
    """System monitoring and maintenance agent"""
    
    def __init__(self):
        super().__init__(
            name="Monitor",
            description="Monitors system health and performance",
            instructions="""
            You are a senior site reliability engineer specializing in system monitoring.
            Your role is to:
            1. Monitor system health and performance metrics
            2. Set up alerts and notifications
            3. Analyze logs and identify issues
            4. Perform root cause analysis
            5. Recommend optimizations and improvements
            
            Be proactive in identifying and resolving issues.
            Provide actionable insights and recommendations.
            """
        )
    
    async def setup_monitoring(self, deployment: Dict[str, Any]) -> Dict[str, Any]:
        """Set up comprehensive monitoring for deployed system"""
        monitoring_prompt = f"""
        Set up monitoring for the deployed system:
        
        Deployment: {deployment}
        
        Include:
        1. Key Performance Indicators (KPIs)
        2. Health Check Endpoints
        3. Alert Configurations
        4. Log Aggregation Setup
        5. Dashboard Configuration
        6. Incident Response Procedures
        """
        
        return await self.execute_task(monitoring_prompt, deployment)
    
    async def analyze_performance(self, metrics: Dict[str, Any], logs: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze system performance and identify issues"""
        analysis_prompt = f"""
        Analyze system performance based on:
        
        Metrics: {metrics}
        Logs: {logs}
        
        Provide:
        1. Performance Summary
        2. Identified Issues
        3. Root Cause Analysis
        4. Optimization Recommendations
        5. Preventive Measures
        """
        
        return await self.execute_task(analysis_prompt, {"metrics": metrics, "logs": logs})
