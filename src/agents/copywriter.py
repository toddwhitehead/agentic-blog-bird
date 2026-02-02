"""
CopyWriter Agent Module

This agent is responsible for creating engaging blog post narratives
from bird detection data and events.
"""

from typing import Dict, Any


class CopyWriterAgent:
    """
    CopyWriter agent that creates entertaining narratives from bird data.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the CopyWriter agent.
        
        Args:
            config: Configuration dictionary for writing style and preferences
        """
        self.config = config or {}
        self.name = "CopyWriter"
        
    def get_system_message(self) -> str:
        """Return the system message for the copywriter agent."""
        return """You are a CopyWriter agent specialized in creating engaging blog posts about birds and wildlife.

Your responsibilities:
1. Transform raw bird detection data into entertaining narratives
2. Create compelling headlines and introductions
3. Weave together data points into cohesive stories
4. Add personality and humor where appropriate
5. Make technical information accessible to general readers

Writing guidelines:
- Use an enthusiastic but informative tone
- Include specific details from the data (times, species, behaviors)
- Create narrative arcs (beginning, middle, end)
- Use vivid descriptions and engaging language
- Balance entertainment with educational content
- Keep paragraphs concise and readable
- Use transitional phrases to connect ideas
- End with a memorable conclusion or call-to-action

Your blog posts should make readers feel like they're experiencing the backyard bird watching adventure themselves!
"""
    
    def create_headline(self, research_data: str) -> str:
        """
        Create a compelling headline for the blog post.
        
        Args:
            research_data: Research summary from the Researcher agent
            
        Returns:
            Blog post headline
        """
        # This would use LLM to generate creative headlines
        # For now, return a template
        return "A Day in the Life of Our Feathered Backyard Visitors"
    
    def write_introduction(self, research_data: str, headline: str) -> str:
        """
        Write an engaging introduction for the blog post.
        
        Args:
            research_data: Research summary from the Researcher agent
            headline: The headline for the post
            
        Returns:
            Introduction paragraph(s)
        """
        intro_template = """
As dawn broke over the backyard, our AI-powered bird monitoring system sprang to life, 
ready to capture another day of avian adventures. What unfolded was a fascinating 
glimpse into the secret lives of our feathered neighbors.
"""
        return intro_template.strip()
    
    def write_body(self, research_data: str) -> str:
        """
        Write the main body of the blog post.
        
        Args:
            research_data: Research summary from the Researcher agent
            
        Returns:
            Body content of the blog post
        """
        body_template = """
## Morning Rush Hour

The day's activity kicked off early, with the first visitors arriving before most of us 
had our morning coffee. Our sensors captured a flurry of activity as birds claimed their 
favorite spots and established the day's pecking order.

## Midday Discoveries

As the sun climbed higher, we observed some fascinating behaviors. Each species brought 
its own personality to the backyard stage, from the bold and curious to the shy and cautious.

## Evening Wind-Down

As afternoon gave way to evening, the pace began to slow. The last visitors of the day 
made their appearances, wrapping up another chapter in our ongoing backyard bird saga.
"""
        return body_template.strip()
    
    def write_conclusion(self, research_data: str) -> str:
        """
        Write a memorable conclusion for the blog post.
        
        Args:
            research_data: Research summary from the Researcher agent
            
        Returns:
            Conclusion paragraph(s)
        """
        conclusion_template = """
As the day drew to a close, our monitoring system had captured countless moments of natural 
wonder. Each detection tells a story, and together they paint a picture of the vibrant 
ecosystem thriving right in our own backyard. We can't wait to see what tomorrow brings!

Stay tuned for more updates from our feathered friends, and remember to keep your feeders 
full and your bird baths fresh!
"""
        return conclusion_template.strip()
    
    def generate_blog_post(self, research_data: str) -> Dict[str, str]:
        """
        Generate a complete blog post from research data.
        
        Args:
            research_data: Research summary from the Researcher agent
            
        Returns:
            Dictionary containing blog post components
        """
        headline = self.create_headline(research_data)
        introduction = self.write_introduction(research_data, headline)
        body = self.write_body(research_data)
        conclusion = self.write_conclusion(research_data)
        
        # Combine all parts
        full_content = f"{introduction}\n\n{body}\n\n{conclusion}"
        
        return {
            "headline": headline,
            "introduction": introduction,
            "body": body,
            "conclusion": conclusion,
            "full_content": full_content,
            "metadata": {
                "author": "Backyard Bird AI",
                "style": "informative-entertaining",
                "target_audience": "general"
            }
        }
    
    def refine_content(self, content: str, feedback: str) -> str:
        """
        Refine content based on editorial feedback.
        
        Args:
            content: Original content
            feedback: Feedback from the Editor agent
            
        Returns:
            Refined content
        """
        # This would use LLM to refine based on feedback
        return content
