"""
Agentic Blog Bird - Agent Modules

Multi-agent system for generating blog posts from bird detection events
using Microsoft Agent Framework on Azure AI Foundry.
"""

from .base_agent import BaseAgent
from .researcher import ResearcherAgent
from .copywriter import CopyWriterAgent
from .publisher import PublisherAgent
from .editor import EditorAgent

__all__ = [
    'BaseAgent',
    'ResearcherAgent',
    'CopyWriterAgent',
    'PublisherAgent',
    'EditorAgent'
]
