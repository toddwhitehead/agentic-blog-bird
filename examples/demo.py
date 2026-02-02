#!/usr/bin/env python3
"""
Example script demonstrating the Agentic Blog Bird system.

This script shows how to use the multi-agent system to generate
blog posts from bird detection events.
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents import EditorAgent, ResearcherAgent, CopyWriterAgent, PublisherAgent


def demo_individual_agents():
    """Demonstrate individual agent capabilities."""
    print("\n" + "="*60)
    print("DEMO: Individual Agent Capabilities")
    print("="*60 + "\n")
    
    # Researcher Agent Demo
    print("1. Researcher Agent Demo")
    print("-" * 60)
    researcher = ResearcherAgent()
    research_summary = researcher.generate_research_summary()
    print(research_summary[:300] + "...\n")
    
    # CopyWriter Agent Demo
    print("2. CopyWriter Agent Demo")
    print("-" * 60)
    copywriter = CopyWriterAgent()
    blog_post = copywriter.generate_blog_post(research_summary)
    print(f"Headline: {blog_post['headline']}")
    print(f"Content length: {len(blog_post['full_content'])} characters\n")
    
    # Publisher Agent Demo
    print("3. Publisher Agent Demo")
    print("-" * 60)
    publisher = PublisherAgent({'output_dir': 'examples/output'})
    frontmatter = publisher.create_frontmatter(blog_post)
    print("Front matter preview:")
    print(frontmatter[:200] + "...\n")


def demo_full_workflow():
    """Demonstrate the complete workflow orchestrated by Editor."""
    print("\n" + "="*60)
    print("DEMO: Complete Workflow with Editor Orchestration")
    print("="*60 + "\n")
    
    # Create output directory
    os.makedirs('examples/output', exist_ok=True)
    
    # Initialize Editor with custom config
    config = {
        'publisher': {
            'output_dir': 'examples/output'
        }
    }
    
    editor = EditorAgent(config)
    
    # Run the complete workflow
    result = editor.orchestrate_blog_creation()
    
    # Display results
    print("\n" + "="*60)
    print("WORKFLOW RESULTS")
    print("="*60 + "\n")
    
    print(f"Status: {result['status']}")
    print(f"Steps completed: {len(result['steps'])}")
    
    if result.get('final_post'):
        post = result['final_post']
        print(f"\nFinal Post:")
        print(f"  Title: {post.get('headline')}")
        print(f"  Date: {post.get('date')}")
        print(f"  Output: {post.get('output_path')}")
        
        # Read and display the published file
        if post.get('output_path') and os.path.exists(post['output_path']):
            print(f"\nPublished content preview:")
            with open(post['output_path'], 'r') as f:
                content = f.read()
                print(content[:500] + "...")


def demo_workflow_history():
    """Demonstrate workflow history tracking."""
    print("\n" + "="*60)
    print("DEMO: Workflow History")
    print("="*60 + "\n")
    
    config = {
        'publisher': {
            'output_dir': 'examples/output'
        }
    }
    
    editor = EditorAgent(config)
    
    # Run multiple workflows
    print("Running multiple workflow executions...\n")
    for i in range(2):
        print(f"Execution {i+1}:")
        editor.orchestrate_blog_creation()
        print()
    
    # Display history
    print(editor.get_workflow_summary())


def main():
    """Run all demos."""
    print("\n" + "="*70)
    print(" "*15 + "AGENTIC BLOG BIRD DEMO")
    print(" "*10 + "Multi-Agent Blog Post Generation System")
    print("="*70)
    
    # Demo 1: Individual agents
    demo_individual_agents()
    
    # Demo 2: Full workflow
    demo_full_workflow()
    
    # Demo 3: Workflow history
    demo_workflow_history()
    
    print("\n" + "="*70)
    print("Demo completed! Check the examples/output directory for generated posts.")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
