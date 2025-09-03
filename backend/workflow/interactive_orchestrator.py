import logging
import asyncio
from typing import Dict, Any

from backend.services.enhanced_process_config_loader import get_enhanced_process_config_loader
from backend.agents.interactive_agent_executor import InteractiveAgentExecutor
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.services.interactive_session_manager import InteractiveSessionManager
# from backend.database.models import WorkflowSession, HITLCheckpoint, ScaffoldedArtifact
# from backend.database.session import get_session

logger = logging.getLogger(__name__)

class InteractiveWorkflowOrchestrator:
    """
    Orchestrates interactive workflows based on flexible YAML configurations.
    """
    def __init__(self, status_broadcaster: AgentStatusBroadcaster):
        self.config_loader = get_enhanced_process_config_loader()
        self.status_broadcaster = status_broadcaster
        self.session_manager = InteractiveSessionManager(status_broadcaster)
        # self.db_session = get_session()

    async def execute(self, config_name: str, project_brief: str, session_id: str):
        """
        Main execution method for an interactive workflow.
        """
        logger.info(f"🚀 Starting interactive workflow '{config_name}' for session '{session_id}'.")

        try:
            config = self.config_loader.get_config(config_name)
            logger.info(f"Successfully loaded configuration for '{config['process_name']}'.")
        except Exception as e:
            logger.error(f"Failed to load process configuration '{config_name}': {e}")
            await self.status_broadcaster.broadcast_agent_response("System", f"Error: Could not load process config '{config_name}'.", session_id)
            return

        interactive_config = config.get('interactive_config', {})
        artifacts = {"Project Brief": project_brief}

        # Step 1: Requirements Gathering (if enabled)
        if interactive_config.get('requirements_gathering', {}).get('enabled'):
            artifacts = await self.handle_requirements_gathering(config, project_brief, session_id, artifacts)

        # Step 2: User Approval Checkpoint (if configured)
        # Placeholder for now

        # Step 3: Sequential Stage Execution
        await self.execute_stages(config, session_id, artifacts)

        logger.info(f"🏁 Interactive workflow '{config_name}' completed for session '{session_id}'.")
        await self.status_broadcaster.broadcast_agent_response("System", f"Workflow '{config_name}' finished.", session_id)

    async def handle_requirements_gathering(self, config: Dict[str, Any], project_brief: str, session_id: str, artifacts: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Gathering requirements for session '{session_id}'...")
        await self.status_broadcaster.broadcast_agent_response("System", "Gathering requirements...", session_id)

        analyst_role = next((r for r in config['roles'] if r['name'] == 'Analyst'), None)
        if not analyst_role:
            logger.error("Analyst role not found in config. Skipping requirements gathering.")
            return artifacts

        interactive_executor = InteractiveAgentExecutor(
            analyst_role,
            self.status_broadcaster,
            config.get('interactive_config')
        )

        questions = await interactive_executor.gather_requirements(project_brief, session_id)

        if not questions:
            logger.warning("No questions generated. Proceeding with original brief.")
            # Create a basic PSD from the brief if question generation fails
            psd_content = f"# Product Specification Document\n\n## Project Brief\n\n{project_brief}"
            artifacts["Product Spec Document (PSD)"] = psd_content
            return artifacts

        # Create interactive session and wait for real user answers
        interactive_session = await self.session_manager.create_session(
            session_id=session_id,
            questions=questions,
            agent_name="Analyst"
        )
        
        # Wait for user to answer all questions (with timeout handling)
        user_answers = await self.session_manager.wait_for_answers(session_id)
        
        # Clean up the session
        self.session_manager.cleanup_session(session_id)
        
        if not user_answers:
            logger.warning(f"No answers received for session {session_id}, proceeding with original brief only")
            # Create a basic PSD from just the brief
            psd_content = f"# Product Specification Document\n\n## Project Brief\n\n{project_brief}\n\n*Note: No additional requirements were provided.*"
            artifacts["Product Spec Document (PSD)"] = psd_content
            return artifacts

        # Generate PSD from brief, questions, and answers
        psd_context = f"Original Brief:\n{project_brief}\n\nQuestions Asked:\n"
        psd_context += "\n".join(f"- {q}" for q in questions)
        psd_context += "\n\nAnswers Provided:\n"
        psd_context += "\n".join(f"- {a}" for a in user_answers.values())

        # Use the regular task executor to generate the PSD
        psd_content = await interactive_executor.execute_task(psd_context, session_id)
        artifacts["Product Spec Document (PSD)"] = psd_content

        logger.info(f"Generated PSD for session '{session_id}'.")
        await self.status_broadcaster.broadcast_agent_response("Analyst", "Thank you. I have created the Product Specification Document.", session_id)

        return artifacts

    async def execute_stages(self, config: Dict[str, Any], session_id: str, artifacts: Dict[str, Any]):
        # This is a simplified linear execution for now.
        stage_order = ["Analyze", "Design", "Build", "Validate", "Launch"]

        for stage_name in stage_order:
            if stage_name not in config.get('stages', {}):
                continue

            stage_config = config['stages'][stage_name]
            logger.info(f"--- Entering Stage: {stage_name} ---")
            await self.status_broadcaster.broadcast_agent_response("System", f"Entering stage: {stage_name}", session_id)

            for task_config in stage_config.get('tasks', []):
                # Skip the requirements gathering task as we've already done it
                if stage_name == "Analyze" and task_config['role'] == "Analyst":
                    continue

                role_name = task_config['role']
                role_details = next((r for r in config['roles'] if r['name'] == role_name), None)
                if not role_details:
                    logger.error(f"Role '{role_name}' not found. Skipping task '{task_config['name']}'.")
                    continue

                agent_executor = InteractiveAgentExecutor(role_details, self.status_broadcaster, config.get('interactive_config'))

                input_artifacts = task_config.get('input_artifacts', [])
                context = "\n\n".join([f"--- {name} ---\n{artifacts.get(name, '')}" for name in input_artifacts])

                if not context.strip():
                    logger.warning(f"Task '{task_config['name']}' has no input context.")
                    continue

                result = await agent_executor.execute_task(context, session_id)

                output_artifact_name = task_config.get('output_artifacts', [None])[0]
                if output_artifact_name:
                    artifacts[output_artifact_name] = result
                    logger.info(f"  -> Produced artifact: '{output_artifact_name}'")
                    await self.status_broadcaster.broadcast_artifact_update({
                        "name": output_artifact_name,
                        "status": "completed",
                        "session_id": session_id,
                    })
