"""
Publisher Agent Module

This agent is responsible for formatting blog posts for Hugo-based sites.
"""

from typing import Dict, Any
from datetime import datetime
import os
from .base_agent import BaseAgent


class PublisherAgent(BaseAgent):
    """
    Publisher agent that formats blog posts for Hugo static site generator.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Publisher agent.
        
        Args:
            config: Configuration dictionary for Hugo settings and output paths
        """
        super().__init__(name="Publisher", config=config)
        self.output_dir = self.config.get('output_dir', 'content/posts')
        self._initialize_agent_client()
        
    def get_system_message(self) -> str:
        """Return the system message for the publisher agent."""
        return """You are a Publisher agent specialized in formatting content for Hugo static sites.

Your responsibilities:
1. Format blog posts according to Hugo conventions
2. Create proper front matter with metadata
3. Organize content structure for optimal rendering
4. Handle image references and media assets
5. Ensure proper markdown formatting
6. Generate SEO-friendly URLs and metadata
7. Validate output format before publishing

Hugo front matter requirements:
- title: Blog post title
- date: Publication date (ISO 8601 format)
- draft: Boolean indicating draft status
- tags: Array of relevant tags
- categories: Array of categories
- author: Author name
- description: Short description for SEO
- featured_image: Path to featured image (if available)

Ensure all markdown is properly formatted and Hugo shortcodes are correctly used.
"""
    
    def create_frontmatter(self, post_data: Dict[str, Any]) -> str:
        """
        Create Hugo front matter for the blog post.
        
        Args:
            post_data: Dictionary containing post data and metadata
            
        Returns:
            Formatted front matter as YAML
        """
        title = post_data.get('headline', 'Untitled Post')
        date = post_data.get('date', datetime.now().isoformat())
        author = post_data.get('author', 'Backyard Bird AI')
        description = post_data.get('description', 
                                   'Daily highlights from our backyard bird monitoring system')
        tags = post_data.get('tags', ['birds', 'wildlife', 'backyard', 'AI monitoring'])
        categories = post_data.get('categories', ['Daily Updates'])
        draft = post_data.get('draft', False)
        
        frontmatter = f"""---
title: "{title}"
date: {date}
draft: {str(draft).lower()}
author: "{author}"
description: "{description}"
tags: [{', '.join(f'"{tag}"' for tag in tags)}]
categories: [{', '.join(f'"{cat}"' for cat in categories)}]
---
"""
        return frontmatter
    
    def format_content(self, content: str) -> str:
        """
        Format content for Hugo markdown rendering.
        
        Args:
            content: Raw blog post content
            
        Returns:
            Formatted content with proper markdown
        """
        # Ensure proper spacing and formatting
        formatted = content.strip()
        
        # Add any Hugo-specific formatting here
        # For example, converting image references to Hugo shortcodes
        
        return formatted
    
    def create_slug(self, title: str, date: str = None) -> str:
        """
        Create a URL-friendly slug for the blog post.
        
        Args:
            title: Blog post title
            date: Publication date
            
        Returns:
            URL-friendly slug
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Convert title to lowercase and replace spaces with hyphens
        slug = title.lower()
        slug = ''.join(c if c.isalnum() or c.isspace() else '' for c in slug)
        slug = '-'.join(slug.split())
        
        # Add date prefix for organization
        date_prefix = date[:10]  # YYYY-MM-DD
        
        return f"{date_prefix}-{slug}"
    
    def publish_post(self, post_data: Dict[str, Any], output_path: str = None) -> str:
        """
        Publish the blog post by creating a Hugo-formatted markdown file.
        
        Args:
            post_data: Complete blog post data including content and metadata
            output_path: Optional custom output path
            
        Returns:
            Path to the published file
        """
        # Create front matter
        frontmatter = self.create_frontmatter(post_data)
        
        # Format content
        content = self.format_content(post_data.get('full_content', ''))
        
        # Combine front matter and content
        full_post = f"{frontmatter}\n{content}\n"
        
        # Determine output path
        if output_path is None:
            slug = self.create_slug(
                post_data.get('headline', 'untitled'),
                post_data.get('date', None)
            )
            filename = f"{slug}.md"
            output_path = os.path.join(self.output_dir, filename)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_post)
        
        return output_path
    
    def validate_hugo_format(self, filepath: str) -> Dict[str, Any]:
        """
        Validate that a Hugo post is properly formatted.
        
        Args:
            filepath: Path to the Hugo markdown file
            
        Returns:
            Dictionary containing validation results
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for front matter
            if not content.startswith('---'):
                validation['valid'] = False
                validation['errors'].append("Missing front matter delimiter")
            
            # Check for required fields (basic check)
            required_fields = ['title:', 'date:', 'draft:']
            for field in required_fields:
                if field not in content:
                    validation['warnings'].append(f"Missing recommended field: {field}")
            
        except Exception as e:
            validation['valid'] = False
            validation['errors'].append(f"Error reading file: {str(e)}")
        
        return validation
    
    def generate_summary(self, post_data: Dict[str, Any]) -> str:
        """
        Generate a publishing summary report.
        
        Args:
            post_data: Published post data
            
        Returns:
            Summary report as string
        """
        summary = f"""
# Publishing Summary

- Title: {post_data.get('headline', 'N/A')}
- Date: {post_data.get('date', 'N/A')}
- Author: {post_data.get('author', 'N/A')}
- Status: Published
- Format: Hugo Markdown
- Output: {post_data.get('output_path', 'N/A')}

Blog post has been formatted and is ready for Hugo site generation.
"""
        return summary
