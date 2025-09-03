import pytest
import yaml
import os
from backend.services.enhanced_process_config_loader import EnhancedProcessConfigLoader

@pytest.fixture
def config_loader_fixture(tmp_path):
    """Fixture to create a temporary config structure for testing."""
    # Create directories
    processes_dir = tmp_path / "processes"
    processes_dir.mkdir()
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    role_profiles_dir = tmp_path / "role_profiles"
    role_profiles_dir.mkdir()

    # Create base template
    base_template_content = {
        "template_name": "base_interactive",
        "default_interactive_config": {
            "requirements_gathering": {"enabled": True, "max_questions": 5},
            "hitl_checkpoints": []
        }
    }
    with open(templates_dir / "base_interactive.yaml", "w") as f:
        yaml.dump(base_template_content, f)

    # Create role profile
    role_profile_content = {
        "profile_name": "strategic_analyst",
        "description": "This is a base analyst profile.",
        "question_patterns": ["What is the primary objective?"]
    }
    with open(role_profiles_dir / "strategic_analyst.yaml", "w") as f:
        yaml.dump(role_profile_content, f)

    # Create a child process config that extends the base template and role
    child_process_content = {
        "process_name": "child_process",
        "extends": "base_interactive",
        "interactive_config": {
            "requirements_gathering": {"max_questions": 10} # Override
        },
        "roles": [
            {
                "name": "Analyst",
                "extends": "strategic_analyst",
                "description": "This is a specific analyst." # Override
            }
        ],
        "artifacts": [],
        "stages": {}
    }
    with open(processes_dir / "child_process.yaml", "w") as f:
        yaml.dump(child_process_content, f)

    # Create a dummy schema file
    schema_content = {"type": "object", "properties": {"process_name": {"type": "string"}}}
    schema_path = tmp_path / "schema.json"
    with open(schema_path, "w") as f:
        import json
        json.dump(schema_content, f)


    loader = EnhancedProcessConfigLoader(
        config_dir=str(processes_dir),
        template_dir=str(templates_dir),
        role_profile_dir=str(role_profiles_dir),
        schema_path=str(schema_path) # Use dummy schema for this test
    )
    # Disable validation for this unit test since we are not testing the full schema
    loader._schema = None
    return loader

def test_config_inheritance(config_loader_fixture):
    """Test that process configuration correctly inherits from a base template."""
    loader = config_loader_fixture
    config = loader.get_config("child_process")

    # Test template inheritance and merge
    assert config["process_name"] == "child_process"
    assert config["default_interactive_config"]["requirements_gathering"]["enabled"] is True # Inherited
    assert config["default_interactive_config"]["requirements_gathering"]["max_questions"] == 5 # from template, not overridden
    assert config["interactive_config"]["requirements_gathering"]["max_questions"] == 10 # from child, override

    # Test role profile inheritance and merge
    analyst_role = config["roles"][0]
    assert analyst_role["name"] == "Analyst"
    assert analyst_role["description"] == "This is a specific analyst." # Overridden
    assert analyst_role["question_patterns"] == ["What is the primary objective?"] # Inherited
