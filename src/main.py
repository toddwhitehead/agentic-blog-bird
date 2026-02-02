"""
Main module for the Agentic Blog Bird application
Multi-agent system using Microsoft Agent Framework with Azure AI Foundry
"""
import asyncio
import logging
from typing import Dict, Any
from src.agents import CoordinatorAgent
from src.config import get_azure_config, get_agent_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgenticBlogBird:
    """
    Main application class for the multi-agent blog generation system
    """
    
    def __init__(self):
        """Initialize the application with agents and configuration"""
        logger.info("Initializing Agentic Blog Bird application")
        
        # Load configuration
        self.azure_config = get_azure_config()
        self.agent_config = get_agent_config()
        
        # Initialize coordinator agent (which initializes sub-agents)
        self.coordinator = CoordinatorAgent(
            name=self.agent_config.coordinator_name,
            model_deployment=self.azure_config.openai_deployment
        )
        
        logger.info("Application initialized successfully")
    
    async def generate_blog_post(
        self,
        raw_telemetry: Dict[str, Any],
        title: str = None
    ) -> str:
        """
        Generate a blog post from raw telemetry data
        
        Args:
            raw_telemetry: Raw telemetry data from IoT devices
            title: Optional title for the blog post
            
        Returns:
            Generated blog post as string
        """
        logger.info("Generating blog post from telemetry data")
        
        blog_post = await self.coordinator.generate_blog_from_telemetry(
            raw_telemetry=raw_telemetry,
            blog_title=title
        )
        
        logger.info("Blog post generation completed")
        return blog_post
    
    async def run(self):
        """Run the application with example data"""
        logger.info("Running Agentic Blog Bird with example data")
        
        # Example telemetry data
        example_telemetry = {
            "sensors": {
                "temperature": {
                    "value": 72.5,
                    "unit": "F",
                    "timestamp": "2026-02-02T09:00:00Z"
                },
                "humidity": {
                    "value": 65,
                    "unit": "%",
                    "timestamp": "2026-02-02T09:00:00Z"
                },
                "motion": {
                    "value": True,
                    "timestamp": "2026-02-02T08:45:00Z"
                }
            },
            "notifications": [
                {
                    "message": "Bird activity detected at feeder",
                    "priority": "normal",
                    "timestamp": "2026-02-02T08:45:00Z"
                },
                {
                    "message": "Water level low in birdbath",
                    "priority": "low",
                    "timestamp": "2026-02-02T09:00:00Z"
                }
            ]
        }
        
        # Generate blog post
        blog_post = await self.generate_blog_post(
            raw_telemetry=example_telemetry,
            title="Morning Adventures in the Backyard"
        )
        
        # Display the result
        print("\n" + "=" * 80)
        print("GENERATED BLOG POST")
        print("=" * 80)
        print(blog_post)
        print("=" * 80 + "\n")
        
        logger.info("Application run completed")


async def main():
    """Main entry point"""
    app = AgenticBlogBird()
    await app.run()


if __name__ == "__main__":
    # Run the application
    asyncio.run(main())
