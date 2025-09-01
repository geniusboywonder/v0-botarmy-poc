import os
import yaml
import json
import logging
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

class ProcessConfigLoader:
    """
    Service to load, validate, and manage process configurations from YAML files.
    """
    def __init__(self, config_dir="backend/configs/processes", schema_path="backend/schemas/process_schema.json"):
        self.config_dir = config_dir
        self.schema_path = schema_path
        self._schema = self._load_schema()
        self._cache = {}

    def _load_schema(self):
        """Loads the JSON schema for process configurations."""
        try:
            with open(self.schema_path, 'r') as f:
                schema = json.load(f)
            logger.info(f"Successfully loaded process schema from {self.schema_path}")
            return schema
        except FileNotFoundError:
            logger.error(f"Schema file not found at {self.schema_path}. Process validation will be skipped.")
            return None
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {self.schema_path}. Process validation will be skipped.")
            return None

    def list_configs(self):
        """Returns a list of available process configuration files (without extension)."""
        if not os.path.isdir(self.config_dir):
            return []
        return [f.replace('.yaml', '').replace('.yml', '') for f in os.listdir(self.config_dir) if f.endswith(('.yaml', '.yml'))]

    def get_config(self, config_name: str, force_reload: bool = False):
        """
        Loads, validates, and returns a process configuration.
        Uses a cache to avoid redundant loads.
        """
        if not force_reload and config_name in self._cache:
            logger.debug(f"Returning cached configuration for '{config_name}'")
            return self._cache[config_name]

        config_path_yaml = os.path.join(self.config_dir, f"{config_name}.yaml")
        config_path_yml = os.path.join(self.config_dir, f"{config_name}.yml")

        if os.path.exists(config_path_yaml):
            config_path = config_path_yaml
        elif os.path.exists(config_path_yml):
            config_path = config_path_yml
        else:
            logger.error(f"Configuration file for '{config_name}' not found.")
            raise FileNotFoundError(f"Configuration file for '{config_name}' not found.")

        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file {config_path}: {e}")
            raise

        if self._schema:
            try:
                validate(instance=config_data, schema=self._schema)
                logger.info(f"Configuration '{config_name}' successfully validated against the schema.")
            except ValidationError as e:
                logger.error(f"Validation error for configuration '{config_name}': {e.message}")
                raise

        self._cache[config_name] = config_data
        return config_data

# Singleton instance
process_config_loader = None

def get_process_config_loader():
    """
    Returns the singleton instance of the ProcessConfigLoader.
    """
    global process_config_loader
    if process_config_loader is None:
        process_config_loader = ProcessConfigLoader()
    return process_config_loader
