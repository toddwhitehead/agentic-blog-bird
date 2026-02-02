"""
Configuration management utilities for the agentic blog bird system.
"""

import os
import json
import yaml
from typing import Dict, Any


class Config:
    """Configuration manager for the blog bird system."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file (JSON or YAML)
        """
        self.config_path = config_path
        self.config_data = {}
        
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
        else:
            self.config_data = self.get_default_config()
    
    def load_config(self, config_path: str):
        """Load configuration from file."""
        with open(config_path, 'r') as f:
            if config_path.endswith('.json'):
                self.config_data = json.load(f)
            elif config_path.endswith(('.yml', '.yaml')):
                self.config_data = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported config format: {config_path}")
    
    def save_config(self, output_path: str):
        """Save configuration to file."""
        with open(output_path, 'w') as f:
            if output_path.endswith('.json'):
                json.dump(self.config_data, f, indent=2)
            elif output_path.endswith(('.yml', '.yaml')):
                yaml.dump(self.config_data, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split('.')
        value = self.config_data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        keys = key.split('.')
        config = self.config_data
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "researcher": {
                "fabric_workspace": "",
                "fabric_endpoint": "",
                "data_retention_days": 7
            },
            "copywriter": {
                "style": "informative-entertaining",
                "target_audience": "general",
                "word_count_target": 800
            },
            "publisher": {
                "output_dir": "content/posts",
                "hugo_base_url": "",
                "default_author": "Backyard Bird AI"
            },
            "editor": {
                "quality_threshold": 0.8,
                "auto_publish": False,
                "review_required": True
            },
            "llm": {
                "provider": "azure_ai_foundry",
                "deployment_name": "",
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }


def load_env_config() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    return {
        "azure_ai_project_connection_string": os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING"),
        "azure_ai_project_name": os.getenv("AZURE_AI_PROJECT_NAME"),
        "azure_ai_deployment_name": os.getenv("AZURE_AI_DEPLOYMENT_NAME"),
        "azure_tenant_id": os.getenv("AZURE_TENANT_ID"),
        "azure_client_id": os.getenv("AZURE_CLIENT_ID"),
        "azure_client_secret": os.getenv("AZURE_CLIENT_SECRET"),
        "fabric_workspace": os.getenv("FABRIC_WORKSPACE"),
        "fabric_token": os.getenv("FABRIC_TOKEN"),
    }
