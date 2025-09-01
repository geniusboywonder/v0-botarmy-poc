"""
Workflow orchestration modules for BotArmy.

This package contains both the original SDLC workflow and the new generic process engine.
"""

from .generic_orchestrator import generic_workflow

__all__ = ["generic_workflow"]