"""
Interactive Session Manager for handling real-time user questions and answers.
Manages the flow between agents asking questions and waiting for user responses.
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import uuid

from backend.config import settings

logger = logging.getLogger(__name__)

@dataclass
class InteractiveQuestion:
    """Represents a question in an interactive session."""
    id: str
    text: str
    agent_name: str
    session_id: str
    created_at: datetime
    required: bool = True
    
@dataclass 
class InteractiveSession:
    """Represents an interactive session with questions and answers."""
    session_id: str
    questions: List[InteractiveQuestion]
    answers: Dict[str, str]
    created_at: datetime
    timeout_at: datetime
    status: str = "active"  # active, completed, timeout, cancelled
    current_question_index: int = 0

class InteractiveSessionManager:
    """
    Manages interactive sessions for collecting user answers to agent questions.
    Handles timeouts, question ordering, and answer validation.
    """
    
    def __init__(self, status_broadcaster, config=None):
        self.status_broadcaster = status_broadcaster
        self.config = config or settings
        self.active_sessions: Dict[str, InteractiveSession] = {}
        self.answer_waiters: Dict[str, asyncio.Event] = {}
        self.session_callbacks: Dict[str, Callable] = {}
        
    async def create_session(self, session_id: str, questions: List[str], 
                           agent_name: str, timeout_minutes: Optional[int] = None) -> InteractiveSession:
        """Create a new interactive session with questions."""
        timeout_minutes = timeout_minutes or self.config.interactive_timeout_minutes
        timeout_at = datetime.now() + timedelta(minutes=timeout_minutes)
        
        # Convert string questions to InteractiveQuestion objects
        question_objects = [
            InteractiveQuestion(
                id=str(uuid.uuid4()),
                text=q,
                agent_name=agent_name,
                session_id=session_id,
                created_at=datetime.now()
            )
            for q in questions
        ]
        
        session = InteractiveSession(
            session_id=session_id,
            questions=question_objects,
            answers={},
            created_at=datetime.now(),
            timeout_at=timeout_at,
            status="active"
        )
        
        self.active_sessions[session_id] = session
        self.answer_waiters[session_id] = asyncio.Event()
        
        logger.info(f"Created interactive session {session_id} with {len(questions)} questions, timeout at {timeout_at}")
        
        # Send questions to UI
        await self._send_questions_to_ui(session)
        
        return session
    
    async def _send_questions_to_ui(self, session: InteractiveSession):
        """Send questions to the UI through the status broadcaster."""
        questions_payload = []
        for q in session.questions:
            questions_payload.append({
                "id": q.id,
                "text": q.text,
                "required": q.required
            })
        
        payload = {
            "type": "interactive_questions",
            "questions": questions_payload,
            "session_id": session.session_id,
            "timeout_minutes": self.config.interactive_timeout_minutes,
            "agent_name": session.questions[0].agent_name if session.questions else "System"
        }
        
        await self.status_broadcaster.broadcast_agent_response(
            session.questions[0].agent_name if session.questions else "System",
            f"I need to ask you {len(session.questions)} questions to better understand your requirements:",
            session.session_id,
            payload=payload
        )
    
    async def submit_answer(self, session_id: str, question_id: str, answer: str) -> bool:
        """Submit an answer for a question in the session."""
        session = self.active_sessions.get(session_id)
        if not session:
            logger.error(f"Session {session_id} not found")
            return False
        
        if session.status != "active":
            logger.error(f"Session {session_id} is not active (status: {session.status})")
            return False
        
        # Find the question
        question = next((q for q in session.questions if q.id == question_id), None)
        if not question:
            logger.error(f"Question {question_id} not found in session {session_id}")
            return False
        
        # Store the answer
        session.answers[question_id] = answer.strip()
        logger.info(f"Answer submitted for question {question_id} in session {session_id}")
        
        # Check if all questions are answered
        answered_count = len(session.answers)
        total_questions = len(session.questions)
        
        # Send progress update
        await self.status_broadcaster.broadcast_agent_response(
            question.agent_name,
            f"Thank you! ({answered_count}/{total_questions} questions answered)",
            session_id
        )
        
        if answered_count >= total_questions:
            # All questions answered
            session.status = "completed"
            await self.status_broadcaster.broadcast_agent_response(
                question.agent_name,
                "All questions answered. Proceeding with analysis...",
                session_id
            )
            
            # Signal waiters that answers are ready
            if session_id in self.answer_waiters:
                self.answer_waiters[session_id].set()
        
        return True
    
    async def wait_for_answers(self, session_id: str) -> Optional[Dict[str, str]]:
        """
        Wait for all answers to be submitted or timeout to occur.
        Returns the answers dict or None if timeout/cancelled.
        """
        session = self.active_sessions.get(session_id)
        if not session:
            logger.error(f"Session {session_id} not found")
            return None
        
        waiter = self.answer_waiters.get(session_id)
        if not waiter:
            logger.error(f"No waiter found for session {session_id}")
            return None
        
        # Calculate remaining timeout
        now = datetime.now()
        if now >= session.timeout_at:
            logger.warning(f"Session {session_id} already timed out")
            return await self._handle_timeout(session_id)
        
        timeout_seconds = (session.timeout_at - now).total_seconds()
        
        try:
            # Wait for either all answers or timeout
            await asyncio.wait_for(waiter.wait(), timeout=timeout_seconds)
            
            # Return the answers
            return self._get_answers_as_dict(session)
            
        except asyncio.TimeoutError:
            logger.warning(f"Session {session_id} timed out waiting for answers")
            return await self._handle_timeout(session_id)
    
    async def _handle_timeout(self, session_id: str) -> Optional[Dict[str, str]]:
        """Handle session timeout."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        session.status = "timeout"
        
        answered_count = len(session.answers)
        total_questions = len(session.questions)
        
        if self.config.auto_proceed_on_timeout and answered_count > 0:
            # Use partial answers
            await self.status_broadcaster.broadcast_agent_response(
                "System",
                f"⏰ Timeout reached. Proceeding with {answered_count}/{total_questions} answers provided.",
                session_id
            )
            return self._get_answers_as_dict(session)
        else:
            # Cancel the session
            await self.status_broadcaster.broadcast_agent_response(
                "System",
                f"⏰ Session timed out. {answered_count}/{total_questions} questions were answered.",
                session_id
            )
            return None
    
    def _get_answers_as_dict(self, session: InteractiveSession) -> Dict[str, str]:
        """Convert question ID -> answer mapping to question text -> answer mapping."""
        result = {}
        for question in session.questions:
            answer = session.answers.get(question.id, "")
            if answer:
                result[question.text] = answer
        return result
    
    async def cancel_session(self, session_id: str) -> bool:
        """Cancel an active session."""
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        session.status = "cancelled"
        
        # Signal any waiters
        if session_id in self.answer_waiters:
            self.answer_waiters[session_id].set()
        
        await self.status_broadcaster.broadcast_agent_response(
            "System",
            "Interactive session cancelled.",
            session_id
        )
        
        logger.info(f"Session {session_id} cancelled")
        return True
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status of a session."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        return {
            "session_id": session_id,
            "status": session.status,
            "questions_total": len(session.questions),
            "questions_answered": len(session.answers),
            "created_at": session.created_at.isoformat(),
            "timeout_at": session.timeout_at.isoformat(),
            "time_remaining_seconds": max(0, (session.timeout_at - datetime.now()).total_seconds())
        }
    
    def cleanup_session(self, session_id: str):
        """Clean up session data."""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        if session_id in self.answer_waiters:
            del self.answer_waiters[session_id]
        if session_id in self.session_callbacks:
            del self.session_callbacks[session_id]
        
        logger.info(f"Cleaned up session {session_id}")
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get list of all active sessions."""
        return [self.get_session_status(sid) for sid in self.active_sessions.keys()]