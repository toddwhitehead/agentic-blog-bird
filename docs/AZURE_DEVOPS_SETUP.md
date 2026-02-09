# Azure DevOps Git Integration Setup Guide

This guide explains how to set up and use the CommitterAgent to automatically commit Hugo markdown blog posts to an Azure DevOps Git repository.

## Overview

The CommitterAgent is an optional agent in the Agentic Blog Bird system that automatically commits generated Hugo markdown files to an Azure DevOps Git repository. This enables seamless integration with CI/CD pipelines for automated blog deployment.

## Prerequisites

1. **Azure DevOps Account**: You need an Azure DevOps organization and project
2. **Git Repository**: A Git repository in your Azure DevOps project for storing blog posts
3. **Personal Access Token (PAT)**: A PAT with repository write permissions
4. **Git**: Git must be installed on the system running the agent

## Step 1: Create Azure DevOps Personal Access Token

1. Log in to your Azure DevOps organization: `https://dev.azure.com/{your-organization}`
2. Click on your profile icon (top right) → **Personal access tokens**
3. Click **+ New Token**
4. Configure the token:
   - **Name**: "Agentic Blog Bird Committer"
   - **Organization**: Select your organization
   - **Expiration**: Choose an appropriate expiration date (90 days or custom)
   - **Scopes**: Select **Custom defined**, then:
     - ✅ **Code** → **Read & Write**
5. Click **Create**
6. **Important**: Copy the token immediately - you won't be able to see it again!

## Step 2: Configure Environment Variables

Add the Azure DevOps Personal Access Token to your `.env` file:

```bash
# Azure DevOps Git Configuration (Committer Agent)
AZURE_DEVOPS_PAT=your_personal_access_token_here
```

Example `.env` file:
```bash
# Required for CommitterAgent
AZURE_DEVOPS_PAT=abcdef1234567890abcdef1234567890abcdef1234567890

# Other environment variables...
AZURE_AI_PROJECT_CONNECTION_STRING=...
AZURE_STORAGE_CONNECTION_STRING=...
```

## Step 3: Configure Repository Settings

Edit `config/config.yaml` to specify your Azure DevOps repository:

```yaml
# Committer Agent Configuration
committer:
  # Azure DevOps Git settings
  azure_devops_repo_url: "https://dev.azure.com/{organization}/{project}/_git/{repository}"
  repo_path: "content/posts"  # Path within the repository
  branch: "main"  # Target branch
  
  # Git author information
  author_name: "Backyard Bird AI"
  author_email: "ai@backyardbird.com"
  
  # Committer options
  enable_auto_commit: true  # Set to false to disable auto-commit
  commit_message_template: "Add blog post: {filename}"
```

### Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `azure_devops_repo_url` | Full URL to your Azure DevOps Git repository | `https://dev.azure.com/myorg/myblog/_git/blog-content` |
| `repo_path` | Directory path within the repository where posts should be committed | `content/posts` or `hugo/content/posts` |
| `branch` | Target branch for commits | `main`, `master`, or `develop` |
| `author_name` | Git commit author name | `Backyard Bird AI` |
| `author_email` | Git commit author email | `ai@backyardbird.com` |
| `enable_auto_commit` | Enable/disable automatic commits | `true` or `false` |

## Step 4: Test the Configuration

Use the provided test script to verify your configuration:

```bash
python examples/test_committer.py
```

Expected output with valid configuration:
```
============================================================
CommitterAgent Test Script
============================================================

1. Initializing CommitterAgent...
   ✓ Agent: Committer
   ✓ Repo URL: https://dev.azure.com/myorg/myproject/_git/myrepo
   ✓ Target path: content/posts
   ✓ Branch: main

2. Validating configuration...
   ✓ Configuration is valid

3. Creating test Hugo markdown file...
   ✓ Created: /tmp/test-post-xxx.md

4. Committing to Azure DevOps repository...
   Status: completed
   ✓ Successfully committed to Azure DevOps!
   Commit SHA: abc1234def567890
   Target path: content/posts/test-post-xxx.md
   Message: Test commit from CommitterAgent - 2024-01-15 10:30:00

5. Cleaned up test file: /tmp/test-post-xxx.md

============================================================
Test completed
============================================================
```

## Step 5: Run the Full Workflow

Generate and commit a blog post:

```bash
# Generate blog post for today and commit to Azure DevOps
python main.py

# Generate blog post for a specific date
python main.py --date 2024-01-15
```

The workflow will:
1. Research bird detection data
2. Create engaging blog content
3. Generate cartoon-style images
4. Format as Hugo markdown
5. **Commit to Azure DevOps Git repository** (NEW!)

## Workflow Steps

The CommitterAgent adds Step 8 to the existing workflow:

```
Step 1: Research Phase
Step 2: Review Research
Step 3: Content Creation Phase
Step 4: Editorial Review
Step 5: Image Generation Phase
Step 6: Publishing Phase
Step 7: Final Validation
Step 8: Commit to Azure DevOps ← NEW!
```

## Troubleshooting

### Error: "Azure DevOps Personal Access Token not found"

**Solution**: Ensure `AZURE_DEVOPS_PAT` is set in your `.env` file

```bash
# Check if environment variable is set
echo $AZURE_DEVOPS_PAT

# If empty, add it to .env file
echo "AZURE_DEVOPS_PAT=your_token_here" >> config/.env
```

### Error: "Failed to clone repository: authentication required"

**Solutions**:
1. Verify your PAT has **Code (Read & Write)** permissions
2. Check that your PAT hasn't expired
3. Ensure the repository URL is correct
4. Test authentication manually:
   ```bash
   git clone https://{PAT}@dev.azure.com/{org}/{project}/_git/{repo}
   ```

### Error: "Failed to push: remote rejected"

**Solutions**:
1. Ensure the branch exists in the remote repository
2. Check that you have write permissions to the branch
3. Verify branch policies allow direct pushes (or use pull requests)
4. Check repository size limits

### Commit Skipped: "No changes to commit"

This means the file already exists in the repository with the same content. This is expected behavior and not an error.

## Disabling Auto-Commit

To disable automatic commits (e.g., for testing), set `enable_auto_commit` to `false` in `config/config.yaml`:

```yaml
committer:
  enable_auto_commit: false
```

The agent will still publish the Hugo markdown file locally but won't commit it to Azure DevOps.

## Security Best Practices

1. **Never commit your PAT to source control**
   - Always use environment variables or secure vaults
   - Add `.env` to your `.gitignore` file

2. **Use minimal PAT permissions**
   - Only grant **Code (Read & Write)** permissions
   - Don't grant unnecessary scopes

3. **Rotate PATs regularly**
   - Set reasonable expiration dates (90 days recommended)
   - Rotate tokens before they expire

4. **Use service accounts for automation**
   - Consider using a dedicated service account for the agent
   - Don't use personal user accounts in production

## Advanced Configuration

### Using a Different Branch

To commit to a branch other than `main`:

```yaml
committer:
  branch: "blog-posts"  # or "develop", "staging", etc.
```

### Custom Commit Messages

The commit message includes the blog post headline by default. You can customize the format:

```python
# In your custom code
commit_message = f"New post: {blog_post['headline']} [automated]"
result = committer.commit_post(markdown_path, commit_message)
```

### Commit to Subdirectories

Organize posts in subdirectories by date:

```yaml
committer:
  repo_path: "content/posts/2024/01"  # Posts organized by year/month
```

## CI/CD Integration

Once posts are committed to Azure DevOps, you can trigger automated builds:

1. **Azure Pipelines**: Set up a pipeline to build and deploy Hugo site
2. **GitHub Actions**: Mirror the repo to GitHub and use Actions
3. **Manual Deployment**: Pull changes and run Hugo locally

Example Azure Pipeline trigger:

```yaml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - content/posts/*
```

## Support and Troubleshooting

For additional help:
1. Check the [Azure DevOps Git Documentation](https://docs.microsoft.com/en-us/azure/devops/repos/git/)
2. Review the CommitterAgent source code: `src/agents/committer.py`
3. Run the test script with verbose output for debugging
4. Check git logs in the temporary directory during operations

## Summary

The CommitterAgent enables seamless integration between the Agentic Blog Bird multi-agent system and Azure DevOps Git repositories. By following this guide, you can automate the entire workflow from bird detection data to published blog posts in your repository.
