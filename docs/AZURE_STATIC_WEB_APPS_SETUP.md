# Azure Static Web Apps Setup Guide

This guide explains how to set up Azure Static Web Apps to work with the Agentic Blog Bird delivery agent.

## Prerequisites

- Azure subscription
- Git repository for your Hugo blog
- Agentic Blog Bird configured and working

## Step 1: Create an Azure Static Web App

### Using Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Static Web App" and select it
4. Click "Create"

### Configure Basic Settings

- **Subscription**: Select your Azure subscription
- **Resource Group**: Create new or select existing
- **Name**: Choose a unique name (e.g., `my-bird-blog`)
- **Plan Type**: Choose Free or Standard based on needs
- **Region**: Select a region close to your users
- **Source**: Choose GitHub (or Azure DevOps/Bitbucket)

### Configure Deployment Details

1. Sign in to GitHub when prompted
2. Select your organization
3. Select your Hugo blog repository
4. Select the branch to deploy from (e.g., `main`)

### Build Details

Configure the build settings for Hugo:

- **Build Presets**: Choose "Hugo"
- **App location**: `/` (or your content root)
- **Api location**: Leave empty (unless you have API functions)
- **Output location**: `public` (Hugo's default output directory)

Click "Review + create" then "Create"

## Step 2: Configure Hugo Build Settings (Optional)

If you need custom build settings, create a file `staticwebapp.config.json` in your repository root:

```json
{
  "routes": [
    {
      "route": "/*",
      "serve": "/index.html",
      "statusCode": 200
    }
  ],
  "navigationFallback": {
    "rewrite": "/index.html"
  },
  "responseOverrides": {
    "404": {
      "rewrite": "/404.html",
      "statusCode": 404
    }
  }
}
```

## Step 3: Configure GitHub Workflow (Automatic)

Azure automatically creates a GitHub Actions workflow file in your repository at `.github/workflows/azure-static-web-apps-*.yml`. This workflow:

1. Triggers on pushes to your main branch
2. Builds your Hugo site
3. Deploys to Azure Static Web Apps

You can customize the Hugo version in this workflow if needed:

```yaml
- name: Build And Deploy
  uses: Azure/static-web-apps-deploy@v1
  with:
    # ... other settings ...
    app_build_command: 'hugo --minify'
```

## Step 4: Configure Agentic Blog Bird

Update your `config/config.yaml` with the delivery settings:

```yaml
delivery:
  # Your blog repository URL
  target_repo_url: "https://github.com/yourusername/your-hugo-blog.git"
  target_repo_branch: "main"
  target_repo_path: "/tmp/blog-delivery-repo"
  
  # Hugo site structure
  content_subdir: "content/posts"
  images_subdir: "content/posts/images"
  
  # Git configuration
  git_user_name: "Blog Bird Agent"
  git_user_email: "blogbird@example.com"
  commit_message_template: "Add blog post: {title}"
  
  # Enable automatic delivery
  auto_deliver: true  # Set to true for automatic deployment
  validate_before_push: true
```

## Step 5: Configure Git Authentication

### Option A: Using Personal Access Token (HTTPS)

1. Generate a GitHub Personal Access Token:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Click "Generate new token"
   - Select scopes: `repo` (for private repos) or `public_repo` (for public repos)
   - Copy the token

2. Configure git credentials for Agentic Blog Bird:
   ```bash
   # Update your repository URL to include the token
   # Format: https://TOKEN@github.com/username/repo.git
   ```

3. Or use git credential helper:
   ```bash
   git config --global credential.helper store
   # First push will prompt for credentials, then store them
   ```

### Option B: Using SSH Keys

1. Generate SSH key if you don't have one:
   ```bash
   ssh-keygen -t ed25519 -C "blogbird@example.com"
   ```

2. Add the public key to GitHub:
   - Go to GitHub Settings > SSH and GPG keys
   - Click "New SSH key"
   - Paste your public key

3. Use SSH URL in your configuration:
   ```yaml
   target_repo_url: "git@github.com:yourusername/your-hugo-blog.git"
   ```

## Step 6: Test the Delivery

1. Run the demo script:
   ```bash
   python examples/demo_delivery.py
   ```

2. Or use the main workflow:
   ```bash
   python main.py --date 2024-02-01
   ```

3. Check your Azure Static Web App:
   - Go to Azure Portal > Your Static Web App > Deployments
   - You should see a new deployment triggered by the git push
   - Wait for the build to complete (usually 1-3 minutes)

## Monitoring Deployments

### Azure Portal

- View deployment history in the Azure Portal
- Check build logs for any errors
- Monitor performance and usage metrics

### GitHub Actions

- View workflow runs in your repository's Actions tab
- Check build logs for Hugo build issues
- Receive notifications on failures

## Troubleshooting

### Issue: Authentication Failed

**Solution**: 
- Verify your git credentials are correct
- For HTTPS: Check your Personal Access Token is valid and has correct permissions
- For SSH: Ensure your SSH key is added to GitHub and the SSH agent is running

### Issue: Build Fails in Azure

**Solution**:
- Check Hugo version compatibility
- Verify `config.toml` or `config.yaml` in your Hugo site is correct
- Check the build logs in Azure Portal for specific errors

### Issue: Site Deploys but Content Missing

**Solution**:
- Verify `content/posts` directory exists in your repository
- Check that blog post files are in the correct location
- Ensure Hugo configuration includes the content directory

### Issue: Delivery Agent Cannot Clone Repository

**Solution**:
- Verify the repository URL is correct
- Check network connectivity
- Ensure git is installed and accessible: `git --version`

## Best Practices

1. **Use SSH for Production**: More secure than HTTPS with tokens
2. **Enable Auto-Delivery Carefully**: Start with `auto_deliver: false` and test manually
3. **Monitor Deployments**: Set up alerts for failed deployments
4. **Use Preview Environments**: Azure Static Web Apps supports preview deployments for PRs
5. **Backup Your Content**: Ensure your blog posts are backed up outside the delivery process

## Additional Resources

- [Azure Static Web Apps Documentation](https://docs.microsoft.com/azure/static-web-apps/)
- [Hugo Documentation](https://gohugo.io/documentation/)
- [GitHub Actions Documentation](https://docs.github.com/actions)

## Cost Considerations

- **Free Tier**: 100 GB bandwidth per month, good for small blogs
- **Standard Tier**: More bandwidth and custom domains, pay per usage
- **GitHub Actions**: Included in GitHub Free for public repos, limited minutes for private repos

## Security Notes

- Never commit git credentials to your repository
- Use environment variables for sensitive configuration
- Rotate access tokens regularly
- Use least-privilege access for service accounts
- Enable branch protection rules in GitHub to prevent accidental force pushes
