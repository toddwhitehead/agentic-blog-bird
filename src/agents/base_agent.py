"""
Base agent implementation using Microsoft Agent Framework
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentMessage:
    """Message structure for agent communication"""
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """
    Base class for agents using Microsoft Agent Framework
    This provides a foundation for building agents that work with Azure AI Foundry
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        model_deployment: str = "gpt-4"
    ):
        """
        Initialize the base agent
        
        Args:
            name: Agent name
            description: Agent description and purpose
            model_deployment: Azure OpenAI deployment name
        """
        self.name = name
        self.description = description
        self.model_deployment = model_deployment
        self.conversation_history: List[AgentMessage] = []
        logger.info(f"Initialized agent: {self.name}")
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a message to the conversation history"""
        message = AgentMessage(role=role, content=content, metadata=metadata)
        self.conversation_history.append(message)
        logger.debug(f"[{self.name}] Added message: {role}")
    
    def get_conversation_history(self) -> List[AgentMessage]:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        logger.info(f"[{self.name}] Cleared conversation history")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results
        
        Args:
            input_data: Input data for the agent to process
            
        Returns:
            Dict containing the agent's response
        """
        pass
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        return f"You are {self.name}, an AI agent. {self.description}"
    
    async def invoke(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Invoke the agent with a user message
        
        Args:
            user_message: The user's message to the agent
            context: Optional context for the agent
            
        Returns:
            The agent's response
        """
        self.add_message("user", user_message)
        
        input_data = {
            "message": user_message,
            "context": context or {},
            "history": self.conversation_history
        }
        
        result = await self.process(input_data)
        response = result.get("response", "")
        
        self.add_message("assistant", response)
        
        return response
