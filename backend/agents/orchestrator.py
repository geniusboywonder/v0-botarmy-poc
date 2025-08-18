import controlflow as cf
from typing import Dict, Any, List, Optional, Callable
from .specialized_agents import (
    AnalystAgent, ArchitectAgent, DeveloperAgent,
    TesterAgent, DeployerAgent, MonitorAgent
)
from .base_agent import AgentStatus
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Orchestrates the 6 specialized agents using ControlFlow"""
    
    def __init__(self):
        # Initialize all agents
        self.agents = {
            "analyst": AnalystAgent(),
            "architect": ArchitectAgent(),
            "developer": DeveloperAgent(),
            "tester": TesterAgent(),
            "deployer": DeployerAgent(),
            "monitor": MonitorAgent()
        }
        
        self.active_workflows: Dict[str, Any] = {}
        self.workflow_history: List[Dict[str, Any]] = []
        
        self.websocket_callback: Optional[Callable] = None
    
    def set_websocket_callback(self, callback: Callable):
        """Set WebSocket callback for all agents and orchestrator"""
        self.websocket_callback = callback
        
        # Set callback for all agents
        for agent in self.agents.values():
            agent.set_websocket_callback(callback)
    
    async def _send_orchestrator_update(self, update_type: str, data: Dict[str, Any] = None):
        """Send orchestrator-level updates"""
        if self.websocket_callback:
            update_data = {
                "type": update_type,
                "source": "orchestrator",
                "timestamp": datetime.now().isoformat(),
                **(data or {})
            }
            try:
                await self.websocket_callback(update_data)
            except Exception as e:
                logger.error(f"Orchestrator WebSocket update failed: {e}")
    
    async def start_project_workflow(self, project_description: str, requirements: Dict[str, Any]) -> str:
        """Start a complete SDLC workflow for a new project"""
        workflow_id = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"Starting project workflow {workflow_id}")
        
        # Create workflow context
        workflow_context = {
            "workflow_id": workflow_id,
            "project_description": project_description,
            "requirements": requirements,
            "started_at": datetime.now().isoformat(),
            "status": "in_progress"
        }
        
        self.active_workflows[workflow_id] = workflow_context
        
        await self._send_orchestrator_update("workflow_started", {
            "workflow_id": workflow_id,
            "project_description": project_description
        })
        
        # Start the workflow asynchronously
        asyncio.create_task(self._execute_sdlc_workflow(workflow_id, workflow_context))
        
        return workflow_id
    
    async def _execute_sdlc_workflow(self, workflow_id: str, context: Dict[str, Any]):
        """Execute the complete SDLC workflow with real-time updates"""
        try:
            await self._send_orchestrator_update("workflow_progress", {
                "workflow_id": workflow_id,
                "phase": "analysis",
                "progress": 0
            })
            
            # Phase 1: Requirements Analysis
            analysis_result = await self.agents["analyst"].execute_task(
                f"Analyze requirements for: {context['project_description']}",
                context
            )
            context["analysis"] = analysis_result
            
            await self._send_orchestrator_update("workflow_progress", {
                "workflow_id": workflow_id,
                "phase": "architecture",
                "progress": 16.7
            })
            
            # Phase 2: Architecture Design
            if analysis_result["success"]:
                architecture_result = await self.agents["architect"].execute_task(
                    f"Design architecture based on analysis: {analysis_result['result']}",
                    context
                )
                context["architecture"] = architecture_result
                
                await self._send_orchestrator_update("workflow_progress", {
                    "workflow_id": workflow_id,
                    "phase": "development",
                    "progress": 33.3
                })
                
                # Phase 3: Development
                if architecture_result["success"]:
                    development_result = await self.agents["developer"].execute_task(
                        f"Implement solution based on architecture: {architecture_result['result']}",
                        context
                    )
                    context["development"] = development_result
                    
                    await self._send_orchestrator_update("workflow_progress", {
                        "workflow_id": workflow_id,
                        "phase": "testing",
                        "progress": 50.0
                    })
                    
                    # Phase 4: Testing
                    if development_result["success"]:
                        testing_result = await self.agents["tester"].execute_task(
                            f"Test implementation: {development_result['result']}",
                            context
                        )
                        context["testing"] = testing_result
                        
                        await self._send_orchestrator_update("workflow_progress", {
                            "workflow_id": workflow_id,
                            "phase": "deployment",
                            "progress": 66.7
                        })
                        
                        # Phase 5: Deployment
                        if testing_result["success"]:
                            deployment_result = await self.agents["deployer"].execute_task(
                                f"Deploy tested solution: {testing_result['result']}",
                                context
                            )
                            context["deployment"] = deployment_result
                            
                            await self._send_orchestrator_update("workflow_progress", {
                                "workflow_id": workflow_id,
                                "phase": "monitoring",
                                "progress": 83.3
                            })
                            
                            # Phase 6: Monitoring Setup
                            if deployment_result["success"]:
                                monitoring_result = await self.agents["monitor"].execute_task(
                                    f"Set up monitoring for deployed solution: {deployment_result['result']}",
                                    context
                                )
                                context["monitoring"] = monitoring_result
            
            # Mark workflow as completed
            context["status"] = "completed"
            context["completed_at"] = datetime.now().isoformat()
            
            await self._send_orchestrator_update("workflow_completed", {
                "workflow_id": workflow_id,
                "progress": 100.0
            })
            
            # Move to history
            self.workflow_history.append(context)
            del self.active_workflows[workflow_id]
            
            logger.info(f"Workflow {workflow_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {e}")
            context["status"] = "failed"
            context["error"] = str(e)
            context["failed_at"] = datetime.now().isoformat()
            
            await self._send_orchestrator_update("workflow_failed", {
                "workflow_id": workflow_id,
                "error": str(e)
            })
    
    async def get_agent_status(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get status of specific agent or all agents"""
        if agent_name and agent_name in self.agents:
            return self.agents[agent_name].get_status_info()
        
        return {
            agent_name: agent.get_status_info() 
            for agent_name, agent in self.agents.items()
        }
    
    async def send_message_to_agent(self, agent_name: str, message: str) -> Dict[str, Any]:
        """Send a direct message to a specific agent"""
        if agent_name not in self.agents:
            return {
                "success": False,
                "error": f"Agent {agent_name} not found"
            }
        
        agent = self.agents[agent_name]
        return await agent.execute_task(f"Respond to user message: {message}")
    
    def get_workflow_status(self, workflow_id: Optional[str] = None) -> Dict[str, Any]:
        """Get status of specific workflow or all active workflows"""
        if workflow_id:
            if workflow_id in self.active_workflows:
                return self.active_workflows[workflow_id]
            else:
                # Check history
                for workflow in self.workflow_history:
                    if workflow["workflow_id"] == workflow_id:
                        return workflow
                return {"error": "Workflow not found"}
        
        return {
            "active_workflows": list(self.active_workflows.keys()),
            "completed_workflows": len(self.workflow_history),
            "total_agents": len(self.agents)
        }

# Global orchestrator instance
orchestrator = AgentOrchestrator()
