"""
Simple working orchestrator that creates actual artifacts and updates UI
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class SimpleWorkflowOrchestrator:
    """Simple orchestrator that actually creates artifacts and updates process store"""
    
    def __init__(self, llm_service, status_broadcaster):
        self.llm_service = llm_service
        self.status_broadcaster = status_broadcaster
        
        # Create artifacts directory
        self.artifacts_dir = Path("artifacts")
        self.artifacts_dir.mkdir(exist_ok=True)
        
        # Simple SDLC stages
        self.stages = [
            {"name": "Analyst", "stage": "Analyze", "task": "Requirements Analysis", "artifact": "requirements_document.md"},
            {"name": "Architect", "stage": "Design", "task": "System Design", "artifact": "system_design.md"},
            {"name": "Developer", "stage": "Build", "task": "Implementation Plan", "artifact": "implementation_plan.md"},
            {"name": "Tester", "stage": "Validate", "task": "Test Plan", "artifact": "test_plan.md"},
            {"name": "Deployer", "stage": "Launch", "task": "Deployment Plan", "artifact": "deployment_plan.md"}
        ]
    
    async def execute_workflow(self, project_brief: str, session_id: str = "default") -> Dict[str, Any]:
        """Execute the SDLC workflow with proper artifact creation"""
        logger.info(f"Starting simple workflow for: {project_brief[:50]}...")
        
        try:
            results = {}
            
            for i, stage_config in enumerate(self.stages):
                agent_name = stage_config["name"]
                stage_name = stage_config["stage"]
                task_name = stage_config["task"]
                artifact_filename = stage_config["artifact"]
                
                logger.info(f"Executing {agent_name} - {task_name}")
                
                # Broadcast starting status
                await self.status_broadcaster.broadcast_agent_status(
                    agent_name=agent_name,
                    status="working",
                    task=task_name,
                    session_id=session_id
                )
                
                # Generate content using LLM
                prompt = f"""
You are a {agent_name} working on: {project_brief}

Your task is to create a {task_name}.

Please provide a comprehensive {task_name.lower()} that includes:
- Clear objectives and requirements
- Technical specifications
- Implementation details
- Dependencies and assumptions

Format your response as a professional document in Markdown format.
Keep it detailed but concise (300-500 words).

Project Brief: {project_brief}
"""
                
                try:
                    # Call LLM service
                    response_content = await self.llm_service.generate_response(
                        prompt=prompt,
                        agent_name=agent_name,
                        preferred_provider="openai"
                    )
                    
                    # Create artifact file
                    artifact_path = self.artifacts_dir / artifact_filename
                    with open(artifact_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {task_name}\n\n")
                        f.write(f"**Agent:** {agent_name}\n")
                        f.write(f"**Project:** {project_brief}\n")
                        f.write(f"**Created:** {datetime.now().isoformat()}\n\n")
                        f.write("---\n\n")
                        f.write(response_content)
                    
                    logger.info(f"Created artifact: {artifact_path}")
                    
                    # Store result
                    results[agent_name] = {
                        "agent": agent_name,
                        "stage": stage_name,
                        "task": task_name,
                        "artifact_file": str(artifact_path),
                        "content": response_content,
                        "status": "completed",
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Broadcast completion
                    await self.status_broadcaster.broadcast_agent_completed(
                        agent_name=agent_name,
                        result=f"Completed {task_name} - Created {artifact_filename}",
                        session_id=session_id
                    )
                    
                    # Send response to chat as well
                    await self.status_broadcaster.broadcast_agent_response(
                        agent_name=agent_name,
                        content=f"✅ **{task_name} Complete**\n\n📄 Created artifact: `{artifact_filename}`\n\nSummary: {response_content[:200]}...",
                        session_id=session_id
                    )
                    
                    logger.info(f"Completed {agent_name} - {task_name}")
                    
                except Exception as e:
                    logger.error(f"Error in {agent_name} stage: {e}")
                    
                    # Broadcast error
                    await self.status_broadcaster.broadcast_agent_error(
                        agent_name=agent_name,
                        error_message=str(e),
                        session_id=session_id
                    )
                    
                    results[agent_name] = {
                        "agent": agent_name,
                        "stage": stage_name,
                        "task": task_name,
                        "error": str(e),
                        "status": "error",
                        "timestamp": datetime.now().isoformat()
                    }
                
                # Short delay between stages
                await asyncio.sleep(1)
            
            # Create workflow summary
            summary = {
                "workflow_id": f"simple_workflow_{session_id}_{int(datetime.now().timestamp())}",
                "project_brief": project_brief,
                "session_id": session_id,
                "results": results,
                "completed_stages": len([r for r in results.values() if r.get("status") == "completed"]),
                "total_stages": len(self.stages),
                "artifacts_created": list(self.artifacts_dir.glob("*.md")),
                "completed_at": datetime.now().isoformat()
            }
            
            logger.info(f"Simple workflow completed: {summary['completed_stages']}/{summary['total_stages']} stages")
            return summary
            
        except Exception as e:
            logger.error(f"Simple workflow failed: {e}")
            raise


def create_simple_workflow(llm_service, status_broadcaster):
    """Factory function to create simple workflow"""
    return SimpleWorkflowOrchestrator(llm_service, status_broadcaster)