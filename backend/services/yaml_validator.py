"""
YAML Configuration Validation Service

Provides comprehensive validation for BotArmy process configuration files.
Addresses security recommendation: Add YAML schema validation before processing.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import yaml
import jsonschema
from jsonschema import ValidationError
import re

logger = logging.getLogger(__name__)

class YAMLValidationError(Exception):
    """Custom exception for YAML validation errors"""
    def __init__(self, message: str, details: Optional[List[str]] = None):
        super().__init__(message)
        self.details = details or []

class YAMLValidator:
    """
    Comprehensive YAML configuration validator with security and structure validation.
    
    Security Features:
    - File size limits
    - Content sanitization
    - Path traversal protection
    - Schema validation
    """
    
    MAX_FILE_SIZE = 1024 * 1024  # 1MB limit
    MAX_YAML_DEPTH = 10  # Prevent YAML bomb attacks
    
    def __init__(self):
        self.schema_path = Path(__file__).parent.parent / "schemas" / "process_config_schema.json"
        self.schema = self._load_schema()
        
    def _load_schema(self) -> Dict[str, Any]:
        """Load JSON schema for validation"""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Schema file not found: {self.schema_path}")
            raise YAMLValidationError(f"Validation schema not found: {self.schema_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON schema: {e}")
            raise YAMLValidationError(f"Invalid validation schema: {e}")
    
    def validate_file_upload(self, file_content: str, filename: str) -> Tuple[bool, List[str]]:
        """
        Validate uploaded YAML file content with comprehensive security checks.
        
        Args:
            file_content: Raw file content as string
            filename: Original filename for logging
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # 1. File size validation
        if len(file_content.encode('utf-8')) > self.MAX_FILE_SIZE:
            errors.append(f"File size exceeds limit of {self.MAX_FILE_SIZE} bytes")
        
        # 2. Filename validation
        if not self._is_safe_filename(filename):
            errors.append("Invalid filename: must be alphanumeric with .yaml/.yml extension")
        
        # 3. Content sanitization check
        if self._contains_suspicious_content(file_content):
            errors.append("File contains potentially malicious content")
        
        # 4. YAML parsing validation
        try:
            yaml_data = self._safe_yaml_load(file_content)
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML format: {str(e)}")
            return False, errors
        except YAMLValidationError as e:
            errors.extend(e.details)
            return False, errors
        
        # 5. Schema validation
        schema_errors = self._validate_schema(yaml_data)
        errors.extend(schema_errors)
        
        # 6. Business logic validation
        business_errors = self._validate_business_rules(yaml_data)
        errors.extend(business_errors)
        
        return len(errors) == 0, errors
    
    def validate_config_data(self, config_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate already parsed configuration data.
        
        Args:
            config_data: Parsed configuration dictionary
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Schema validation
        schema_errors = self._validate_schema(config_data)
        errors.extend(schema_errors)
        
        # Business logic validation
        business_errors = self._validate_business_rules(config_data)
        errors.extend(business_errors)
        
        return len(errors) == 0, errors
    
    def _is_safe_filename(self, filename: str) -> bool:
        """Check if filename is safe and follows naming conventions"""
        # Must end with .yaml or .yml
        if not filename.lower().endswith(('.yaml', '.yml')):
            return False
        
        # Must be alphanumeric with allowed characters
        base_name = Path(filename).stem
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_\-]*$'
        return bool(re.match(pattern, base_name)) and len(base_name) <= 50
    
    def _contains_suspicious_content(self, content: str) -> bool:
        """Check for potentially malicious content patterns"""
        suspicious_patterns = [
            # YAML exploits
            r'!!python/',  # Python object instantiation
            r'!!map:',     # Map merge exploit
            r'&.*\*.*',    # Complex anchor/alias patterns
            # Path traversal
            r'\.\./+',     # Directory traversal
            r'/etc/',      # System paths
            r'~/',         # Home directory
            # Script injection patterns
            r'<script',    # JavaScript
            r'javascript:', # JavaScript protocol
            r'eval\s*\(',  # Code evaluation
        ]
        
        content_lower = content.lower()
        for pattern in suspicious_patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                logger.warning(f"Suspicious content detected: {pattern}")
                return True
        
        return False
    
    def _safe_yaml_load(self, content: str) -> Dict[str, Any]:
        """Safely load YAML with security restrictions"""
        try:
            # Use safe_load to prevent arbitrary code execution
            data = yaml.safe_load(content)
            
            if not isinstance(data, dict):
                raise YAMLValidationError("YAML root must be an object/dictionary", 
                                        ["Root element must be a dictionary"])
            
            # Check nesting depth to prevent YAML bombs
            if self._get_max_depth(data) > self.MAX_YAML_DEPTH:
                raise YAMLValidationError("YAML structure too deeply nested",
                                        [f"Maximum depth of {self.MAX_YAML_DEPTH} exceeded"])
            
            return data
            
        except yaml.YAMLError as e:
            raise YAMLValidationError(f"YAML parsing error: {str(e)}")
    
    def _get_max_depth(self, obj, current_depth=0):
        """Calculate maximum nesting depth of dictionary/list structure"""
        if current_depth > self.MAX_YAML_DEPTH:
            return current_depth
        
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(self._get_max_depth(v, current_depth + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return current_depth
            return max(self._get_max_depth(item, current_depth + 1) for item in obj)
        else:
            return current_depth
    
    def _validate_schema(self, data: Dict[str, Any]) -> List[str]:
        """Validate data against JSON schema"""
        errors = []
        
        try:
            jsonschema.validate(instance=data, schema=self.schema)
        except ValidationError as e:
            # Parse validation errors into user-friendly messages
            path = " -> ".join(str(p) for p in e.path) if e.path else "root"
            errors.append(f"Schema validation error at '{path}': {e.message}")
            
            # Add context for specific validation failures
            if hasattr(e, 'context') and e.context:
                for context_error in e.context[:3]:  # Limit to first 3 sub-errors
                    context_path = " -> ".join(str(p) for p in context_error.path)
                    errors.append(f"  └─ {context_path}: {context_error.message}")
        
        return errors
    
    def _validate_business_rules(self, data: Dict[str, Any]) -> List[str]:
        """Validate business logic and cross-references"""
        errors = []
        
        try:
            # Extract key collections for cross-reference validation
            role_names = {role['name'] for role in data.get('roles', [])}
            artifact_names = {artifact['name'] for artifact in data.get('artifacts', [])}
            stage_names = set(data.get('stages', {}).keys())
            task_names = set()
            
            # Collect all task names
            for stage_name, stage in data.get('stages', {}).items():
                for task in stage.get('tasks', []):
                    task_names.add(task.get('name'))
            
            # Validate role references in stages
            for stage_name, stage in data.get('stages', {}).items():
                for task in stage.get('tasks', []):
                    role_name = task.get('role')
                    if role_name and role_name not in role_names:
                        errors.append(f"Stage '{stage_name}' task '{task.get('name')}' references undefined role '{role_name}'")
            
            # Validate artifact references
            for stage_name, stage in data.get('stages', {}).items():
                for task in stage.get('tasks', []):
                    # Check input artifacts
                    for artifact in task.get('input_artifacts', []):
                        if artifact not in artifact_names:
                            errors.append(f"Stage '{stage_name}' task '{task.get('name')}' references undefined input artifact '{artifact}'")
                    
                    # Check output artifacts
                    for artifact in task.get('output_artifacts', []):
                        if artifact not in artifact_names:
                            errors.append(f"Stage '{stage_name}' task '{task.get('name')}' references undefined output artifact '{artifact}'")
            
            # Validate task dependencies
            for stage_name, stage in data.get('stages', {}).items():
                for task in stage.get('tasks', []):
                    for dep_task in task.get('depends_on', []):
                        if dep_task not in task_names:
                            errors.append(f"Stage '{stage_name}' task '{task.get('name')}' depends on undefined task '{dep_task}'")
            
            # Validate stage involvement
            for role in data.get('roles', []):
                for stage_name in role.get('stage_involvement', []):
                    if stage_name not in stage_names:
                        errors.append(f"Role '{role.get('name')}' references undefined stage '{stage_name}'")
            
            # Validate path templates for security
            for artifact in data.get('artifacts', []):
                path_template = artifact.get('path_template', '')
                if not self._is_safe_path_template(path_template):
                    errors.append(f"Artifact '{artifact.get('name')}' has unsafe path template '{path_template}'")
        
        except Exception as e:
            logger.error(f"Business rule validation error: {e}")
            errors.append(f"Internal validation error: {str(e)}")
        
        return errors
    
    def _is_safe_path_template(self, path: str) -> bool:
        """Validate that path template is safe and doesn't allow traversal"""
        if not path:
            return False
        
        # Check for path traversal attempts
        if '..' in path or path.startswith('/') or '~' in path:
            return False
        
        # Must be relative path with safe characters
        safe_pattern = r'^[a-zA-Z0-9_\-/\.]+\.[a-zA-Z0-9]+$'
        return bool(re.match(safe_pattern, path))

# Global validator instance
_validator_instance = None

def get_yaml_validator() -> YAMLValidator:
    """Get singleton validator instance"""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = YAMLValidator()
    return _validator_instance