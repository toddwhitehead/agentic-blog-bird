# Agentic Blog Bird

A multi-agent application built with **Microsoft Agent Framework** and **Azure AI Foundry** to generate entertaining blog posts from telemetry and notifications from backyard AI and IoT monitoring systems.

## Overview

Agentic Blog Bird uses a coordinated multi-agent architecture to transform raw sensor data and IoT notifications into engaging blog content. The system leverages Microsoft's Agent Framework running on Azure AI Foundry for intelligent processing and content generation.

## Architecture

The application consists of three specialized agents:

1. **DataCollectorAgent**: Collects and processes telemetry data from IoT sensors and notifications
2. **BlogWriterAgent**: Generates entertaining blog posts from processed data
3. **CoordinatorAgent**: Orchestrates the workflow between agents to complete complex tasks

All agents are built on the Microsoft Agent Framework and designed to work with Azure AI Foundry.

## Features

- 🤖 Multi-agent architecture using Microsoft Agent Framework
- ☁️ Integration with Azure AI Foundry
- 📊 Telemetry data processing and analysis
- ✍️ Automated blog post generation
- 🔄 Coordinated agent workflows
- 📝 Conversation history tracking
- 🎨 Customizable writing styles

## Prerequisites

- Python 3.12 or higher
- Azure subscription with AI Foundry access
- Azure OpenAI deployment (e.g., GPT-4)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/toddwhitehead/agentic-blog-bird.git
cd agentic-blog-bird
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Azure AI Foundry:
```bash
cp .env.example .env
# Edit .env with your Azure credentials and configuration
```

## Configuration

Set up your `.env` file with the following Azure AI Foundry credentials:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-project>.api.azureml.ms
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_PROJECT_NAME=<your-project-name>
AZURE_OPENAI_DEPLOYMENT=gpt-4
```

See `.env.example` for all available configuration options.

## Usage

### Basic Usage

Run the application with example data:

```bash
python -m src.main
```

### Programmatic Usage

```python
import asyncio
from src.main import AgenticBlogBird

async def generate_blog():
    app = AgenticBlogBird()
    
    # Example telemetry data
    telemetry = {
        "sensors": {
            "temperature": {"value": 72.5, "unit": "F"},
            "humidity": {"value": 65, "unit": "%"}
        },
        "notifications": [
            {"message": "Bird activity detected", "priority": "normal"}
        ]
    }
    
    # Generate blog post
    blog_post = await app.generate_blog_post(
        raw_telemetry=telemetry,
        title="Backyard Adventures"
    )
    
    print(blog_post)

asyncio.run(generate_blog())
```

### Using Individual Agents

```python
from src.agents import DataCollectorAgent, BlogWriterAgent

# Initialize agents
collector = DataCollectorAgent()
writer = BlogWriterAgent()

# Process data
result = await collector.process({
    "message": "Process telemetry",
    "context": {"raw_telemetry": telemetry_data}
})

# Generate blog
blog = await writer.process({
    "message": "Write blog post",
    "context": {"telemetry": result["processed_data"]}
})
```

## Project Structure

```
agentic-blog-bird/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py    # Base agent class
│   │   ├── blog_writer_agent.py
│   │   ├── data_collector_agent.py
│   │   └── coordinator_agent.py
│   └── config/
│       ├── __init__.py
│       └── settings.py      # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── .gitignore
└── README.md
```

## Microsoft Agent Framework Integration

This application is built on the Microsoft Agent Framework, which provides:

- **Agent Orchestration**: Coordinate multiple specialized agents
- **Azure AI Foundry Integration**: Seamless connection to Azure AI services
- **Model Management**: Easy integration with Azure OpenAI deployments
- **Scalability**: Production-ready agent architecture

### Key Components

- **BaseAgent**: Foundation class for all agents with conversation history and message handling
- **Agent Communication**: Structured message passing between agents using `AgentMessage` dataclass
- **Async Processing**: Non-blocking agent operations using Python asyncio
- **Azure Integration**: Ready for Azure AI Foundry inference client integration

## Development

### Running Tests

(Tests to be added based on project requirements)

```bash
pytest tests/
```

### Code Style

The project follows Python best practices and PEP 8 style guidelines.

## Roadmap

- [ ] Full Azure AI Foundry inference client integration
- [ ] Real-time telemetry streaming support
- [ ] Web API for blog generation
- [ ] Advanced anomaly detection in telemetry
- [ ] Multiple blog style templates
- [ ] Database storage for generated posts
- [ ] Monitoring and observability with Azure Application Insights

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.

## Acknowledgments

- Built with [Microsoft Agent Framework](https://learn.microsoft.com/en-us/azure/ai-services/agents/)
- Powered by [Azure AI Foundry](https://azure.microsoft.com/en-us/products/ai-foundry/)
- Uses [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)
