"""
Delivery Agent Module

This agent is responsible for delivering Hugo-formatted blog posts to a git repository
that will trigger automatic deployment to an Azure Static Web App.
"""

import os
import subprocess
import shutil
from typing import Dict, Any, Optional
from datetime import datetime
from .base_agent import BaseAgent


class DeliveryAgent(BaseAgent):
    """
    Delivery agent that pushes Hugo-formatted blog posts to a git repository
    for automatic deployment to Azure Static Web Apps.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Delivery agent.
        
        Args:
            config: Configuration dictionary for git repository settings and deployment
        """
        super().__init__(name="Delivery", config=config)
        self.target_repo_url = self.config.get('target_repo_url', '')
        self.target_repo_branch = self.config.get('target_repo_branch', 'main')
        self.target_repo_path = self.config.get('target_repo_path', '/tmp/blog-delivery-repo')
        self.content_subdir = self.config.get('content_subdir', 'content/posts')
        self.images_subdir = self.config.get('images_subdir', 'content/posts/images')
        self.git_user_name = self.config.get('git_user_name', 'Blog Bird Agent')
        self.git_user_email = self.config.get('git_user_email', 'blogbird@example.com')
        self.commit_message_template = self.config.get('commit_message_template', 
                                                       'Add blog post: {title}')
        self._initialize_agent_client()
        
    def get_system_message(self) -> str:
        """Return the system message for the delivery agent."""
        return """You are a Delivery agent specialized in deploying Hugo-formatted blog posts 
to git repositories for automatic publication to Azure Static Web Apps.

Your responsibilities:
1. Manage git repository operations (clone, pull, add, commit, push)
2. Copy blog post files to the appropriate directories in the target repository
3. Handle both markdown content files and image assets
4. Ensure proper git configuration for automated commits
5. Trigger Azure Static Web Apps deployment through git push
6. Validate successful delivery and provide status reports
7. Handle errors gracefully (authentication, network issues, conflicts)

Git workflow:
- Clone or update the target repository
- Copy new blog post files to the appropriate locations
- Stage all changes (content and images)
- Commit with a descriptive message
- Push to trigger Azure Static Web Apps deployment

Azure Static Web Apps integration:
- Pushing to the configured branch automatically triggers a build and deployment
- The Static Web App should be configured to detect Hugo site structure
- Build configuration should be set in the Azure portal or staticwebapp.config.json

Error handling:
- Provide clear error messages for git operations
- Report authentication failures
- Handle merge conflicts gracefully
- Validate file operations before committing
"""
    
    def _run_git_command(self, command: list, cwd: str = None) -> Dict[str, Any]:
        """
        Run a git command and return the result.
        
        Args:
            command: Git command as list of strings
            cwd: Working directory for the command
            
        Returns:
            Dictionary with success status, output, and error messages
        """
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.target_repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "error": result.stderr.strip(),
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }
    
    def _ensure_repo_ready(self) -> Dict[str, Any]:
        """
        Ensure the target repository is cloned and up to date.
        
        Returns:
            Dictionary with success status and messages
        """
        result = {
            "success": False,
            "message": "",
            "action": ""
        }
        
        # Check if repository already exists
        if os.path.exists(self.target_repo_path) and os.path.exists(
            os.path.join(self.target_repo_path, '.git')
        ):
            # Repository exists, pull latest changes
            print(f"Delivery: Updating existing repository at {self.target_repo_path}")
            
            # Fetch latest changes
            fetch_result = self._run_git_command(['git', 'fetch', 'origin'])
            if not fetch_result['success']:
                result['message'] = f"Failed to fetch: {fetch_result['error']}"
                return result
            
            # Pull latest changes
            pull_result = self._run_git_command([
                'git', 'pull', 'origin', self.target_repo_branch
            ])
            if not pull_result['success']:
                result['message'] = f"Failed to pull: {pull_result['error']}"
                return result
            
            result['success'] = True
            result['action'] = 'updated'
            result['message'] = 'Repository updated successfully'
            
        else:
            # Repository doesn't exist, clone it
            print(f"Delivery: Cloning repository to {self.target_repo_path}")
            
            # Remove directory if it exists but is not a git repo
            if os.path.exists(self.target_repo_path):
                shutil.rmtree(self.target_repo_path)
            
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(self.target_repo_path), exist_ok=True)
            
            # Clone repository
            clone_result = self._run_git_command(
                ['git', 'clone', '-b', self.target_repo_branch, 
                 self.target_repo_url, self.target_repo_path],
                cwd=os.path.dirname(self.target_repo_path)
            )
            
            if not clone_result['success']:
                result['message'] = f"Failed to clone: {clone_result['error']}"
                return result
            
            result['success'] = True
            result['action'] = 'cloned'
            result['message'] = 'Repository cloned successfully'
        
        return result
    
    def _configure_git_identity(self) -> bool:
        """
        Configure git user identity for commits.
        
        Returns:
            True if configuration successful, False otherwise
        """
        # Configure user name
        name_result = self._run_git_command([
            'git', 'config', 'user.name', self.git_user_name
        ])
        
        # Configure user email
        email_result = self._run_git_command([
            'git', 'config', 'user.email', self.git_user_email
        ])
        
        return name_result['success'] and email_result['success']
    
    def _copy_blog_post_files(self, post_file_path: str, 
                              image_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Copy blog post files to the target repository.
        
        Args:
            post_file_path: Path to the blog post markdown file
            image_path: Optional path to the featured image
            
        Returns:
            Dictionary with copied file paths and status
        """
        result = {
            "success": False,
            "copied_files": [],
            "errors": []
        }
        
        # Create target directories if they don't exist
        target_content_dir = os.path.join(self.target_repo_path, self.content_subdir)
        target_images_dir = os.path.join(self.target_repo_path, self.images_subdir)
        
        os.makedirs(target_content_dir, exist_ok=True)
        os.makedirs(target_images_dir, exist_ok=True)
        
        # Copy blog post file
        if os.path.exists(post_file_path):
            filename = os.path.basename(post_file_path)
            target_post_path = os.path.join(target_content_dir, filename)
            
            try:
                shutil.copy2(post_file_path, target_post_path)
                result['copied_files'].append(target_post_path)
                print(f"Delivery: Copied blog post to {target_post_path}")
            except Exception as e:
                result['errors'].append(f"Failed to copy blog post: {str(e)}")
                return result
        else:
            result['errors'].append(f"Blog post file not found: {post_file_path}")
            return result
        
        # Copy image file if provided
        if image_path and os.path.exists(image_path):
            image_filename = os.path.basename(image_path)
            target_image_path = os.path.join(target_images_dir, image_filename)
            
            try:
                shutil.copy2(image_path, target_image_path)
                result['copied_files'].append(target_image_path)
                print(f"Delivery: Copied image to {target_image_path}")
            except Exception as e:
                result['errors'].append(f"Failed to copy image: {str(e)}")
                # Don't return here - image is optional
        
        result['success'] = True
        return result
    
    def deliver_blog_post(self, post_file_path: str, 
                          post_metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Deliver a blog post to the target git repository for deployment.
        
        Args:
            post_file_path: Path to the Hugo-formatted blog post markdown file
            post_metadata: Optional metadata about the post (title, images, etc.)
            
        Returns:
            Dictionary containing delivery status and details
        """
        delivery_result = {
            "status": "started",
            "post_file": post_file_path,
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "errors": []
        }
        
        print(f"\n{'='*60}")
        print(f"Delivery Agent: Starting blog post delivery")
        print(f"Post file: {post_file_path}")
        print(f"Target repository: {self.target_repo_url}")
        print(f"Target branch: {self.target_repo_branch}")
        print(f"{'='*60}\n")
        
        # Step 1: Ensure repository is ready
        print("Step 1: Preparing target repository")
        print("-" * 60)
        repo_result = self._ensure_repo_ready()
        delivery_result['steps'].append({
            "step": "prepare_repository",
            "status": "success" if repo_result['success'] else "failed",
            "action": repo_result.get('action', ''),
            "message": repo_result['message']
        })
        
        if not repo_result['success']:
            delivery_result['status'] = 'failed'
            delivery_result['errors'].append(repo_result['message'])
            return delivery_result
        
        # Step 2: Configure git identity
        print("\nStep 2: Configuring git identity")
        print("-" * 60)
        if not self._configure_git_identity():
            delivery_result['status'] = 'failed'
            delivery_result['errors'].append("Failed to configure git identity")
            return delivery_result
        print(f"Delivery: Configured git user as {self.git_user_name} <{self.git_user_email}>")
        delivery_result['steps'].append({
            "step": "configure_git",
            "status": "success"
        })
        
        # Step 3: Copy blog post files
        print("\nStep 3: Copying blog post files")
        print("-" * 60)
        image_path = post_metadata.get('featured_image') if post_metadata else None
        copy_result = self._copy_blog_post_files(post_file_path, image_path)
        delivery_result['steps'].append({
            "step": "copy_files",
            "status": "success" if copy_result['success'] else "failed",
            "files_copied": len(copy_result['copied_files']),
            "files": copy_result['copied_files']
        })
        
        if not copy_result['success']:
            delivery_result['status'] = 'failed'
            delivery_result['errors'].extend(copy_result['errors'])
            return delivery_result
        
        # Step 4: Stage changes
        print("\nStep 4: Staging changes")
        print("-" * 60)
        add_result = self._run_git_command(['git', 'add', '.'])
        delivery_result['steps'].append({
            "step": "stage_changes",
            "status": "success" if add_result['success'] else "failed"
        })
        
        if not add_result['success']:
            delivery_result['status'] = 'failed'
            delivery_result['errors'].append(f"Failed to stage changes: {add_result['error']}")
            return delivery_result
        print("Delivery: Changes staged successfully")
        
        # Step 5: Check if there are changes to commit
        status_result = self._run_git_command(['git', 'status', '--porcelain'])
        if not status_result['output']:
            print("Delivery: No changes to commit (files may already exist)")
            delivery_result['status'] = 'completed'
            delivery_result['message'] = 'No new changes to deploy'
            return delivery_result
        
        # Step 6: Commit changes
        print("\nStep 6: Committing changes")
        print("-" * 60)
        title = post_metadata.get('headline', 'New blog post') if post_metadata else 'New blog post'
        commit_message = self.commit_message_template.format(title=title)
        
        commit_result = self._run_git_command(['git', 'commit', '-m', commit_message])
        delivery_result['steps'].append({
            "step": "commit_changes",
            "status": "success" if commit_result['success'] else "failed",
            "commit_message": commit_message
        })
        
        if not commit_result['success']:
            delivery_result['status'] = 'failed'
            delivery_result['errors'].append(f"Failed to commit: {commit_result['error']}")
            return delivery_result
        print(f"Delivery: Changes committed: {commit_message}")
        
        # Step 7: Push to remote
        print("\nStep 7: Pushing to remote repository")
        print("-" * 60)
        push_result = self._run_git_command([
            'git', 'push', 'origin', self.target_repo_branch
        ])
        delivery_result['steps'].append({
            "step": "push_to_remote",
            "status": "success" if push_result['success'] else "failed",
            "branch": self.target_repo_branch
        })
        
        if not push_result['success']:
            delivery_result['status'] = 'failed'
            delivery_result['errors'].append(f"Failed to push: {push_result['error']}")
            return delivery_result
        
        print(f"Delivery: Successfully pushed to {self.target_repo_branch}")
        print("\nAzure Static Web App deployment should be triggered automatically")
        
        # Mark as completed
        delivery_result['status'] = 'completed'
        delivery_result['message'] = 'Blog post delivered successfully'
        delivery_result['deployment_triggered'] = True
        
        print(f"\n{'='*60}")
        print(f"Delivery Agent: Blog post delivered successfully!")
        print(f"Azure Static Web App deployment triggered")
        print(f"{'='*60}\n")
        
        return delivery_result
    
    def get_delivery_status(self) -> Dict[str, Any]:
        """
        Get the current status of the delivery repository.
        
        Returns:
            Dictionary with repository status information
        """
        if not os.path.exists(self.target_repo_path):
            return {
                "status": "not_initialized",
                "message": "Repository not cloned yet"
            }
        
        # Get current branch
        branch_result = self._run_git_command(['git', 'branch', '--show-current'])
        
        # Get last commit
        log_result = self._run_git_command([
            'git', 'log', '-1', '--pretty=format:%H|%an|%ae|%s|%ai'
        ])
        
        # Get status
        status_result = self._run_git_command(['git', 'status', '--porcelain'])
        
        status = {
            "status": "ready",
            "repository_path": self.target_repo_path,
            "current_branch": branch_result['output'],
            "has_uncommitted_changes": bool(status_result['output']),
        }
        
        if log_result['success'] and log_result['output']:
            parts = log_result['output'].split('|')
            if len(parts) == 5:
                status['last_commit'] = {
                    "hash": parts[0],
                    "author": parts[1],
                    "email": parts[2],
                    "message": parts[3],
                    "date": parts[4]
                }
        
        return status
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate the delivery agent configuration.
        
        Returns:
            Dictionary with validation results
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required configuration
        if not self.target_repo_url:
            validation['valid'] = False
            validation['errors'].append("target_repo_url is required")
        
        if not self.target_repo_branch:
            validation['warnings'].append("target_repo_branch not set, using 'main'")
        
        # Check git is available
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                check=True
            )
            if result.returncode == 0:
                validation['git_version'] = result.stdout.strip()
            else:
                validation['valid'] = False
                validation['errors'].append("Git is not available")
        except Exception as e:
            validation['valid'] = False
            validation['errors'].append(f"Git is not available: {str(e)}")
        
        return validation
