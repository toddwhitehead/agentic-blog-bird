#!/usr/bin/env python3
"""
Example script demonstrating the Agentic Blog Bird system.

This script shows how to use the multi-agent system to generate
blog posts from bird detection events using Microsoft Agent Framework
on Azure AI Foundry.
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
    print("Testing data source (Azure Blob Storage or local sample-data)...")
    researcher = ResearcherAgent()
    
    # List available data files
    data_files = researcher.list_data_files()
    print(f"Found {len(data_files)} data files:")
    for file in data_files[:3]:  # Show first 3 files
        print(f"  - {file}")
    if len(data_files) > 3:
        print(f"  ... and {len(data_files) - 3} more")
    print()
    
    # Generate research summary
    if data_files:
        print(f"Generating research summary for: {data_files[0]}")
        research_summary = researcher.generate_research_summary_for_file(data_files[0])
        print(research_summary[:400] + "...\n")
    else:
        print("No data files available for analysis.\n")
    
    # CopyWriter Agent Demo
    print("2. CopyWriter Agent Demo")
    print("-" * 60)
    copywriter = CopyWriterAgent()
    if data_files:
        blog_post = copywriter.generate_blog_post(research_summary)
        print(f"Headline: {blog_post['headline']}")
        print(f"Content length: {len(blog_post['full_content'])} characters\n")
    else:
        print("Skipping (no research data available)\n")
    
    # Publisher Agent Demo
    print("3. Publisher Agent Demo")
    print("-" * 60)
    publisher = PublisherAgent({'output_dir': 'examples/output'})
    if data_files:
        frontmatter = publisher.create_frontmatter(blog_post)
        print("Front matter preview:")
        print(frontmatter[:200] + "...\n")
    else:
        print("Skipping (no blog post data available)\n")


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
    print(" "*8 + "Powered by Microsoft Agent Framework")
    print(" "*12 + "on Azure AI Foundry")
    print("="*70)
    
    print("\n" + "INFO: This demo can run with or without Azure credentials.")
    print("INFO: When Azure Blob Storage is not configured, the system")
    print("INFO: automatically uses sample bird event data from the")
    print("INFO: 'sample-data' folder for demonstration purposes.")
    print()
    
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
