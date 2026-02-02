"""
Demo script showing how to use the DeliveryAgent to deploy blog posts to Azure Static Web Apps.

This script demonstrates:
1. Initializing the DeliveryAgent with configuration
2. Creating a sample blog post
3. Delivering the blog post to a git repository
4. Triggering Azure Static Web Apps deployment

Prerequisites:
- Git installed on the system
- Valid git repository URL with push access
- Azure Static Web App configured to watch the repository
"""

import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.delivery import DeliveryAgent
from agents.publisher import PublisherAgent


def create_sample_blog_post():
    """Create a sample blog post for demonstration."""
    print("\n" + "="*60)
    print("Creating Sample Blog Post")
    print("="*60 + "\n")
    
    # Initialize publisher agent
    publisher_config = {
        'output_dir': 'content/posts'
    }
    publisher = PublisherAgent(publisher_config)
    
    # Create sample blog post data
    post_data = {
        'headline': 'A Day in the Life of Backyard Birds',
        'date': datetime.now().isoformat(),
        'author': 'Backyard Bird AI',
        'description': 'Daily highlights from our backyard bird monitoring system',
        'tags': ['birds', 'wildlife', 'backyard', 'AI monitoring'],
        'categories': ['Daily Updates'],
        'introduction': 'Today was an exciting day in our backyard!',
        'body': '''## Morning Activity

The morning started with a flurry of activity as several Blue Jays visited the feeder. 
Their vibrant blue plumage caught the morning sun beautifully.

## Afternoon Visitors

In the afternoon, we spotted a pair of Cardinals. The male's bright red color 
was particularly striking against the green foliage.

## Evening Wrap-up

As the day drew to a close, a family of Sparrows came by for their evening meal. 
It's always heartwarming to see them together.''',
        'conclusion': 'Another wonderful day of observing our feathered friends!',
        'full_content': '''## Morning Activity

The morning started with a flurry of activity as several Blue Jays visited the feeder. 
Their vibrant blue plumage caught the morning sun beautifully.

## Afternoon Visitors

In the afternoon, we spotted a pair of Cardinals. The male's bright red color 
was particularly striking against the green foliage.

## Evening Wrap-up

As the day drew to a close, a family of Sparrows came by for their evening meal. 
It's always heartwarming to see them together.

Another wonderful day of observing our feathered friends!'''
    }
    
    # Publish the blog post
    output_path = publisher.publish_post(post_data)
    
    print(f"✓ Sample blog post created: {output_path}")
    
    # Validate the output
    validation = publisher.validate_hugo_format(output_path)
    if validation['valid']:
        print("✓ Blog post is valid Hugo format")
    else:
        print("✗ Blog post validation failed:")
        for error in validation['errors']:
            print(f"  - {error}")
    
    return output_path, post_data


def demo_delivery_agent():
    """Demonstrate the DeliveryAgent functionality."""
    print("\n" + "="*60)
    print("DeliveryAgent Demo")
    print("Deploying Blog Posts to Azure Static Web Apps")
    print("="*60)
    
    # Configuration for the DeliveryAgent
    # NOTE: Replace with your actual repository URL and credentials
    delivery_config = {
        'target_repo_url': os.getenv('BLOG_REPO_URL', 'https://github.com/yourusername/your-hugo-blog.git'),
        'target_repo_branch': os.getenv('BLOG_REPO_BRANCH', 'main'),
        'target_repo_path': '/tmp/demo-blog-delivery-repo',
        'content_subdir': 'content/posts',
        'images_subdir': 'content/posts/images',
        'git_user_name': os.getenv('GIT_USER_NAME', 'Blog Bird Agent'),
        'git_user_email': os.getenv('GIT_USER_EMAIL', 'blogbird@example.com'),
        'commit_message_template': 'Add blog post: {title}',
    }
    
    print("\n1. Initializing DeliveryAgent...")
    print(f"   Target repository: {delivery_config['target_repo_url']}")
    print(f"   Branch: {delivery_config['target_repo_branch']}")
    
    delivery_agent = DeliveryAgent(delivery_config)
    
    # Validate configuration
    print("\n2. Validating configuration...")
    validation = delivery_agent.validate_configuration()
    
    if not validation['valid']:
        print("✗ Configuration validation failed:")
        for error in validation['errors']:
            print(f"  - {error}")
        print("\nTo use this demo:")
        print("1. Set BLOG_REPO_URL environment variable to your git repository")
        print("2. Ensure you have git credentials configured")
        print("3. Configure Azure Static Web App to watch your repository")
        return 1
    
    print("✓ Configuration is valid")
    if validation.get('git_version'):
        print(f"  Git version: {validation['git_version']}")
    
    # Create a sample blog post
    print("\n3. Creating sample blog post...")
    post_path, post_data = create_sample_blog_post()
    
    # Check if we should actually deliver (only if repo URL is configured)
    if delivery_config['target_repo_url'] == 'https://github.com/yourusername/your-hugo-blog.git':
        print("\n" + "="*60)
        print("Demo Complete (Dry Run)")
        print("="*60)
        print("\nTo enable actual delivery:")
        print("1. Configure your git repository URL:")
        print("   export BLOG_REPO_URL='https://github.com/yourusername/your-hugo-blog.git'")
        print("\n2. Set up git authentication (SSH key or HTTPS credentials)")
        print("\n3. Create an Azure Static Web App:")
        print("   - Go to Azure Portal")
        print("   - Create a Static Web App")
        print("   - Connect it to your git repository")
        print("   - Configure build settings for Hugo")
        print("\n4. Run this demo again")
        print("\nBlog post created at: " + post_path)
        return 0
    
    # Deliver the blog post
    print("\n4. Delivering blog post to repository...")
    post_metadata = {
        'headline': post_data['headline'],
        'featured_image': post_data.get('featured_image')
    }
    
    delivery_result = delivery_agent.deliver_blog_post(post_path, post_metadata)
    
    if delivery_result['status'] == 'completed':
        print("\n" + "="*60)
        print("✓ Blog Post Delivered Successfully!")
        print("="*60)
        print(f"\nPost file: {post_path}")
        print(f"Repository: {delivery_config['target_repo_url']}")
        print(f"Branch: {delivery_config['target_repo_branch']}")
        print("\nAzure Static Web App will automatically:")
        print("1. Detect the git push")
        print("2. Build your Hugo site")
        print("3. Deploy to production")
        print("\nCheck your Azure Static Web App for the deployment status.")
        return 0
    else:
        print("\n✗ Delivery failed:")
        for error in delivery_result.get('errors', []):
            print(f"  - {error}")
        return 1


def main():
    """Main entry point."""
    print("\n" + "="*70)
    print(" "*15 + "Agentic Blog Bird - Delivery Agent Demo")
    print(" "*10 + "Deploy Hugo Blog Posts to Azure Static Web Apps")
    print("="*70)
    
    try:
        return demo_delivery_agent()
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
