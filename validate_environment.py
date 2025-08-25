#!/usr/bin/env python3
"""
Environment Configuration Validation Script
Validates all required environment variables and configurations for BotArmy
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
load_dotenv('.env.local')  # Also load local overrides

class EnvironmentValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
    def log_error(self, message):
        self.errors.append(f"❌ ERROR: {message}")
        
    def log_warning(self, message):
        self.warnings.append(f"⚠️  WARNING: {message}")
        
    def log_info(self, message):
        self.info.append(f"ℹ️  INFO: {message}")
        
    def log_success(self, message):
        self.info.append(f"✅ SUCCESS: {message}")

    def validate_api_keys(self):
        """Validate API keys for LLM providers"""
        print("🔑 Validating API Keys...")
        
        # OpenAI API Key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            self.log_error("OPENAI_API_KEY is missing")
        elif not openai_key.startswith('sk-'):
            self.log_error("OPENAI_API_KEY appears to be invalid (should start with 'sk-')")
        elif len(openai_key) < 50:
            self.log_error("OPENAI_API_KEY appears to be too short")
        else:
            self.log_success(f"OPENAI_API_KEY is present and properly formatted (length: {len(openai_key)})")
            
        # Gemini API Key  
        gemini_key = os.getenv('GEMINI_KEY_KEY')  # Note: It's GEMINI_KEY_KEY in the env file
        if not gemini_key:
            self.log_warning("GEMINI_KEY_KEY is missing (optional but recommended)")
        elif not gemini_key.startswith('AIza'):
            self.log_warning("GEMINI_KEY_KEY appears to be invalid (should start with 'AIza')")
        else:
            self.log_success(f"GEMINI_KEY_KEY is present and properly formatted (length: {len(gemini_key)})")

    def validate_backend_config(self):
        """Validate backend configuration"""
        print("🔧 Validating Backend Configuration...")
        
        backend_host = os.getenv('BACKEND_HOST', 'localhost')
        backend_port = os.getenv('BACKEND_PORT', '8000')
        backend_url = os.getenv('BACKEND_URL', f'http://{backend_host}:{backend_port}')
        
        self.log_success(f"Backend Host: {backend_host}")
        self.log_success(f"Backend Port: {backend_port}")
        self.log_success(f"Backend URL: {backend_url}")
        
        # Validate port is numeric
        try:
            port_num = int(backend_port)
            if port_num < 1024 or port_num > 65535:
                self.log_warning(f"Backend port {port_num} is unusual (should be 1024-65535)")
        except ValueError:
            self.log_error(f"Backend port '{backend_port}' is not numeric")

    def validate_websocket_config(self):
        """Validate WebSocket configuration"""
        print("🌐 Validating WebSocket Configuration...")
        
        # Check main WebSocket URL
        websocket_url = os.getenv('WEBSOCKET_URL', 'ws://localhost:8000/ws')
        self.log_success(f"WebSocket URL: {websocket_url}")
        
        # Check frontend WebSocket URL
        frontend_ws_url = os.getenv('NEXT_PUBLIC_WEBSOCKET_URL')
        if not frontend_ws_url:
            self.log_error("NEXT_PUBLIC_WEBSOCKET_URL is missing")
        else:
            self.log_success(f"Frontend WebSocket URL: {frontend_ws_url}")
            
        # Check for inconsistencies
        if websocket_url and frontend_ws_url:
            # Remove /api prefix if present in frontend URL
            normalized_frontend = frontend_ws_url.replace('/api/ws', '/ws')
            if websocket_url != normalized_frontend:
                self.log_warning(f"WebSocket URLs might be inconsistent:")
                self.log_warning(f"  Backend: {websocket_url}")
                self.log_warning(f"  Frontend: {frontend_ws_url}")

    def validate_frontend_config(self):
        """Validate frontend configuration"""
        print("🖥️  Validating Frontend Configuration...")
        
        backend_url = os.getenv('NEXT_PUBLIC_BACKEND_URL')
        if not backend_url:
            self.log_error("NEXT_PUBLIC_BACKEND_URL is missing")
        else:
            self.log_success(f"Frontend Backend URL: {backend_url}")
            
        # Check consistency with backend config
        expected_url = os.getenv('BACKEND_URL', 'http://localhost:8000')
        if backend_url != expected_url:
            self.log_warning(f"Frontend and backend URLs might be inconsistent:")
            self.log_warning(f"  BACKEND_URL: {expected_url}")
            self.log_warning(f"  NEXT_PUBLIC_BACKEND_URL: {backend_url}")

    def validate_safety_config(self):
        """Validate safety brake configuration"""
        print("🛡️  Validating Safety Brake Configuration...")
        
        test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
        agent_test_mode = os.getenv('AGENT_TEST_MODE', 'false').lower() == 'true'
        enable_hitl = os.getenv('ENABLE_HITL', 'false').lower() == 'true'
        auto_action = os.getenv('AUTO_ACTION', 'none')
        
        if test_mode:
            self.log_success("TEST_MODE is enabled (safe for testing)")
        else:
            self.log_warning("TEST_MODE is disabled (will consume LLM tokens/costs)")
            
        if agent_test_mode:
            self.log_success("AGENT_TEST_MODE is enabled (agents return mock responses)")
        else:
            self.log_warning("AGENT_TEST_MODE is disabled (agents will make real LLM calls)")
            
        if enable_hitl:
            self.log_success("ENABLE_HITL is enabled (human-in-the-loop active)")
        else:
            self.log_warning("ENABLE_HITL is disabled (no human approval gates)")
            
        self.log_info(f"AUTO_ACTION setting: {auto_action}")
        
        # Safety recommendation
        if test_mode and agent_test_mode:
            self.log_success("🛡️ SAFETY BRAKES FULLY ENGAGED - Safe for testing")
        else:
            self.log_warning("🚨 SAFETY BRAKES NOT FULLY ENGAGED - May consume resources")

    def validate_development_config(self):
        """Validate development configuration"""
        print("🔧 Validating Development Configuration...")
        
        debug = os.getenv('DEBUG', 'false').lower() == 'true'
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        if debug:
            self.log_success("DEBUG mode is enabled (verbose logging)")
        else:
            self.log_info("DEBUG mode is disabled (production logging)")
            
        self.log_info(f"Log level: {log_level}")
        
        # Agent configuration
        max_agents = os.getenv('MAX_AGENTS', '6')
        agent_timeout = os.getenv('AGENT_TIMEOUT', '300')
        llm_rate_limit_delay = os.getenv('LLM_RATE_LIMIT_DELAY', '2')
        
        self.log_info(f"Max agents: {max_agents}")
        self.log_info(f"Agent timeout: {agent_timeout} seconds")
        self.log_info(f"LLM rate limit delay: {llm_rate_limit_delay} seconds")

    def validate_file_structure(self):
        """Validate key files exist"""
        print("📁 Validating File Structure...")
        
        key_files = [
            ('backend/main.py', 'Backend server'),
            ('app/page.tsx', 'Frontend main page'),
            ('lib/websocket/websocket-service.ts', 'WebSocket service'),
            ('lib/stores/agent-store.ts', 'Agent store'),
            ('package.json', 'Node.js dependencies'),
            ('requirements.txt', 'Python dependencies')
        ]
        
        for file_path, description in key_files:
            if Path(file_path).exists():
                self.log_success(f"{description}: {file_path}")
            else:
                self.log_error(f"Missing {description}: {file_path}")

    def validate_dependencies(self):
        """Check if key dependencies are available"""
        print("📦 Validating Dependencies...")
        
        # Check package.json
        try:
            with open('package.json', 'r') as f:
                package_data = json.load(f)
                deps = package_data.get('dependencies', {})
                
                key_frontend_deps = [
                    'next', 'react', 'zustand', 'lucide-react'
                ]
                
                for dep in key_frontend_deps:
                    if dep in deps:
                        self.log_success(f"Frontend dependency: {dep}@{deps[dep]}")
                    else:
                        self.log_error(f"Missing frontend dependency: {dep}")
        except FileNotFoundError:
            self.log_error("package.json not found")
        except json.JSONDecodeError:
            self.log_error("package.json is invalid JSON")
            
        # Check requirements.txt
        try:
            with open('requirements.txt', 'r') as f:
                requirements = f.read().lower()
                
                key_backend_deps = [
                    'fastapi', 'uvicorn', 'websockets', 'pydantic', 'openai'
                ]
                
                for dep in key_backend_deps:
                    if dep in requirements:
                        self.log_success(f"Backend dependency found: {dep}")
                    else:
                        self.log_error(f"Missing backend dependency: {dep}")
        except FileNotFoundError:
            self.log_error("requirements.txt not found")

    def run_validation(self):
        """Run all validation checks"""
        print("🔍 BotArmy Environment Configuration Validation")
        print("=" * 60)
        
        self.validate_api_keys()
        print()
        self.validate_backend_config()
        print()
        self.validate_websocket_config()
        print()
        self.validate_frontend_config()
        print()
        self.validate_safety_config()
        print()
        self.validate_development_config()
        print()
        self.validate_file_structure()
        print()
        self.validate_dependencies()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
            print()
            
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
            print()
            
        if self.info:
            print("ℹ️  INFO:")
            for info in self.info[:5]:  # Show first 5 info items
                print(f"  {info}")
            if len(self.info) > 5:
                print(f"  ... and {len(self.info) - 5} more items")
            print()
        
        # Final assessment
        if not self.errors:
            if not self.warnings:
                print("🎉 ALL CHECKS PASSED - Configuration is optimal")
                return 0
            else:
                print("✅ CONFIGURATION OK - Minor warnings noted")
                return 0
        else:
            print("🚨 CONFIGURATION HAS ISSUES - Please fix errors before proceeding")
            return 1

if __name__ == "__main__":
    validator = EnvironmentValidator()
    exit_code = validator.run_validation()
    sys.exit(exit_code)
