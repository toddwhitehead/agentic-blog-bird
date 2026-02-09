"""
Main entry point for the Agentic Blog Bird system.

This module provides the main interface for running the multi-agent
blog post generation workflow using Microsoft Agent Framework on Azure AI Foundry.
"""

import argparse
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents import EditorAgent
from utils.config import Config


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='Generate blog posts from bird detection events using multi-agent system'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Date to generate blog post for (YYYY-MM-DD format)',
        default=datetime.now().strftime("%Y-%m-%d")
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file',
        default='config/config.yaml'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Output directory for blog posts',
        default='content/posts'
    )
    parser.add_argument(
        '--all-files',
        action='store_true',
        help='Process all data files from blob storage (one blog post per file)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    if os.path.exists(args.config):
        config = Config(args.config)
    else:
        print(f"Configuration file not found: {args.config}")
        print("Using default configuration...")
        config = Config()
    
    # Override output directory if specified
    if args.output_dir:
        config.set('publisher.output_dir', args.output_dir)
    
    # Initialize Editor agent (which manages all other agents)
    print("\n" + "="*60)
    print("Agentic Blog Bird - Multi-Agent Blog Post Generator")
    print("Powered by Microsoft Agent Framework on Azure AI Foundry")
    print("="*60 + "\n")
    
    editor = EditorAgent(config.config_data)
    
    # Run the blog creation workflow
    try:
        if args.all_files:
            # Process all data files from blob storage
            print(f"Mode: Processing all data files from blob storage\n")
            result = editor.orchestrate_multiple_blog_creation()
            
            if result['status'] == 'completed':
                print("\n✓ Multiple blog post generation completed!")
                print(f"\nTotal files processed: {result['total_files']}")
                print(f"Posts created: {result['posts_created']}")
                print(f"Posts failed: {result['posts_failed']}")
                
                if result.get('posts'):
                    print("\nGenerated posts:")
                    for post in result['posts']:
                        if post['status'] == 'completed':
                            print(f"  ✓ {post['file']} -> {post.get('output_path')}")
                        else:
                            print(f"  ✗ {post['file']} - {post.get('reason', post.get('error', 'Unknown error'))}")
                
                return 0 if result['posts_failed'] == 0 else 1
            else:
                print("\n✗ Multiple blog post generation failed!")
                return 1
        else:
            # Single blog post mode (backward compatible)
            result = editor.orchestrate_blog_creation(args.date)
            
            if result['status'] == 'completed':
                print("\n✓ Blog post generation completed successfully!")
                if result.get('final_post'):
                    post = result['final_post']
                    print(f"\nTitle: {post.get('headline')}")
                    print(f"Date: {post.get('date')}")
                    print(f"Output: {post.get('output_path')}")
                
                return 0
            else:
                print("\n✗ Blog post generation failed!")
                if result.get('error'):
                    print(f"Error: {result['error']}")
                return 1
            
    except Exception as e:
        print(f"\n✗ Error during blog post generation: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
