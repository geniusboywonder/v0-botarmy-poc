"""
Lightweight Multi-Agent Orchestrator for SDLC Workflow
Replaces ControlFlow/Prefect with simple sequential agent handoffs using OpenAI directly
"""

import asyncio
import json
import os
import yaml
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from backend.services.llm_service import LLMService
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.agui.protocol import agui_handler

import logging
logger = logging.getLogger(__name__)


class SDLCOrchestrator:
    """
    Lightweight multi-agent orchestrator for SDLC workflow.
    Manages sequential handoffs: Analyst → Architect → Developer → Tester → Deployer
    """
    
    def __init__(self, llm_service: LLMService, status_broadcaster: AgentStatusBroadcaster):
        self.llm_service = llm_service
        self.status_broadcaster = status_broadcaster
        
        # Load SDLC process configuration
        self.process_config = self._load_process_config()
        
        # Initialize agent configurations (simple dict-based approach)
        self.agent_configs = self._create_agent_configs()
        
        # Artifact storage
        self.artifacts_dir = Path("artifacts")
        self.artifacts_dir.mkdir(exist_ok=True)
        
    def _load_process_config(self) -> Dict[str, Any]:
        """Load SDLC process configuration from YAML"""
        # Use absolute path from project root
        config_path = Path(__file__).parent.parent / "configs" / "processes" / "sdlc.yaml"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.info(f"Successfully loaded SDLC config from {config_path}")
                return config
        except Exception as e:
            logger.error(f"Failed to load SDLC config from {config_path}: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Fallback configuration if YAML loading fails"""
        return {
            "roles": [
                {"name": "Analyst", "stage_involvement": ["Analyze"]},
                {"name": "Architect", "stage_involvement": ["Design"]}, 
                {"name": "Developer", "stage_involvement": ["Build"]},
                {"name": "Tester", "stage_involvement": ["Validate"]},
                {"name": "Deployer", "stage_involvement": ["Launch"]}
            ],
            "stages": {
                "Analyze": {"description": "Analyze project brief"},
                "Design": {"description": "Design architecture"},
                "Build": {"description": "Create implementation plan"},
                "Validate": {"description": "Create test plan"},
                "Launch": {"description": "Create deployment plan"}
            }
        }
    
    def _create_agent_configs(self) -> Dict[str, Dict[str, Any]]:
        """Create agent configurations from SDLC configuration"""
        agents = {}
        
        for role_config in self.process_config.get("roles", []):
            role_name = role_config["name"]
            description = role_config.get("description", f"You are a {role_name} agent.")
            
            # Create simple agent configuration
            agents[role_name] = {
                "name": role_name,
                "instructions": description,
                "model": "gpt-4o-mini",
                "stage_involvement": role_config.get("stage_involvement", [])
            }
            
            logger.info(f"Created {role_name} agent configuration")
        
        return agents
    
    def _write_artifact(self, filename: str, content: str) -> bool:
        """Write artifact to filesystem"""
        try:
            filepath = self.artifacts_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Artifact written: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to write artifact {filename}: {e}")
            return False
    
    def _read_artifact(self, filename: str) -> Optional[str]:
        """Read artifact from filesystem"""
        try:
            filepath = self.artifacts_dir / filename
            if not filepath.exists():
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Artifact read: {filepath}")
            return content
        except Exception as e:
            logger.error(f"Failed to read artifact {filename}: {e}")
            return None
    
    async def run_workflow(self, project_brief: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Execute SDLC workflow with lightweight multi-agent orchestration
        Returns workflow results and artifacts
        """
        logger.info(f"Starting SDLC workflow for session: {session_id}")
        
        try:
            # Execute workflow stages
            results = {}
            current_context = project_brief
            
            # Define workflow sequence
            workflow_sequence = [
                ("Analyst", "Requirements Document", "requirements.md"),
                ("Architect", "Architecture Document", "architecture.md"), 
                ("Developer", "Implementation Plan", "implementation_plan.md"),
                ("Tester", "Test Plan", "test_plan.md"),
                ("Deployer", "Deployment Plan", "deployment_plan.md")
            ]
            
            for i, (agent_name, artifact_name, filename) in enumerate(workflow_sequence):
                logger.info(f"Executing stage {i+1}/5: {agent_name}")
                
                # Broadcast agent status - starting
                await self.status_broadcaster.broadcast_agent_status(
                    agent_name=agent_name,
                    status="working",
                    task=f"Create {artifact_name}",
                    session_id=session_id
                )
                
                try:
                    # Get agent config
                    agent_config = self.agent_configs.get(agent_name)
                    if not agent_config:
                        raise ValueError(f"Agent {agent_name} not found")
                    
                    # Prepare prompt for LLM call
                    prompt = f"""
{agent_config["instructions"]}

Your task: Create the {artifact_name}

Project context: {current_context}

Instructions:
1. Create a comprehensive {artifact_name} based on the project context
2. Format your response in Markdown
3. Keep it under 500 words
4. Focus on {agent_name.lower()}-specific aspects

Please provide your response now:
"""
                    
                    # Call LLM directly using generate_response method
                    response_content = await self.llm_service.generate_response(
                        prompt=prompt,
                        agent_name=agent_name,
                        preferred_provider=None
                    )
                    
                    # Write artifact to filesystem
                    artifact_saved = self._write_artifact(filename, response_content)
                    
                    # Store result
                    results[agent_name] = {
                        "agent": agent_name,
                        "artifact": artifact_name,
                        "filename": filename,
                        "response": response_content,
                        "artifact_saved": artifact_saved,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Update context for next agent
                    current_context = response_content
                    
                    # Broadcast completion
                    await self.status_broadcaster.broadcast_agent_completed(
                        agent_name=agent_name,
                        result=f"Completed {artifact_name}",
                        session_id=session_id
                    )
                    
                    logger.info(f"Completed {agent_name} stage - artifact saved: {artifact_saved}")
                    
                except Exception as e:
                    logger.error(f"Error in {agent_name} stage: {e}")
                    
                    # Broadcast error
                    await self.status_broadcaster.broadcast_agent_error(
                        agent_name=agent_name,
                        error_message=str(e),
                        session_id=session_id
                    )
                    
                    # Continue with fallback
                    results[agent_name] = {
                        "agent": agent_name,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Create summary
            workflow_summary = {
                "workflow_id": f"sdlc_{session_id}_{int(datetime.now().timestamp())}",
                "session_id": session_id,
                "project_brief": project_brief,
                "results": results,
                "completed_at": datetime.now().isoformat(),
                "artifacts_created": len([r for r in results.values() if "error" not in r])
            }
            
            logger.info(f"SDLC workflow completed: {workflow_summary['workflow_id']}")
            return workflow_summary
            
        except Exception as e:
            logger.error(f"SDLC workflow failed: {e}")
            raise
    
class LightweightMultiAgentWorkflow:
    """
    Main workflow class that replaces the ControlFlow botarmy_workflow function
    """
    
    def __init__(self, llm_service: LLMService, status_broadcaster: AgentStatusBroadcaster):
        self.orchestrator = SDLCOrchestrator(llm_service, status_broadcaster)
    
    async def execute(self, project_brief: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Execute the SDLC workflow
        This replaces the botarmy_workflow function
        """
        logger.info(f"Starting lightweight multi-agent workflow for: {project_brief[:50]}...")
        
        try:
            result = await self.orchestrator.run_workflow(project_brief, session_id)
            logger.info("Lightweight multi-agent workflow completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Lightweight multi-agent workflow failed: {e}")
            raise


# Factory function to create workflow instance
def create_openai_agents_workflow(llm_service: LLMService, status_broadcaster: AgentStatusBroadcaster) -> LightweightMultiAgentWorkflow:
    """Create and return lightweight multi-agent workflow instance"""
    return LightweightMultiAgentWorkflow(llm_service, status_broadcaster)