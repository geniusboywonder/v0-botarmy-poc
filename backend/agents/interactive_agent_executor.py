import logging
from typing import Dict, Any, List

from backend.agents.generic_agent_executor import GenericAgentExecutor, InputSanitizer

logger = logging.getLogger(__name__)

class InteractiveAgentExecutor(GenericAgentExecutor):
    """
    Extends GenericAgentExecutor with capabilities for interactive workflows,
    such as requirements gathering.
    """

    def __init__(self, role_config: Dict[str, Any], status_broadcaster=None, interactive_config: Dict[str, Any] = None):
        super().__init__(role_config, status_broadcaster)
        self.interactive_config = interactive_config or {}

    async def gather_requirements(self, project_brief: str, session_id: str) -> List[str]:
        """
        Analyzes a project brief and generates clarifying questions.

        Args:
            project_brief (str): The initial high-level project description.
            session_id (str): The session ID for broadcasting status updates.

        Returns:
            A list of clarifying questions.
        """
        logger.info(f"[{self.agent_name}] Starting requirements gathering for session '{session_id}'.")

        # Sanitize the input brief
        try:
            sanitized_brief = InputSanitizer.sanitize_context(project_brief)
        except ValueError as e:
            logger.warning(f"Project brief validation failed: {e}")
            await self.status_broadcaster.broadcast_agent_response(
                agent_name=self.agent_name,
                content=f"⚠️ Input validation failed: {e}",
                session_id=session_id
            )
            return []

        # Construct a specialized prompt for generating questions
        max_questions = self.interactive_config.get('requirements_gathering', {}).get('max_questions', 5)

        prompt = f"""
You are an expert business analyst. Your task is to analyze the following project brief and identify key areas where more information is needed. Based on your analysis, generate exactly {max_questions} critical and insightful questions to clarify the project's requirements, scope, and objectives.

Return ONLY a JSON array of strings, where each string is a single question. Do not include any other text, explanation, or formatting.

Example format:
[
    "What is the primary goal of this project?",
    "Who are the target users for this application?"
]

Project Brief:
"{sanitized_brief}"
"""

        if self.status_broadcaster:
            await self.status_broadcaster.broadcast_agent_progress(self.agent_name, "Generating questions", 1, 2, session_id)

        try:
            response = await self.llm_service.generate_response(
                prompt=prompt,
                agent_name=self.agent_name,
                response_format={"type": "json_object"}
            )

            # The LLM should return a JSON string representing a list of questions.
            import json
            questions = json.loads(response)

            if not isinstance(questions, list) or not all(isinstance(q, str) for q in questions):
                raise ValueError("LLM response is not a valid list of strings.")

            logger.info(f"[{self.agent_name}] Successfully generated {len(questions)} questions.")
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(self.agent_name, "Questions generated", 2, 2, session_id)

            return questions

        except Exception as e:
            logger.error(f"[{self.agent_name}] Failed to generate requirements questions: {e}")
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_response(
                    agent_name=self.agent_name,
                    content=f"Error during requirements gathering: {e}",
                    session_id=session_id
                )
            return []

    async def scaffold_artifacts(self, artifact_configs: list, session_id: str):
        """
        Creates placeholder artifacts in the database.
        (This is a placeholder for now, will be implemented later)
        """
        logger.info(f"[{self.agent_name}] Scaffolding {len(artifact_configs)} artifacts for session '{session_id}'.")
        # In a real implementation, this would interact with the database
        # to create entries in the 'artifacts_scaffolded' table.
        if self.status_broadcaster:
            for artifact in artifact_configs:
                await self.status_broadcaster.broadcast_artifact_update({
                    "name": artifact.get("name"),
                    "status": "scaffolded",
                    "session_id": session_id,
                })
        await asyncio.sleep(1) # Simulate DB work
        return True
