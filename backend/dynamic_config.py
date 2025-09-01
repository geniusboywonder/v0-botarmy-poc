"""
Dynamic configuration service that reads .env file at runtime.

This service provides dynamic access to environment variables that can be changed
via the settings page without requiring a backend restart.
"""

import os
import logging
from typing import Any, Dict, Optional
from threading import Lock

logger = logging.getLogger(__name__)

class DynamicConfig:
    """
    Centralized configuration service that reads .env file dynamically.
    
    This allows environment variables to be updated through the settings page
    and immediately take effect without requiring a restart.
    """
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self._cache = {}
        self._cache_lock = Lock()
        self._last_modified = 0
        
    def _parse_env_file(self) -> Dict[str, str]:
        """Parse .env file and return key-value pairs."""
        env_vars = {}
        
        if not os.path.exists(self.env_file):
            logger.warning(f"Environment file {self.env_file} not found")
            return env_vars
            
        try:
            with open(self.env_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key=value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        env_vars[key] = value
                        
        except Exception as e:
            logger.error(f"Error parsing {self.env_file}: {e}")
            
        return env_vars
    
    def _refresh_cache_if_needed(self):
        """Refresh cache if .env file has been modified."""
        try:
            current_modified = os.path.getmtime(self.env_file)
            if current_modified > self._last_modified:
                with self._cache_lock:
                    self._cache = self._parse_env_file()
                    self._last_modified = current_modified
                    logger.info("Configuration cache refreshed from .env file")
        except Exception as e:
            logger.error(f"Error checking .env file modification time: {e}")
    
    def get(self, key: str, default: Any = None, var_type: str = "string") -> Any:
        """
        Get environment variable with type conversion and dynamic refresh.
        
        Args:
            key: Environment variable key
            default: Default value if key not found
            var_type: Type to convert to ("string", "boolean", "integer", "float")
        
        Returns:
            Environment variable value with appropriate type conversion
        """
        # First try to get from actual environment (for non-.env vars)
        env_value = os.getenv(key)
        if env_value is not None:
            return self._convert_type(env_value, var_type, default)
        
        # Then check .env file cache
        self._refresh_cache_if_needed()
        
        with self._cache_lock:
            value = self._cache.get(key, default)
        
        if value is not None:
            return self._convert_type(str(value), var_type, default)
        
        return default
    
    def _convert_type(self, value: str, var_type: str, default: Any) -> Any:
        """Convert string value to specified type."""
        try:
            if var_type == "boolean":
                return value.lower() in ("true", "yes", "1", "on")
            elif var_type == "integer":
                return int(value)
            elif var_type == "float":
                return float(value)
            else:  # string
                return value
        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to convert {value} to {var_type}, using default {default}: {e}")
            return default
    
    def get_all_env_vars(self) -> Dict[str, str]:
        """Get all environment variables from .env file."""
        self._refresh_cache_if_needed()
        with self._cache_lock:
            return self._cache.copy()
    
    def is_test_mode(self) -> bool:
        """Check if any test mode is enabled."""
        return (self.get("AGENT_TEST_MODE", False, "boolean") or 
                self.get("TEST_MODE", False, "boolean") or
                self.get("ROLE_TEST_MODE", False, "boolean"))
    
    def is_agent_test_mode(self) -> bool:
        """Check if agent test mode is enabled."""
        return self.get("AGENT_TEST_MODE", False, "boolean")
    
    def is_role_test_mode(self) -> bool:
        """Check if role test mode is enabled."""
        return self.get("ROLE_TEST_MODE", False, "boolean")
    
    def is_hitl_enabled(self) -> bool:
        """Check if Human-in-the-Loop is enabled."""
        return self.get("ENABLE_HITL", True, "boolean")
    
    def get_auto_action(self) -> str:
        """Get auto action setting."""
        return self.get("AUTO_ACTION", "none", "string")
    
    def force_refresh(self):
        """Force refresh of configuration cache."""
        with self._cache_lock:
            self._last_modified = 0
        self._refresh_cache_if_needed()
        logger.info("Configuration cache force refreshed")


# Global singleton instance
_dynamic_config = None
_config_lock = Lock()

def get_dynamic_config() -> DynamicConfig:
    """Get the singleton DynamicConfig instance."""
    global _dynamic_config
    if _dynamic_config is None:
        with _config_lock:
            if _dynamic_config is None:
                _dynamic_config = DynamicConfig()
    return _dynamic_config

def refresh_config():
    """Force refresh the global configuration."""
    config = get_dynamic_config()
    config.force_refresh()