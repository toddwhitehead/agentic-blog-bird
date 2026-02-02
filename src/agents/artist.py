"""
Artist Agent Module

This agent is responsible for generating original cartoon-style images
to accompany blog posts using Wile E. Coyote and Road Runner cartoon inspiration.
"""

from typing import Dict, Any, Optional
import os
import base64
import requests
from .base_agent import BaseAgent


class ArtistAgent(BaseAgent):
    """
    Artist agent that generates cartoon-style images for blog posts.
    Inspired by Wile E. Coyote and Road Runner cartoons.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Artist agent.
        
        Args:
            config: Configuration dictionary for image generation settings
        """
        super().__init__(name="Artist", config=config)
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        self.api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://api.openai.com/v1")
        self.image_style = self.config.get('image_style', 'cartoon')
        self.image_size = self.config.get('image_size', '1024x1024')
        self.output_dir = self.config.get('output_dir', 'content/posts/images')
        self._initialize_agent_client()
        
    def get_system_message(self) -> str:
        """Return the system message for the artist agent."""
        return """You are an Artist agent specialized in creating original cartoon-style images 
inspired by classic Looney Tunes cartoons, particularly Wile E. Coyote and Road Runner.

Your responsibilities:
1. Analyze blog post content to identify key visual moments
2. Generate image prompts that capture the essence of the story
3. Create vibrant, cartoon-style images with exaggerated expressions and dynamic action
4. Maintain the playful, energetic aesthetic of classic Warner Bros. cartoons
5. Ensure images complement and enhance the blog post narrative

Artistic style guidelines:
- Bold, vibrant colors reminiscent of classic Looney Tunes
- Exaggerated character expressions and body language
- Dynamic action poses and movement
- Desert/southwestern landscape elements when appropriate
- Comedic timing and visual humor
- Simple but expressive character designs
- Clear silhouettes and strong composition
- Playful, energetic atmosphere

Your images should capture the spirit and personality of bird watching through 
the lens of classic cartoon comedy!
"""
    
    def generate_image_prompt(self, blog_post_content: str) -> str:
        """
        Generate an image prompt based on blog post content.
        
        Args:
            blog_post_content: The full blog post content
            
        Returns:
            Image generation prompt optimized for cartoon style
        """
        # Extract key themes from blog content
        # In production, this would use LLM to analyze content
        
        # Base cartoon style prompt inspired by Wile E. Coyote and Road Runner
        base_style = """A vibrant cartoon illustration in the style of classic Warner Bros. 
Looney Tunes cartoons (Wile E. Coyote and Road Runner era). Features bold colors, 
exaggerated expressions, dynamic action poses, and comedic energy."""
        
        # Create scene description based on blog content
        scene_description = """Backyard birds at bird feeders, with playful and energetic 
poses. Birds show exaggerated cartoon personalities - some are comically surprised, 
others are scheming or excited. Desert southwestern aesthetic with vibrant blue sky, 
scattered clouds, and typical backyard setting. Comedic and entertaining mood."""
        
        full_prompt = f"{base_style} {scene_description}"
        
        return full_prompt
    
    def generate_image(self, prompt: str, filename: str = None) -> Dict[str, Any]:
        """
        Generate an image using AI image generation API.
        
        Args:
            prompt: Image generation prompt
            filename: Optional custom filename for the image
            
        Returns:
            Dictionary containing image data and metadata
        """
        result = {
            "success": False,
            "image_path": None,
            "image_url": None,
            "prompt": prompt,
            "error": None
        }
        
        # Check if API key is available
        if not self.api_key:
            result["error"] = "Image generation API key not configured (OPENAI_API_KEY or AZURE_OPENAI_API_KEY)"
            result["note"] = "Image generation is optional. Set API key to enable this feature."
            print(f"Artist: {result['error']}")
            print(f"Artist: {result['note']}")
            return result
        
        try:
            # Determine API endpoint
            if "azure" in self.api_endpoint.lower():
                # Azure OpenAI DALL-E endpoint
                api_url = f"{self.api_endpoint}/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"
                headers = {
                    "api-key": self.api_key,
                    "Content-Type": "application/json"
                }
            else:
                # OpenAI DALL-E endpoint
                api_url = f"{self.api_endpoint}/images/generations"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            
            # Prepare request payload
            payload = {
                "prompt": prompt,
                "n": 1,
                "size": self.image_size,
                "quality": "standard",
                "style": "vivid"  # Vivid style for more vibrant, cartoon-like results
            }
            
            print(f"Artist: Generating image with cartoon style...")
            print(f"Artist: Prompt: {prompt[:100]}...")
            
            # Make API request
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                image_url = data['data'][0]['url']
                
                # Download and save image
                image_response = requests.get(image_url, timeout=30)
                
                if image_response.status_code == 200:
                    # Create output directory
                    os.makedirs(self.output_dir, exist_ok=True)
                    
                    # Generate filename
                    if filename is None:
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"blog_image_{timestamp}.png"
                    
                    # Ensure .png extension
                    if not filename.endswith('.png'):
                        filename = f"{filename}.png"
                    
                    image_path = os.path.join(self.output_dir, filename)
                    
                    # Save image
                    with open(image_path, 'wb') as f:
                        f.write(image_response.content)
                    
                    result["success"] = True
                    result["image_path"] = image_path
                    result["image_url"] = image_url
                    
                    print(f"Artist: Image generated successfully!")
                    print(f"Artist: Saved to: {image_path}")
                else:
                    result["error"] = f"Failed to download image: HTTP {image_response.status_code}"
                    print(f"Artist: {result['error']}")
            else:
                result["error"] = f"Image generation failed: HTTP {response.status_code} - {response.text}"
                print(f"Artist: {result['error']}")
                
        except requests.exceptions.Timeout:
            result["error"] = "Image generation request timed out"
            print(f"Artist: {result['error']}")
        except Exception as e:
            result["error"] = f"Error generating image: {str(e)}"
            print(f"Artist: {result['error']}")
        
        return result
    
    def create_blog_image(self, blog_post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an image for a blog post based on its content.
        
        Args:
            blog_post_data: Complete blog post data including content and metadata
            
        Returns:
            Dictionary containing image generation results
        """
        print("\nArtist: Creating cartoon-style image for blog post...")
        print("Artist: Using Wile E. Coyote and Road Runner cartoon inspiration")
        
        # Extract content from blog post
        full_content = blog_post_data.get('full_content', '')
        headline = blog_post_data.get('headline', '')
        
        # Generate optimized image prompt
        image_prompt = self.generate_image_prompt(full_content)
        
        # Generate filename based on blog post slug
        date = blog_post_data.get('date', '')
        if date and headline:
            # Create slug from headline for filename
            slug = headline.lower()
            slug = ''.join(c if c.isalnum() or c.isspace() else '' for c in slug)
            slug = '-'.join(slug.split())
            filename = f"{date[:10]}-{slug}"
        else:
            filename = None
        
        # Generate the image
        result = self.generate_image(image_prompt, filename)
        
        # Add metadata
        result['headline'] = headline
        result['style'] = 'Wile E. Coyote and Road Runner cartoon style'
        
        return result
    
    def get_image_metadata(self, image_path: str) -> Dict[str, Any]:
        """
        Get metadata for a generated image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing image metadata
        """
        import os
        
        if not os.path.exists(image_path):
            return {
                "exists": False,
                "error": "Image file not found"
            }
        
        file_size = os.path.getsize(image_path)
        
        return {
            "exists": True,
            "path": image_path,
            "filename": os.path.basename(image_path),
            "size_bytes": file_size,
            "size_kb": round(file_size / 1024, 2)
        }
