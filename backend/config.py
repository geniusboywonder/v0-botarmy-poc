"""
Backend configuration management with environment variable support.
Enhanced with interactive workflow and performance monitoring settings.
"""

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application configuration with enhanced settings"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    gemini_key_key: Optional[str] = None
    
    # API Settings
    api_title: str = "BotArmy Backend"
    api_version: str = "3.0.0"
    debug: bool = True
    
    # CORS Settings
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # WebSocket Settings
    websocket_heartbeat_interval: int = 30
    websocket_timeout: int = 60
    
    # Agent Settings
    max_agents: int = 6
    agent_timeout: int = 300
    
    # Interactive Workflow Settings
    interactive_timeout_minutes: int = 10
    max_questions_per_session: int = 5
    auto_proceed_on_timeout: bool = True
    
    # Performance Settings
    max_concurrent_workflows: int = 3
    workflow_result_cache_ttl: int = 3600
    
    # Error Handling Settings
    max_retry_attempts: int = 3
    retry_backoff_seconds: int = 2
    
    # Environment Settings
    replit: Optional[str] = None
    
    # Safety and Testing Settings
    agent_test_mode: bool = False
    role_test_mode: bool = False
    test_mode: bool = False
    enable_hitl: bool = True
    auto_action: str = "none"
    
    # URL Settings
    backend_url: Optional[str] = None
    next_public_backend_url: Optional[str] = None
    websocket_url: Optional[str] = None
    next_public_websocket_url: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from .env file

@dataclass
class AgentConfig:
    """Agent-specific configuration."""
    name: str
    status: str = "configured"
    description: str = ""
    role: str = ""
    timeout: Optional[int] = None
    max_retries: int = 3
    config: Dict[str, Any] = field(default_factory=dict)

# Global settings instance
settings = Settings()

def get_agent_configurations() -> List[Dict[str, Any]]:
    """Get default agent configurations."""
    return [
        {
            "name": "Analyst",
            "status": "configured",
            "description": "Requirements analysis agent",
            "role": "analyst",
            "timeout": settings.agent_timeout,
            "config": {
                "specialization": "requirements_gathering",
                "max_questions": settings.max_questions_per_session
            }
        },
        {
            "name": "Architect",
            "status": "configured", 
            "description": "System design agent",
            "role": "architect",
            "timeout": settings.agent_timeout,
            "config": {
                "specialization": "system_design",
                "include_diagrams": True
            }
        },
        {
            "name": "Developer",
            "status": "configured",
            "description": "Code generation agent", 
            "role": "developer",
            "timeout": settings.agent_timeout * 2,
            "config": {
                "specialization": "code_generation",
                "include_tests": True
            }
        },
        {
            "name": "Tester",
            "status": "configured",
            "description": "Quality assurance agent",
            "role": "tester", 
            "timeout": settings.agent_timeout,
            "config": {
                "specialization": "quality_assurance",
                "test_types": ["unit", "integration", "e2e"]
            }
        },
        {
            "name": "Deployer",
            "status": "configured",
            "description": "Deployment management agent",
            "role": "deployer",
            "timeout": settings.agent_timeout,
            "config": {
                "specialization": "deployment",
                "platforms": ["docker", "kubernetes", "serverless"]
            }
        },
        {
            "name": "Monitor", 
            "status": "configured",
            "description": "System monitoring agent",
            "role": "monitor",
            "timeout": settings.agent_timeout // 2,
            "config": {
                "specialization": "monitoring",
                "metrics_enabled": True
            }
        }
    ]

def get_environment_info() -> Dict[str, Any]:
    """Get environment configuration info."""
    return {
        "is_replit": "REPL_OWNER" in os.environ,
        "test_mode": os.getenv("TEST_MODE", "false").lower() == "true",
        "agent_test_mode": os.getenv("AGENT_TEST_MODE", "false").lower() == "true", 
        "hitl_enabled": os.getenv("ENABLE_HITL", "true").lower() == "true",
        "database_available": bool(os.getenv("DATABASE_URL")),
        "redis_available": bool(os.getenv("REDIS_URL"))
    }
