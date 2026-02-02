"""
Coordinator Agent for orchestrating multi-agent workflows
Uses Microsoft Agent Framework with Azure AI Foundry
"""
from typing import Any, Dict, List, Optional
import logging
from .base_agent import BaseAgent
from .blog_writer_agent import BlogWriterAgent
from .data_collector_agent import DataCollectorAgent

logger = logging.getLogger(__name__)


class CoordinatorAgent(BaseAgent):
    """
    Agent that coordinates between multiple specialized agents
    to complete complex tasks
    """
    
    def __init__(
        self,
        name: str = "Coordinator",
        model_deployment: str = "gpt-4",
        blog_writer: Optional[BlogWriterAgent] = None,
        data_collector: Optional[DataCollectorAgent] = None
    ):
        """Initialize the Coordinator Agent"""
        description = (
            "An AI agent specialized in coordinating multiple agents to accomplish "
            "complex tasks. You orchestrate data collection and blog post generation "
            "workflows, ensuring smooth collaboration between specialized agents."
        )
        super().__init__(name, description, model_deployment)
        
        # Initialize sub-agents if not provided
        self.blog_writer = blog_writer or BlogWriterAgent(model_deployment=model_deployment)
        self.data_collector = data_collector or DataCollectorAgent(model_deployment=model_deployment)
        
        logger.info(f"[{self.name}] Initialized with sub-agents: {self.blog_writer.name}, {self.data_collector.name}")
    
    def get_system_prompt(self) -> str:
        """Get the specialized system prompt for coordination"""
        return (
            f"{super().get_system_prompt()}\n\n"
            "Your role is to:\n"
            "1. Coordinate between the DataCollector and BlogWriter agents\n"
            "2. Manage the workflow from data collection to blog generation\n"
            "3. Ensure data flows properly between agents\n"
            "4. Handle errors and edge cases gracefully\n"
            "5. Optimize the multi-agent collaboration process\n\n"
            "You have access to specialized agents for specific tasks."
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate the multi-agent workflow
        
        Args:
            input_data: Contains task specification and data
            
        Returns:
            Dict with final output from coordinated agents
        """
        message = input_data.get("message", "")
        context = input_data.get("context", {})
        
        logger.info(f"[{self.name}] Starting coordination workflow")
        
        # Determine the task type
        task_type = context.get("task_type", "generate_blog")
        
        if task_type == "generate_blog":
            result = await self._generate_blog_workflow(message, context)
        elif task_type == "collect_data":
            result = await self._collect_data_workflow(message, context)
        else:
            result = {
                "response": f"Unknown task type: {task_type}",
                "success": False
            }
        
        logger.info(f"[{self.name}] Coordination workflow completed")
        
        return result
    
    async def _generate_blog_workflow(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow for generating a blog post from telemetry data
        
        1. Collect and process data using DataCollector
        2. Generate blog post using BlogWriter
        3. Return final blog post
        """
        logger.info(f"[{self.name}] Executing blog generation workflow")
        
        # Step 1: Collect and process telemetry data
        raw_telemetry = context.get("raw_telemetry", {})
        
        collector_input = {
            "message": "Process telemetry data for blog generation",
            "context": {"raw_telemetry": raw_telemetry}
        }
        
        collector_result = await self.data_collector.process(collector_input)
        processed_data = collector_result.get("processed_data", {})
        data_summary = collector_result.get("response", "")
        
        logger.info(f"[{self.name}] Data collection completed")
        
        # Step 2: Generate blog post with processed data
        writer_input = {
            "message": message or "Generate an entertaining blog post",
            "context": {
                "telemetry": processed_data,
                "summary": data_summary
            }
        }
        
        writer_result = await self.blog_writer.process(writer_input)
        blog_post = writer_result.get("response", "")
        
        logger.info(f"[{self.name}] Blog post generation completed")
        
        # Step 3: Return final result
        return {
            "response": blog_post,
            "processed_data": processed_data,
            "data_summary": data_summary,
            "metadata": {
                "agent": self.name,
                "workflow": "generate_blog",
                "steps_completed": ["data_collection", "blog_generation"],
                "sub_agents_used": [self.data_collector.name, self.blog_writer.name]
            },
            "success": True
        }
    
    async def _collect_data_workflow(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow for collecting and processing data only
        """
        logger.info(f"[{self.name}] Executing data collection workflow")
        
        raw_telemetry = context.get("raw_telemetry", {})
        
        collector_input = {
            "message": message or "Collect and process telemetry data",
            "context": {"raw_telemetry": raw_telemetry}
        }
        
        result = await self.data_collector.process(collector_input)
        
        return {
            **result,
            "metadata": {
                "agent": self.name,
                "workflow": "collect_data",
                "steps_completed": ["data_collection"],
                "sub_agents_used": [self.data_collector.name]
            },
            "success": True
        }
    
    async def generate_blog_from_telemetry(
        self,
        raw_telemetry: Dict[str, Any],
        blog_title: Optional[str] = None
    ) -> str:
        """
        Convenience method to generate a blog post from raw telemetry
        
        Args:
            raw_telemetry: Raw telemetry data from IoT devices
            blog_title: Optional title for the blog post
            
        Returns:
            Generated blog post as string
        """
        input_data = {
            "message": blog_title or "Generate an entertaining blog post",
            "context": {
                "task_type": "generate_blog",
                "raw_telemetry": raw_telemetry
            }
        }
        
        result = await self.process(input_data)
        return result.get("response", "")
