"""
Editor Agent Module

This agent is responsible for orchestrating other agents to ensure
quality blog post production using Microsoft Agent Framework.
"""

from typing import Dict, Any, List
from datetime import datetime
from .base_agent import BaseAgent
from .researcher import ResearcherAgent
from .copywriter import CopyWriterAgent
from .artist import ArtistAgent
from .publisher import PublisherAgent
from .delivery import DeliveryAgent


class EditorAgent(BaseAgent):
    """
    Editor agent that orchestrates the blog post creation workflow
    using Microsoft Agent Framework on Azure AI Foundry.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Editor agent.
        
        Args:
            config: Configuration dictionary for all agents and workflow
        """
        super().__init__(name="Editor", config=config)
        
        # Initialize other agents
        self.researcher = ResearcherAgent(self.config.get('researcher', {}))
        self.copywriter = CopyWriterAgent(self.config.get('copywriter', {}))
        self.artist = ArtistAgent(self.config.get('artist', {}))
        self.publisher = PublisherAgent(self.config.get('publisher', {}))
        self.delivery = DeliveryAgent(self.config.get('delivery', {}))
        
        self.workflow_history = []
        self._initialize_agent_client()
        
    def get_system_message(self) -> str:
        """Return the system message for the editor agent."""
        return """You are an Editor agent running on Microsoft Agent Framework in Azure AI Foundry, 
responsible for orchestrating a team of specialized agents to produce high-quality blog posts 
about bird detection events.

Your responsibilities:
1. Coordinate the workflow between Researcher, CopyWriter, Artist, and Publisher agents
2. Ensure data quality and accuracy from research phase
3. Review and approve blog post content for quality and tone
4. Oversee image generation for visual appeal
5. Provide constructive feedback to improve content
6. Manage the publishing pipeline
7. Maintain quality standards across all blog posts

Workflow management:
- Request research data from the Researcher agent
- Review research for completeness and interesting content
- Direct the CopyWriter to create engaging narratives
- Coordinate with Artist to create accompanying cartoon-style images
- Review drafts and provide feedback for improvements
- Coordinate with Publisher for proper formatting
- Ensure final output meets all quality standards

Quality criteria:
- Accuracy: All data must be factually correct
- Engagement: Content must be interesting and readable
- Visual Appeal: Images should complement the narrative
- Structure: Clear beginning, middle, and end
- Formatting: Proper Hugo markdown format
- SEO: Appropriate metadata and descriptions
- Consistency: Maintains voice and style guidelines

You have the authority to request revisions from any agent to ensure the final product 
meets publication standards.
"""
    
    def orchestrate_blog_creation(self, date: str = None) -> Dict[str, Any]:
        """
        Orchestrate the complete blog post creation workflow.
        
        Args:
            date: Date to create blog post for (YYYY-MM-DD format)
            
        Returns:
            Dictionary containing workflow results and final post data
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        workflow_result = {
            "date": date,
            "status": "started",
            "steps": [],
            "final_post": None
        }
        
        print(f"\n{'='*60}")
        print(f"Editor: Starting blog post creation workflow for {date}")
        print(f"{'='*60}\n")
        
        # Step 1: Research Phase
        print("Step 1: Research Phase")
        print("-" * 60)
        research_summary = self._conduct_research(date)
        workflow_result["steps"].append({
            "phase": "research",
            "status": "completed",
            "output_length": len(research_summary)
        })
        
        # Step 2: Review Research
        print("\nStep 2: Review Research")
        print("-" * 60)
        research_approved = self._review_research(research_summary)
        workflow_result["steps"].append({
            "phase": "research_review",
            "status": "approved" if research_approved else "needs_revision"
        })
        
        if not research_approved:
            workflow_result["status"] = "failed"
            workflow_result["error"] = "Research did not meet quality standards"
            return workflow_result
        
        # Step 3: Content Creation
        print("\nStep 3: Content Creation Phase")
        print("-" * 60)
        blog_post = self._create_content(research_summary)
        workflow_result["steps"].append({
            "phase": "content_creation",
            "status": "completed",
            "headline": blog_post.get("headline")
        })
        
        # Step 4: Editorial Review
        print("\nStep 4: Editorial Review")
        print("-" * 60)
        content_approved = self._review_content(blog_post)
        workflow_result["steps"].append({
            "phase": "content_review",
            "status": "approved" if content_approved else "needs_revision"
        })
        
        if not content_approved:
            # In a full implementation, this would loop back for revisions
            print("Content needs revision (would request changes in full implementation)")
        
        # Step 5: Image Generation
        print("\nStep 5: Image Generation Phase")
        print("-" * 60)
        image_result = self._generate_image(blog_post)
        workflow_result["steps"].append({
            "phase": "image_generation",
            "status": "completed" if image_result.get("success") else "skipped",
            "image_path": image_result.get("image_path")
        })
        
        # Add image to blog post data if generated successfully
        if image_result.get("success"):
            blog_post['featured_image'] = image_result.get('image_path')
        
        # Step 6: Publishing
        print("\nStep 6: Publishing Phase")
        print("-" * 60)
        published_path = self._publish_content(blog_post, date)
        workflow_result["steps"].append({
            "phase": "publishing",
            "status": "completed",
            "output_path": published_path
        })
        
        # Step 7: Final Validation
        print("\nStep 7: Final Validation")
        print("-" * 60)
        validation = self._validate_output(published_path)
        workflow_result["steps"].append({
            "phase": "validation",
            "status": "completed",
            "validation_result": validation
        })
        
        # Step 8: Delivery (optional, based on configuration)
        auto_deliver = self.config.get('delivery', {}).get('auto_deliver', False)
        if auto_deliver:
            print("\nStep 8: Delivery Phase")
            print("-" * 60)
            delivery_result = self._deliver_content(published_path, blog_post)
            workflow_result["steps"].append({
                "phase": "delivery",
                "status": delivery_result.get("status"),
                "deployment_triggered": delivery_result.get("deployment_triggered", False)
            })
        else:
            print("\nStep 8: Delivery Phase (Skipped)")
            print("-" * 60)
            print("Delivery: Auto-delivery is disabled. To deliver manually, use:")
            print(f"  delivery.deliver_blog_post('{published_path}', post_metadata)")
            workflow_result["steps"].append({
                "phase": "delivery",
                "status": "skipped",
                "note": "Auto-delivery is disabled in configuration"
            })
        
        workflow_result["status"] = "completed"
        workflow_result["final_post"] = {
            "headline": blog_post.get("headline"),
            "output_path": published_path,
            "date": date
        }
        
        print(f"\n{'='*60}")
        print(f"Editor: Workflow completed successfully!")
        print(f"Blog post published to: {published_path}")
        print(f"{'='*60}\n")
        
        # Store in history
        self.workflow_history.append(workflow_result)
        
        return workflow_result
    
    def _conduct_research(self, date: str) -> str:
        """Conduct research phase using Researcher agent."""
        print("Editor: Requesting research from Researcher agent...")
        research_summary = self.researcher.generate_research_summary(date)
        print(f"Editor: Received research summary ({len(research_summary)} characters)")
        return research_summary
    
    def _review_research(self, research_summary: str) -> bool:
        """Review research quality."""
        print("Editor: Reviewing research quality...")
        
        # Basic quality checks
        checks = {
            "has_content": len(research_summary) > 100,
            "has_structure": "##" in research_summary,
            "has_date": any(char.isdigit() for char in research_summary)
        }
        
        passed = all(checks.values())
        
        if passed:
            print("Editor: Research approved ✓")
        else:
            print("Editor: Research needs improvement")
            for check, result in checks.items():
                print(f"  - {check}: {'✓' if result else '✗'}")
        
        return passed
    
    def _create_content(self, research_summary: str) -> Dict[str, Any]:
        """Create content using CopyWriter agent."""
        print("Editor: Requesting content from CopyWriter agent...")
        blog_post = self.copywriter.generate_blog_post(research_summary)
        print(f"Editor: Received blog post: '{blog_post.get('headline')}'")
        return blog_post
    
    def _review_content(self, blog_post: Dict[str, Any]) -> bool:
        """Review blog post content quality."""
        print("Editor: Reviewing content quality...")
        
        # Quality checks
        checks = {
            "has_headline": bool(blog_post.get("headline")),
            "has_introduction": bool(blog_post.get("introduction")),
            "has_body": bool(blog_post.get("body")),
            "has_conclusion": bool(blog_post.get("conclusion")),
            "sufficient_length": len(blog_post.get("full_content", "")) > 200
        }
        
        passed = all(checks.values())
        
        if passed:
            print("Editor: Content approved ✓")
        else:
            print("Editor: Content needs improvement")
            for check, result in checks.items():
                print(f"  - {check}: {'✓' if result else '✗'}")
        
        return passed
    
    def _generate_image(self, blog_post: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image using Artist agent."""
        print("Editor: Requesting image from Artist agent...")
        print("Editor: Style: Wile E. Coyote and Road Runner cartoon inspiration")
        
        image_result = self.artist.create_blog_image(blog_post)
        
        if image_result.get("success"):
            print(f"Editor: Image generated successfully!")
            print(f"Editor: Image path: {image_result.get('image_path')}")
        else:
            print(f"Editor: Image generation skipped or failed")
            if image_result.get("note"):
                print(f"Editor: {image_result.get('note')}")
        
        return image_result
    
    def _publish_content(self, blog_post: Dict[str, Any], date: str) -> str:
        """Publish content using Publisher agent."""
        print("Editor: Requesting publishing from Publisher agent...")
        
        # Add date to post data
        blog_post['date'] = date
        blog_post['author'] = blog_post.get('metadata', {}).get('author', 'Backyard Bird AI')
        
        # Publish
        output_path = self.publisher.publish_post(blog_post)
        print(f"Editor: Content published to {output_path}")
        
        return output_path
    
    def _validate_output(self, filepath: str) -> Dict[str, Any]:
        """Validate the published output."""
        print("Editor: Validating published output...")
        validation = self.publisher.validate_hugo_format(filepath)
        
        if validation['valid']:
            print("Editor: Validation passed ✓")
        else:
            print("Editor: Validation issues found:")
            for error in validation['errors']:
                print(f"  - Error: {error}")
            for warning in validation['warnings']:
                print(f"  - Warning: {warning}")
        
        return validation
    
    def _deliver_content(self, published_path: str, blog_post: Dict[str, Any]) -> Dict[str, Any]:
        """Deliver content using Delivery agent."""
        print("Editor: Requesting delivery from Delivery agent...")
        
        # Prepare post metadata for delivery
        post_metadata = {
            'headline': blog_post.get('headline'),
            'featured_image': blog_post.get('featured_image')
        }
        
        # Deliver
        delivery_result = self.delivery.deliver_blog_post(published_path, post_metadata)
        
        if delivery_result.get('status') == 'completed':
            print("Editor: Content delivered successfully ✓")
            print("Editor: Azure Static Web App deployment triggered")
        else:
            print("Editor: Delivery encountered issues:")
            for error in delivery_result.get('errors', []):
                print(f"  - Error: {error}")
        
        return delivery_result
    
    def get_workflow_summary(self) -> str:
        """
        Get a summary of all workflow executions.
        
        Returns:
            Formatted summary string
        """
        if not self.workflow_history:
            return "No workflows executed yet."
        
        summary = f"\n# Workflow History ({len(self.workflow_history)} executions)\n\n"
        
        for i, workflow in enumerate(self.workflow_history, 1):
            summary += f"## Execution {i}\n"
            summary += f"- Date: {workflow['date']}\n"
            summary += f"- Status: {workflow['status']}\n"
            
            if workflow.get('final_post'):
                post = workflow['final_post']
                summary += f"- Title: {post.get('headline')}\n"
                summary += f"- Output: {post.get('output_path')}\n"
            
            summary += f"- Steps completed: {len(workflow['steps'])}\n\n"
        
        return summary
