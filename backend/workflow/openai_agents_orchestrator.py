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
    
    def _get_ordered_tasks(self) -> List[Dict[str, Any]]:
        """Parse YAML configuration and return tasks in proper dependency order"""
        try:
            ordered_tasks = []
            stages = self.process_config.get("stages", {})
            
            # Get all tasks with their stage information
            for stage_name, stage_config in stages.items():
                stage_tasks = stage_config.get("tasks", [])
                
                for task in stage_tasks:
                    task_info = {
                        "stage": stage_name,
                        "name": task.get("name", ""),
                        "role": task.get("role", ""),
                        "input_artifacts": task.get("input_artifacts", []),
                        "output_artifacts": task.get("output_artifacts", []),
                        "depends_on": task.get("depends_on", []),
                        "description": stage_config.get("description", "")
                    }
                    ordered_tasks.append(task_info)
            
            # Sort tasks by dependencies (simple dependency resolution)
            # This ensures execution plans are created before main tasks
            sorted_tasks = []
            completed_tasks = set()
            
            while len(sorted_tasks) < len(ordered_tasks):
                for task in ordered_tasks:
                    if task["name"] not in completed_tasks:
                        # Check if all dependencies are completed
                        dependencies_met = all(dep in completed_tasks for dep in task["depends_on"])
                        
                        if dependencies_met:
                            sorted_tasks.append(task)
                            completed_tasks.add(task["name"])
                            break
                else:
                    # If no task can be added, there might be circular dependencies
                    remaining_tasks = [task["name"] for task in ordered_tasks if task["name"] not in completed_tasks]
                    logger.warning(f"Possible circular dependency or missing tasks: {remaining_tasks}")
                    break
            
            logger.info(f"Ordered {len(sorted_tasks)} tasks for execution")
            return sorted_tasks
            
        except Exception as e:
            logger.error(f"Failed to parse task order from YAML: {e}")
            # Fallback to simple task list if parsing fails
            return []
    
    async def run_workflow(self, project_brief: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Execute SDLC workflow with lightweight multi-agent orchestration
        Returns workflow results and artifacts
        """
        logger.info(f"Starting SDLC workflow for session: {session_id}")
        
        try:
            # Execute workflow stages dynamically from YAML configuration
            results = {}
            artifacts_created = {}  # Track created artifacts for task dependencies
            artifacts_created["Project Brief"] = project_brief  # Initialize with project brief
            
            # Get all tasks in dependency order from YAML stages
            all_tasks = self._get_ordered_tasks()
            total_tasks = len(all_tasks)
            
            for i, task_info in enumerate(all_tasks):
                task_name = task_info["name"]
                agent_name = task_info["role"]
                stage_name = task_info["stage"]
                
                logger.info(f"Executing task {i+1}/{total_tasks}: {task_name} (Agent: {agent_name})")
                
                # Broadcast agent status - starting
                await self.status_broadcaster.broadcast_agent_status(
                    agent_name=agent_name,
                    status="working",
                    task=task_name,
                    session_id=session_id
                )
                
                try:
                    # Get agent config
                    agent_config = self.agent_configs.get(agent_name)
                    if not agent_config:
                        raise ValueError(f"Agent {agent_name} not found")
                    
                    # Build context from input artifacts
                    context_parts = []
                    for input_artifact in task_info["input_artifacts"]:
                        if input_artifact in artifacts_created:
                            context_parts.append(f"**{input_artifact}:**\n{artifacts_created[input_artifact]}")
                    
                    combined_context = "\n\n---\n\n".join(context_parts) if context_parts else project_brief
                    
                    # Determine output artifact name
                    output_artifacts = task_info["output_artifacts"]
                    primary_output = output_artifacts[0] if output_artifacts else "document"
                    
                    # Prepare prompt for LLM call
                    prompt = f"""
{agent_config["instructions"]}

Your task: {task_name}
Target output: {primary_output}

Available context and input artifacts:
{combined_context}

Instructions:
1. Create a comprehensive {primary_output} following the task requirements
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
                    
                    # Generate filename from artifact name
                    artifact_filename = f"{primary_output.lower().replace(' ', '_')}.md"
                    
                    # Write artifact to filesystem
                    artifact_saved = self._write_artifact(artifact_filename, response_content)
                    
                    # Store the artifact content for future tasks
                    artifacts_created[primary_output] = response_content
                    
                    # Store result
                    task_key = f"{agent_name}_{task_name}"
                    results[task_key] = {
                        "task_name": task_name,
                        "stage": stage_name,
                        "agent": agent_name,
                        "artifact": primary_output,
                        "filename": artifact_filename,
                        "response": response_content,
                        "artifact_saved": artifact_saved,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Broadcast completion
                    await self.status_broadcaster.broadcast_agent_completed(
                        agent_name=agent_name,
                        result=f"Completed {task_name}",
                        session_id=session_id
                    )
                    
                    logger.info(f"Completed {task_name} ({agent_name}) - artifact saved: {artifact_saved}")
                    
                except Exception as e:
                    logger.error(f"Error in {task_name} ({agent_name}): {e}")
                    
                    # Broadcast error
                    await self.status_broadcaster.broadcast_agent_error(
                        agent_name=agent_name,
                        error_message=str(e),
                        session_id=session_id
                    )
                    
                    # Continue with fallback
                    task_key = f"{agent_name}_{task_name}"
                    results[task_key] = {
                        "task_name": task_name,
                        "stage": stage_name,
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
                "tasks_completed": len([r for r in results.values() if "error" not in r]),
                "artifacts_created": len(artifacts_created) - 1  # Subtract 1 for Project Brief
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