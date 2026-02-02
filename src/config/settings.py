"""
Configuration module for Azure AI Foundry and Agent Framework
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AzureAIConfig(BaseModel):
    """Configuration for Azure AI Foundry connection"""
    
    project_endpoint: str = Field(
        default_factory=lambda: os.getenv("AZURE_AI_PROJECT_ENDPOINT", ""),
        description="Azure AI Project endpoint URL"
    )
    subscription_id: str = Field(
        default_factory=lambda: os.getenv("AZURE_SUBSCRIPTION_ID", ""),
        description="Azure subscription ID"
    )
    resource_group: str = Field(
        default_factory=lambda: os.getenv("AZURE_RESOURCE_GROUP", ""),
        description="Azure resource group name"
    )
    project_name: str = Field(
        default_factory=lambda: os.getenv("AZURE_PROJECT_NAME", ""),
        description="Azure AI project name"
    )
    connection_string: Optional[str] = Field(
        default_factory=lambda: os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING"),
        description="Azure AI Project connection string"
    )
    
    # Authentication
    client_id: Optional[str] = Field(
        default_factory=lambda: os.getenv("AZURE_CLIENT_ID"),
        description="Azure client ID for authentication"
    )
    client_secret: Optional[str] = Field(
        default_factory=lambda: os.getenv("AZURE_CLIENT_SECRET"),
        description="Azure client secret for authentication"
    )
    tenant_id: Optional[str] = Field(
        default_factory=lambda: os.getenv("AZURE_TENANT_ID"),
        description="Azure tenant ID for authentication"
    )
    
    # Model configuration
    openai_deployment: str = Field(
        default_factory=lambda: os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4"),
        description="Azure OpenAI deployment name"
    )
    api_version: str = Field(
        default_factory=lambda: os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        description="Azure OpenAI API version"
    )


class AgentConfig(BaseModel):
    """Configuration for individual agents"""
    
    blog_writer_name: str = Field(
        default_factory=lambda: os.getenv("BLOG_WRITER_AGENT_NAME", "BlogWriter"),
        description="Name for the blog writer agent"
    )
    data_collector_name: str = Field(
        default_factory=lambda: os.getenv("DATA_COLLECTOR_AGENT_NAME", "DataCollector"),
        description="Name for the data collector agent"
    )
    coordinator_name: str = Field(
        default_factory=lambda: os.getenv("COORDINATOR_AGENT_NAME", "Coordinator"),
        description="Name for the coordinator agent"
    )


def get_azure_config() -> AzureAIConfig:
    """Get Azure AI configuration"""
    return AzureAIConfig()


def get_agent_config() -> AgentConfig:
    """Get agent configuration"""
    return AgentConfig()
