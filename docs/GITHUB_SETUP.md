# GitHub Git Integration Setup Guide

This guide explains how to set up and use the CommitterAgent to automatically commit Hugo markdown blog posts to a GitHub Git repository.

## Overview

The CommitterAgent is an optional agent in the Agentic Blog Bird system that automatically commits generated Hugo markdown files to a GitHub Git repository. This enables seamless integration with CI/CD pipelines for automated blog deployment.

## Prerequisites

1. **GitHub Account**: You need a GitHub account
2. **Git Repository**: A Git repository on GitHub for storing blog posts (e.g., https://github.com/toddwhitehead/acme-giyt-web)
3. **Personal Access Token (PAT)**: A PAT with repository write permissions
4. **Git**: Git must be installed on the system running the agent

## Step 1: Create GitHub Personal Access Token

1. Log in to your GitHub account: `https://github.com`
2. Click on your profile icon (top right) → **Settings**
3. Scroll down to **Developer settings** (bottom left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Configure the token:
   - **Note**: "Agentic Blog Bird Committer"
   - **Expiration**: Choose an appropriate expiration date (90 days or custom)
   - **Select scopes**:
     - ✅ **repo** (Full control of private repositories)
       - This includes repo:status, repo_deployment, public_repo, repo:invite, security_events
7. Click **Generate token**
8. **Important**: Copy the token immediately - you won't be able to see it again!

## Step 2: Configure Environment Variables

Add the GitHub Personal Access Token to your `.env` file:

```bash
# GitHub Configuration (Committer Agent)
GITHUB_TOKEN=your_personal_access_token_here

# Optional: Set the repository URL (can also be set in config.yaml)
GITHUB_REPO_URL=https://github.com/toddwhitehead/acme-giyt-web
```

Example `.env` file:
```bash
# Required for CommitterAgent
GITHUB_TOKEN=ghp_abcdef1234567890abcdef1234567890abcdef

# Repository URL (overrides config.yaml if set)
GITHUB_REPO_URL=https://github.com/toddwhitehead/acme-giyt-web

# Other environment variables...
AZURE_AI_PROJECT_CONNECTION_STRING=...
AZURE_STORAGE_CONNECTION_STRING=...
```

**Note**: You can set the repository URL either in the `.env` file (as `GITHUB_REPO_URL`) or in `config/config.yaml`. The environment variable takes precedence if both are set.

## Step 3: Configure Repository Settings

Edit `config/config.yaml` to specify your GitHub repository (if not using environment variable):

```yaml
# Committer Agent Configuration
committer:
  # GitHub Git settings
  github_repo_url: "https://github.com/{owner}/{repository}"
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
| `github_repo_url` | Full URL to your GitHub Git repository (can be overridden by `GITHUB_REPO_URL` env var) | `https://github.com/{owner}/{repository}` |
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
   ✓ Repo URL: https://github.com/toddwhitehead/acme-giyt-web
   ✓ Target path: content/posts
   ✓ Branch: main

2. Validating configuration...
   ✓ Configuration is valid

3. Creating test Hugo markdown file...
   ✓ Created: /tmp/test-post-xxx.md

4. Committing to GitHub repository...
   Status: completed
   ✓ Successfully committed to GitHub!
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
# Generate blog post for today and commit to GitHub
python main.py

# Generate blog post for a specific date
python main.py --date 2024-01-15
```

The workflow will:
1. Research bird detection data
2. Create engaging blog content
3. Generate cartoon-style images
4. Format as Hugo markdown
5. **Commit to GitHub Git repository** (NEW!)

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
Step 8: Commit to GitHub ← NEW!
```

## Troubleshooting

### Error: "GitHub Personal Access Token not found"

**Solution**: Ensure `GITHUB_TOKEN` is set in your `.env` file

```bash
# Check if environment variable is set
echo $GITHUB_TOKEN

# If empty, add it to .env file
echo "GITHUB_TOKEN=your_token_here" >> config/.env
```

### Error: "Failed to clone repository: authentication required"

**Solutions**:
1. Verify your PAT has **repo** permissions
2. Check that your PAT hasn't expired
3. Ensure the repository URL is correct
4. Test authentication manually:
   ```bash
   git clone https://{TOKEN}@github.com/{owner}/{repo}
   ```

### Error: "Failed to push: remote rejected"

**Solutions**:
1. Ensure the branch exists in the remote repository
2. Check that you have write permissions to the branch
3. Verify branch protection rules allow direct pushes (or use pull requests)
4. Check repository size limits

### Commit Skipped: "No changes to commit"

This means the file already exists in the repository with the same content. This is expected behavior and not an error.

## Disabling Auto-Commit

To disable automatic commits (e.g., for testing), set `enable_auto_commit` to `false` in `config/config.yaml`:

```yaml
committer:
  enable_auto_commit: false
```

The agent will still publish the Hugo markdown file locally but won't commit it to GitHub.

## Security Best Practices

1. **Never commit your PAT to source control**
   - Always use environment variables or secure vaults
   - Add `.env` to your `.gitignore` file

2. **Use minimal PAT permissions**
   - Only grant **repo** permissions for the specific repository
   - Don't grant unnecessary scopes

3. **Rotate PATs regularly**
   - Set reasonable expiration dates (90 days recommended)
   - Rotate tokens before they expire

4. **Use fine-grained tokens when possible**
   - GitHub offers fine-grained personal access tokens
   - These can be restricted to specific repositories

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

Once posts are committed to GitHub, you can trigger automated builds:

1. **GitHub Actions**: Set up a workflow to build and deploy Hugo site
2. **GitHub Pages**: Deploy directly from the repository
3. **Netlify/Vercel**: Connect your repository for automatic deployments

Example GitHub Actions workflow:

```yaml
name: Deploy Hugo Site

on:
  push:
    branches:
      - main
    paths:
      - 'content/posts/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
      - name: Build
        run: hugo --minify
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

## Support and Troubleshooting

For additional help:
1. Check the [GitHub Documentation](https://docs.github.com/)
2. Review the CommitterAgent source code: `src/agents/committer.py`
3. Run the test script with verbose output for debugging
4. Check git logs in the temporary directory during operations

## Summary

The CommitterAgent enables seamless integration between the Agentic Blog Bird multi-agent system and GitHub Git repositories. By following this guide, you can automate the entire workflow from bird detection data to published blog posts in your repository.
