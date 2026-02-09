"""
Test script for CommitterAgent

This script demonstrates the CommitterAgent functionality for committing
Hugo markdown files to an Azure DevOps Git repository.

Prerequisites:
- Azure DevOps repository URL configured
- AZURE_DEVOPS_PAT environment variable set with a Personal Access Token
- Git installed on the system

Usage:
    python examples/test_committer.py
"""

import os
import sys
import tempfile
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.committer import CommitterAgent


def create_test_markdown_file():
    """Create a test Hugo markdown file."""
    # Hugo expects RFC3339 format for dates
    now = datetime.now()
    hugo_date = now.strftime('%Y-%m-%dT%H:%M:%S-00:00')  # Using UTC offset
    
    content = f"""---
title: "Test Blog Post"
date: {hugo_date}
draft: false
author: "Backyard Bird AI"
description: "A test blog post for CommitterAgent"
tags: ["test", "demo"]
categories: ["Testing"]
---

# Test Blog Post

This is a test blog post created to demonstrate the CommitterAgent functionality.

## Features

- Automatic git operations
- Azure DevOps integration
- Hugo markdown support

Generated at: {now.strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.md',
        prefix='test-post-',
        delete=False
    )
    temp_file.write(content)
    temp_file.close()
    
    return temp_file.name


def main():
    """Main test function."""
    print("="*60)
    print("CommitterAgent Test Script")
    print("="*60 + "\n")
    
    # Configuration
    config = {
        'azure_devops_repo_url': os.getenv(
            'AZURE_DEVOPS_REPO_URL',
            'https://dev.azure.com/myorg/myproject/_git/myrepo'
        ),
        'repo_path': 'content/posts',
        'branch': 'main',
        'author_name': 'Backyard Bird AI',
        'author_email': 'ai@backyardbird.com'
    }
    
    # Initialize CommitterAgent
    print("1. Initializing CommitterAgent...")
    agent = CommitterAgent(config)
    print(f"   ✓ Agent: {agent.name}")
    print(f"   ✓ Repo URL: {config['azure_devops_repo_url']}")
    print(f"   ✓ Target path: {config['repo_path']}")
    print(f"   ✓ Branch: {config['branch']}\n")
    
    # Validate configuration
    print("2. Validating configuration...")
    validation = agent.validate_configuration()
    print(f"   Configuration valid: {validation['valid']}")
    
    if validation['errors']:
        print("   Errors:")
        for error in validation['errors']:
            print(f"     - {error}")
    
    if validation['warnings']:
        print("   Warnings:")
        for warning in validation['warnings']:
            print(f"     - {warning}")
    
    if not validation['valid']:
        print("\n❌ Configuration is invalid. Please fix the errors above.")
        print("\nRequired environment variables:")
        print("  - AZURE_DEVOPS_PAT: Personal Access Token for Azure DevOps")
        print("\nOptional environment variables:")
        print("  - AZURE_DEVOPS_REPO_URL: Override default repository URL")
        return 1
    
    print("   ✓ Configuration is valid\n")
    
    # Create test markdown file
    print("3. Creating test Hugo markdown file...")
    test_file = create_test_markdown_file()
    print(f"   ✓ Created: {test_file}\n")
    
    try:
        # Commit the file
        print("4. Committing to Azure DevOps repository...")
        commit_message = f"Test commit from CommitterAgent - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        result = agent.commit_post(test_file, commit_message)
        
        print(f"   Status: {result['status']}")
        
        if result['status'] == 'completed':
            print("   ✓ Successfully committed to Azure DevOps!")
            print(f"   Commit SHA: {result.get('commit_sha', 'N/A')}")
            print(f"   Target path: {result.get('target_path', 'N/A')}")
            print(f"   Message: {result.get('commit_message', 'N/A')}")
        elif result['status'] == 'skipped':
            print("   ⚠ Commit skipped")
            for warning in result.get('warnings', []):
                print(f"     - {warning}")
        else:
            print("   ❌ Commit failed")
            for error in result.get('errors', []):
                print(f"     - {error}")
        
    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\n5. Cleaned up test file: {test_file}")
    
    print("\n" + "="*60)
    print("Test completed")
    print("="*60)
    
    return 0 if result['status'] == 'completed' else 1


if __name__ == '__main__':
    sys.exit(main())
