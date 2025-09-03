import os
import yaml
import logging
import collections.abc

from backend.services.process_config_loader import ProcessConfigLoader

logger = logging.getLogger(__name__)

def deep_merge(d, u):
    """
    Recursively merge dictionaries.
    'u' values overwrite 'd' values.
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = deep_merge(d.get(k, {}), v)
        else:
            d[k] = v
    return d

class EnhancedProcessConfigLoader(ProcessConfigLoader):
    """
    Extends ProcessConfigLoader to support template and role inheritance.
    """
    def __init__(self,
                 config_dir="backend/configs/processes",
                 schema_path="backend/schemas/process_schema.json",
                 template_dir="backend/configs/templates",
                 role_profile_dir="backend/configs/role_profiles"):
        super().__init__(config_dir, schema_path)
        self.template_dir = template_dir
        self.role_profile_dir = role_profile_dir
        self._template_cache = {}
        self._role_profile_cache = {}

    def _load_yaml(self, file_path: str):
        """Helper to load a single YAML file."""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)

    def _get_template(self, template_name: str):
        """Loads a template from the template directory, with caching."""
        if template_name in self._template_cache:
            return self._template_cache[template_name]

        template_path = os.path.join(self.template_dir, f"{template_name}.yaml")
        template_data = self._load_yaml(template_path)
        # Recursively load parent templates
        if 'extends' in template_data and template_data['extends']:
            parent_template = self._get_template(template_data['extends'])
            template_data = deep_merge(parent_template.copy(), template_data)

        self._template_cache[template_name] = template_data
        return template_data

    def _get_role_profile(self, profile_name: str):
        """Loads a role profile from the role profile directory, with caching."""
        if profile_name in self._role_profile_cache:
            return self._role_profile_cache[profile_name]

        profile_path = os.path.join(self.role_profile_dir, f"{profile_name}.yaml")
        profile_data = self._load_yaml(profile_path)
        self._role_profile_cache[profile_name] = profile_data
        return profile_data

    def get_config(self, config_name: str, force_reload: bool = False):
        """
        Overrides the base get_config to implement inheritance.
        """
        if not force_reload and config_name in self._cache:
            logger.debug(f"Returning cached configuration for '{config_name}'")
            return self._cache[config_name]

        # Load the base config using the parent method, but without validation yet
        # as it might be incomplete before inheritance.
        # Temporarily disable schema validation in the parent.
        original_schema = self._schema
        self._schema = None
        try:
            config = super().get_config(config_name, force_reload=True) # force reload to bypass parent cache
        finally:
            self._schema = original_schema # Restore schema

        # 1. Process template inheritance
        if 'extends' in config and config['extends']:
            template = self._get_template(config['extends'])
            config = deep_merge(template.copy(), config)

        # 2. Process role inheritance
        if 'roles' in config:
            processed_roles = []
            for role in config['roles']:
                if 'extends' in role and role['extends']:
                    profile = self._get_role_profile(role['extends'])
                    processed_role = deep_merge(profile.copy(), role)
                    processed_roles.append(processed_role)
                else:
                    processed_roles.append(role)
            config['roles'] = processed_roles

        # 3. Validate the final, merged config
        if self._schema:
            from jsonschema import validate, ValidationError
            try:
                validate(instance=config, schema=self._schema)
                logger.info(f"Merged configuration '{config_name}' successfully validated.")
            except ValidationError as e:
                logger.error(f"Validation error for merged config '{config_name}': {e.message}")
                raise

        self._cache[config_name] = config
        return config

# Singleton instance
enhanced_process_config_loader = None

def get_enhanced_process_config_loader():
    """
    Returns the singleton instance of the EnhancedProcessConfigLoader.
    """
    global enhanced_process_config_loader
    if enhanced_process_config_loader is None:
        enhanced_process_config_loader = EnhancedProcessConfigLoader()
    return enhanced_process_config_loader
