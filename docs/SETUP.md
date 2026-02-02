# Setup Guide for Agentic Blog Bird

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)
- (Optional) Microsoft Fabric access for real data integration
- (Optional) OpenAI API key or Azure OpenAI access for LLM integration

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

### 4. Configure Environment

```bash
# Copy the environment template
cp config/.env.template config/.env

# Edit the .env file with your credentials
nano config/.env  # or use your preferred editor
```

Fill in the following values in `.env`:

```env
# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=sk-your-key-here

# Azure OpenAI Configuration (if using Azure)
AZURE_OPENAI_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name

# Microsoft Fabric Configuration
FABRIC_WORKSPACE=your-workspace-id
FABRIC_TOKEN=your-access-token
FABRIC_LAKEHOUSE=your-lakehouse-name

# Hugo Site Configuration
HUGO_BASE_URL=https://yourblog.com
HUGO_OUTPUT_DIR=content/posts
```

### 5. Configure Agent Settings (Optional)

Edit `config/config.yaml` to customize:
- Agent behavior and parameters
- Writing style and tone
- Output formats and paths
- Quality thresholds

### 6. Test the Installation

Run the demo script to verify everything is working:

```bash
python examples/demo.py
```

This will:
- Test all four agents individually
- Run a complete workflow
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

## Microsoft Fabric Integration

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

## Next Steps

1. **Customize Your Agents**: Modify the system messages and behavior in each agent
2. **Add Real Data**: Integrate with your actual bird detection system
3. **Enhance Content**: Implement LLM integration for better content generation
4. **Automate**: Set up cron jobs or scheduled tasks to run daily
5. **Deploy**: Set up CI/CD to automatically publish to your Hugo site
