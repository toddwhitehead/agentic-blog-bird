"""
Committer Agent Module

This agent is responsible for committing Hugo markdown files to a GitHub git repository.
"""

import os
import subprocess
import tempfile
import shutil
from typing import Dict, Any, Optional
from .base_agent import BaseAgent


class CommitterAgent(BaseAgent):
    """
    Committer agent that commits Hugo markdown files to GitHub git repository.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Committer agent.
        
        Args:
            config: Configuration dictionary for GitHub git settings
        """
        super().__init__(name="Committer", config=config)
        
        # GitHub Git configuration
        self.repo_url = self.config.get('github_repo_url', '')
        self.repo_path = self.config.get('repo_path', 'content/posts')
        self.personal_access_token = os.getenv('GITHUB_TOKEN', '')
        self.author_name = self.config.get('author_name', 'Backyard Bird AI')
        self.author_email = self.config.get('author_email', 'ai@backyardbird.com')
        self.branch = self.config.get('branch', 'main')
        
        self._initialize_agent_client()
        
    def get_system_message(self) -> str:
        """Return the system message for the committer agent."""
        return """You are a Committer agent specialized in managing git operations for GitHub.

Your responsibilities:
1. Clone or access GitHub git repositories
2. Commit Hugo markdown files to the repository
3. Push changes to the remote repository
4. Handle authentication with GitHub
5. Manage commit messages and metadata
6. Ensure proper file organization in the repository
7. Handle git conflicts and errors gracefully

Git operation requirements:
- Use Personal Access Token (PAT) for authentication
- Create meaningful commit messages
- Organize files in the correct directory structure
- Handle images and other assets alongside markdown files
- Ensure proper git configuration (author, email)
- Push changes to the specified branch
- Validate successful push operations

You work with Hugo-formatted markdown files and ensure they are properly
committed to the GitHub repository for CI/CD pipeline processing.
"""
    
    def commit_post(self, markdown_path: str, commit_message: str = None) -> Dict[str, Any]:
        """
        Commit a Hugo markdown file to GitHub git repository.
        
        Args:
            markdown_path: Path to the Hugo markdown file to commit
            commit_message: Custom commit message (optional)
            
        Returns:
            Dictionary containing commit operation results
        """
        result = {
            "status": "started",
            "markdown_path": markdown_path,
            "errors": [],
            "warnings": []
        }
        
        # Validate inputs
        if not self.repo_url:
            result["status"] = "failed"
            result["errors"].append("GitHub repository URL not configured")
            return result
        
        if not self.personal_access_token:
            result["status"] = "failed"
            result["errors"].append("GitHub Personal Access Token not found in environment")
            return result
        
        if not os.path.exists(markdown_path):
            result["status"] = "failed"
            result["errors"].append(f"Markdown file not found: {markdown_path}")
            return result
        
        try:
            # Create temporary directory for git operations
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Committer: Using temporary directory: {temp_dir}")
                
                # Clone the repository
                print(f"Committer: Cloning repository from {self.repo_url}")
                clone_result = self._clone_repository(temp_dir)
                
                if not clone_result["success"]:
                    result["status"] = "failed"
                    result["errors"].append(f"Failed to clone repository: {clone_result.get('error')}")
                    return result
                
                repo_dir = clone_result["repo_dir"]
                
                # Copy the markdown file to the repository
                print(f"Committer: Copying markdown file to repository")
                copy_result = self._copy_file_to_repo(markdown_path, repo_dir)
                
                if not copy_result["success"]:
                    result["status"] = "failed"
                    result["errors"].append(f"Failed to copy file: {copy_result.get('error')}")
                    return result
                
                # Add the file to git
                print(f"Committer: Adding file to git")
                add_result = self._git_add(repo_dir, copy_result["target_path"])
                
                if not add_result["success"]:
                    result["status"] = "failed"
                    result["errors"].append(f"Failed to add file to git: {add_result.get('error')}")
                    return result
                
                # Commit the changes
                if commit_message is None:
                    filename = os.path.basename(markdown_path)
                    commit_message = f"Add blog post: {filename}"
                
                print(f"Committer: Committing changes with message: {commit_message}")
                commit_result = self._git_commit(repo_dir, commit_message)
                
                if not commit_result["success"]:
                    # Check if there are no changes to commit
                    if "nothing to commit" in commit_result.get("message", "").lower():
                        result["status"] = "skipped"
                        result["warnings"].append("No changes to commit (file may already exist)")
                        return result
                    
                    result["status"] = "failed"
                    result["errors"].append(f"Failed to commit: {commit_result.get('error')}")
                    return result
                
                # Push to remote
                print(f"Committer: Pushing changes to remote repository")
                push_result = self._git_push(repo_dir)
                
                if not push_result["success"]:
                    result["status"] = "failed"
                    result["errors"].append(f"Failed to push: {push_result.get('error')}")
                    return result
                
                result["status"] = "completed"
                result["commit_sha"] = commit_result.get("commit_sha")
                result["target_path"] = copy_result["target_path"]
                result["commit_message"] = commit_message
                
                print(f"Committer: Successfully committed and pushed to GitHub")
                
        except Exception as e:
            result["status"] = "failed"
            result["errors"].append(f"Unexpected error: {str(e)}")
        
        return result
    
    def _clone_repository(self, target_dir: str) -> Dict[str, Any]:
        """
        Clone the GitHub repository.
        
        Args:
            target_dir: Directory to clone into
            
        Returns:
            Dictionary with clone operation results
        """
        result = {"success": False}
        
        try:
            # Construct authenticated URL
            auth_url = self._get_authenticated_url()
            
            # Clone command
            clone_dir = os.path.join(target_dir, "repo")
            cmd = ["git", "clone", auth_url, clone_dir]
            
            # Execute clone
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if process.returncode == 0:
                result["success"] = True
                result["repo_dir"] = clone_dir
            else:
                result["error"] = process.stderr or process.stdout
                
        except subprocess.TimeoutExpired:
            result["error"] = "Clone operation timed out"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _copy_file_to_repo(self, source_path: str, repo_dir: str) -> Dict[str, Any]:
        """
        Copy markdown file to the repository directory.
        
        Args:
            source_path: Source markdown file path
            repo_dir: Repository directory
            
        Returns:
            Dictionary with copy operation results
        """
        result = {"success": False}
        
        try:
            # Create target directory if needed
            target_dir = os.path.join(repo_dir, self.repo_path)
            os.makedirs(target_dir, exist_ok=True)
            
            # Determine target filename
            filename = os.path.basename(source_path)
            target_path = os.path.join(target_dir, filename)
            
            # Copy the file
            shutil.copy2(source_path, target_path)
            
            result["success"] = True
            result["target_path"] = os.path.join(self.repo_path, filename)
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _git_add(self, repo_dir: str, file_path: str) -> Dict[str, Any]:
        """
        Add file to git staging.
        
        Args:
            repo_dir: Repository directory
            file_path: Relative file path to add
            
        Returns:
            Dictionary with add operation results
        """
        result = {"success": False}
        
        try:
            cmd = ["git", "add", file_path]
            
            process = subprocess.run(
                cmd,
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if process.returncode == 0:
                result["success"] = True
            else:
                result["error"] = process.stderr or process.stdout
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _git_commit(self, repo_dir: str, message: str) -> Dict[str, Any]:
        """
        Commit staged changes.
        
        Args:
            repo_dir: Repository directory
            message: Commit message
            
        Returns:
            Dictionary with commit operation results
        """
        result = {"success": False}
        
        try:
            # Set git user config
            subprocess.run(
                ["git", "config", "user.name", self.author_name],
                cwd=repo_dir,
                capture_output=True,
                timeout=10
            )
            subprocess.run(
                ["git", "config", "user.email", self.author_email],
                cwd=repo_dir,
                capture_output=True,
                timeout=10
            )
            
            # Commit
            cmd = ["git", "commit", "-m", message]
            
            process = subprocess.run(
                cmd,
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if process.returncode == 0:
                result["success"] = True
                result["message"] = process.stdout
                
                # Get commit SHA using rev-parse for reliability
                try:
                    sha_process = subprocess.run(
                        ["git", "rev-parse", "HEAD"],
                        cwd=repo_dir,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if sha_process.returncode == 0:
                        result["commit_sha"] = sha_process.stdout.strip()
                except Exception:
                    # If we can't get the SHA, it's not critical
                    pass
            else:
                result["error"] = process.stderr or process.stdout
                result["message"] = process.stdout
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _git_push(self, repo_dir: str) -> Dict[str, Any]:
        """
        Push commits to remote repository.
        
        Args:
            repo_dir: Repository directory
            
        Returns:
            Dictionary with push operation results
        """
        result = {"success": False}
        
        try:
            cmd = ["git", "push", "origin", self.branch]
            
            process = subprocess.run(
                cmd,
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if process.returncode == 0:
                result["success"] = True
                result["output"] = process.stdout
            else:
                result["error"] = process.stderr or process.stdout
                
        except subprocess.TimeoutExpired:
            result["error"] = "Push operation timed out"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _get_authenticated_url(self) -> str:
        """
        Get repository URL with embedded authentication.
        
        Returns:
            Authenticated repository URL
        """
        # GitHub URL format with PAT
        # https://{PAT}@github.com/{owner}/{repository}
        
        if '@' in self.repo_url:
            # URL already has authentication
            return self.repo_url
        
        # Insert PAT into URL
        if self.repo_url.startswith('https://'):
            # Replace https:// with https://{PAT}@
            auth_url = self.repo_url.replace('https://', f'https://{self.personal_access_token}@')
            return auth_url
        
        return self.repo_url
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate committer configuration.
        
        Returns:
            Dictionary containing validation results
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        if not self.repo_url:
            validation["valid"] = False
            validation["errors"].append("GitHub repository URL not configured")
        
        if not self.personal_access_token:
            validation["valid"] = False
            validation["errors"].append("GitHub Personal Access Token not found")
        
        if not self.author_name:
            validation["warnings"].append("Author name not configured (using default)")
        
        if not self.author_email:
            validation["warnings"].append("Author email not configured (using default)")
        
        return validation
