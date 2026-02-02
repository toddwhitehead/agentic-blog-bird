"""
Package initialization for Agentic Blog Bird
"""
from .agents import (
    BaseAgent,
    AgentMessage,
    BlogWriterAgent,
    DataCollectorAgent,
    CoordinatorAgent
)
from .config import (
    AzureAIConfig,
    AgentConfig,
    get_azure_config,
    get_agent_config
)

__version__ = "1.0.0"

__all__ = [
    "BaseAgent",
    "AgentMessage",
    "BlogWriterAgent",
    "DataCollectorAgent",
    "CoordinatorAgent",
    "AzureAIConfig",
    "AgentConfig",
    "get_azure_config",
    "get_agent_config"
]
