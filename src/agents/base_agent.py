"""
Base Agent Module

Base class for all agents using Microsoft Agent Framework on Azure AI Foundry.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BaseAgent:
    """
    Base agent class that provides common functionality for all agents
    using Microsoft Agent Framework.
    """
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the base agent.
        
        Args:
            name: Name of the agent
            config: Configuration dictionary for the agent
        """
        self.name = name
        self.config = config or {}
        self._client = None
        self._agent = None
        
    def _get_azure_credentials(self) -> Dict[str, str]:
        """
        Get Azure credentials from environment variables.
        
        Returns:
            Dictionary containing Azure credentials
        """
        return {
            "connection_string": os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING", ""),
            "project_name": os.getenv("AZURE_AI_PROJECT_NAME", ""),
            "deployment_name": os.getenv("AZURE_AI_DEPLOYMENT_NAME", ""),
            "tenant_id": os.getenv("AZURE_TENANT_ID", ""),
            "client_id": os.getenv("AZURE_CLIENT_ID", ""),
            "client_secret": os.getenv("AZURE_CLIENT_SECRET", "")
        }
    
    def _initialize_agent_client(self):
        """
        Initialize the Microsoft Agent Framework client.
        This method will be implemented when the agent framework is ready.
        For now, it's a placeholder for future integration.
        """
        # When Microsoft Agent Framework SDK is available, initialize it here:
        # from azure.ai.agent import AIAgentClient
        # credentials = self._get_azure_credentials()
        # self._client = AIAgentClient(
        #     connection_string=credentials["connection_string"],
        #     project_name=credentials["project_name"]
        # )
        pass
    
    def get_system_message(self) -> str:
        """
        Return the system message for the agent.
        This should be overridden by subclasses.
        
        Returns:
            System message string
        """
        return f"You are a {self.name} agent."
    
    def process(self, input_data: Any) -> Any:
        """
        Process input data using the agent.
        This should be overridden by subclasses.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Processed output
        """
        raise NotImplementedError("Subclasses must implement the process method")
    
    def _invoke_agent(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Invoke the agent with a prompt using Microsoft Agent Framework.
        
        Args:
            prompt: The prompt to send to the agent
            context: Optional context dictionary
            
        Returns:
            Agent response as string
        """
        # This is a placeholder implementation
        # When Microsoft Agent Framework is fully integrated, this will use the actual SDK
        
        # For now, we'll use the system message and prompt to structure a response
        system_msg = self.get_system_message()
        
        # In the future, this would call the Azure AI Foundry agent:
        # response = self._client.invoke_agent(
        #     agent_id=self._agent.id,
        #     messages=[
        #         {"role": "system", "content": system_msg},
        #         {"role": "user", "content": prompt}
        #     ],
        #     context=context
        # )
        # return response.content
        
        # For now, return a formatted placeholder
        return f"[{self.name} Agent Response]\n\nPrompt processed successfully."
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get agent metadata.
        
        Returns:
            Dictionary containing agent metadata
        """
        return {
            "name": self.name,
            "framework": "Microsoft Agent Framework",
            "platform": "Azure AI Foundry",
            "config": self.config
        }
