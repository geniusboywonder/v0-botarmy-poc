from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application configuration"""
    
    # API Settings
    api_title: str = "BotArmy Backend"
    api_version: str = "1.0.0"
    debug: bool = True
    
    # CORS Settings
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # WebSocket Settings
    websocket_heartbeat_interval: int = 30
    websocket_timeout: int = 60
    
    # Agent Settings
    max_agents: int = 6
    agent_timeout: int = 300
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
