# Setup Guide for Agentic Blog Bird

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)
- Azure subscription with Azure AI Foundry access
- (Optional) Microsoft Fabric access for real data integration

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/toddwhitehead/agentic-blog-bird.git
cd agentic-blog-bird
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Azure AI Foundry

#### Create Azure AI Foundry Project

1. Go to [Azure AI Foundry Portal](https://ai.azure.com)
2. Create a new project or select an existing one
3. Note your project connection string and project name
4. Deploy a model (e.g., GPT-4, GPT-3.5-turbo) for the agents to use

#### Create Service Principal for Authentication

```bash
# Create a service principal with minimal permissions
# Use a more specific role for Azure AI Foundry
az ad sp create-for-rbac --name "agentic-blog-bird-sp" \
  --role "Cognitive Services OpenAI User" \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{account-name}

# Alternatively, use Azure AI Developer role (if available)
# az ad sp create-for-rbac --name "agentic-blog-bird-sp" \
#   --role "Azure AI Developer" \
#   --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group}

# Note the output:
# - appId (AZURE_CLIENT_ID)
# - password (AZURE_CLIENT_SECRET)
# - tenant (AZURE_TENANT_ID)
```

### 5. Configure Environment

```bash
# Copy the environment template
cp config/.env.template config/.env

# Edit the .env file with your credentials
nano config/.env  # or use your preferred editor
```

Fill in the following values in `.env`:

```env
# Azure AI Foundry Configuration
AZURE_AI_PROJECT_CONNECTION_STRING=your_connection_string
AZURE_AI_PROJECT_NAME=your_project_name
AZURE_AI_DEPLOYMENT_NAME=your_model_deployment_name

# Azure Authentication
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret

# Microsoft Fabric Configuration (Optional)
FABRIC_WORKSPACE=your-workspace-id
FABRIC_TOKEN=your-access-token
FABRIC_LAKEHOUSE=your-lakehouse-name

# Hugo Site Configuration
HUGO_BASE_URL=https://yourblog.com
HUGO_OUTPUT_DIR=content/posts
```

### 6. Configure Agent Settings (Optional)

Edit `config/config.yaml` to customize:
- Agent behavior and parameters
- Writing style and tone
- Output formats and paths
- Quality thresholds
- Azure AI Foundry deployment settings

### 7. Test the Installation

Run the demo script to verify everything is working:

```bash
python examples/demo.py
```

This will:
- Test all four agents individually using Microsoft Agent Framework
- Run a complete workflow orchestrated by the Editor agent
- Generate sample blog posts in `examples/output/`

## Usage

### Generate a Blog Post

For today's date:
```bash
python main.py
```

For a specific date:
```bash
python main.py --date 2024-01-15
```

With custom configuration:
```bash
python main.py --config config/custom_config.yaml --output-dir my_posts/
```

### Integration with Hugo

If you're using Hugo for your blog:

1. Ensure the output directory matches your Hugo content directory:
   ```yaml
   # In config/config.yaml
   publisher:
     output_dir: "content/posts"
   ```

2. Run the blog generation:
   ```bash
   python main.py
   ```

3. Build your Hugo site:
   ```bash
   hugo server -D  # For preview
   hugo            # For production build
   ```

## Azure AI Foundry Integration

### Model Deployment

The system uses Azure AI Foundry for AI agent orchestration and model inference:

1. **Choose a Model**: In Azure AI Foundry, deploy a model suitable for your needs:
   - GPT-4 for high-quality content
   - GPT-3.5-turbo for faster, cost-effective generation
   
2. **Update Configuration**: Set the deployment name in `config/config.yaml`:
   ```yaml
   llm:
     provider: "azure_ai_foundry"
     deployment_name: "gpt-4"
   ```

3. **Test Connection**: The base agent will automatically connect to Azure AI Foundry using your credentials

### Microsoft Fabric Integration

To connect to Microsoft Fabric for real bird detection data:

1. Set up Microsoft Fabric access:
   - Create a workspace in Microsoft Fabric
   - Set up a lakehouse with your bird detection data
   - Generate an access token

2. Update your `.env` file with Fabric credentials

3. Modify `src/agents/researcher.py` to implement actual Fabric queries:
   ```python
   def collect_bird_data(self, date: str = None) -> Dict[str, Any]:
       # Add your Fabric query logic here
       # Use the Fabric SDK to query your lakehouse
       pass
   ```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Azure Authentication Errors**
```bash
# Verify your Azure credentials
az account show

# Test service principal authentication
az login --service-principal \
  -u $AZURE_CLIENT_ID \
  -p $AZURE_CLIENT_SECRET \
  --tenant $AZURE_TENANT_ID
```

**Azure AI Foundry Connection Issues**
- Verify your project connection string is correct
- Check that your service principal has the necessary permissions
- Ensure your subscription is active and has available quota
- Verify the deployment name matches your Azure AI Foundry deployment

**Permission Errors**
```bash
# Make sure output directories are writable
chmod -R 755 content/
chmod -R 755 examples/output/
```

**Configuration Not Found**
```bash
# Create config directory if it doesn't exist
mkdir -p config

# Copy the template
cp config/.env.template config/.env
```

## Advanced Configuration

### Using Managed Identity (Recommended for Production)

Instead of service principal credentials, use Azure Managed Identity:

1. Enable managed identity on your Azure resource (VM, App Service, etc.)
2. Grant the managed identity access to your Azure AI Foundry project
3. Remove client credentials from `.env`:
   ```env
   # Remove or comment out:
   # AZURE_CLIENT_ID=...
   # AZURE_CLIENT_SECRET=...
   ```
4. The `azure-identity` library will automatically use managed identity

### Monitoring and Logging

Enable Azure Application Insights for monitoring:

1. Create an Application Insights resource in Azure
2. Add the connection string to your `.env`:
   ```env
   APPLICATIONINSIGHTS_CONNECTION_STRING=your_connection_string
   ```
3. The agents will automatically send telemetry to Application Insights

## Next Steps

1. **Customize Your Agents**: Modify the system messages and behavior in each agent
2. **Add Real Data**: Integrate with your actual bird detection system via Microsoft Fabric
3. **Enhance Content**: Leverage Azure AI models for better content generation
4. **Automate**: Set up Azure Functions or Logic Apps to run on a schedule
5. **Deploy**: Use Azure DevOps or GitHub Actions for CI/CD
6. **Monitor**: Set up alerts and dashboards in Application Insights

## Security Best Practices

- Store credentials in Azure Key Vault instead of `.env` files
- Use managed identities for authentication when possible
- Rotate service principal secrets regularly
- Enable Azure RBAC for fine-grained access control
- Use private endpoints for Azure services when available
- Enable audit logging for compliance requirements
