# Agentic Blog Bird 🐦

A multi-agent system for automatically generating entertaining blog posts based on bird detection events and telemetry data from backyard AI and IoT monitoring systems. Built with **Microsoft Agent Framework on Azure AI Foundry**.

## Overview

This system uses a team of specialized AI agents working together to produce high-quality blog posts from bird detection data:

1. **Editor Agent** - Orchestrates the entire workflow and ensures quality
2. **Researcher Agent** - Collects and analyzes data from Microsoft Fabric
3. **CopyWriter Agent** - Creates engaging narratives from the data
4. **Artist Agent** - Generates original cartoon-style images for blog posts
5. **Publisher Agent** - Formats content for Hugo-based static sites

The agents are powered by **Microsoft Agent Framework** running on **Azure AI Foundry**, providing robust orchestration and AI capabilities.

## Features

- ✨ Multi-agent architecture with specialized roles using Microsoft Agent Framework
- 🔵 Built on Azure AI Foundry for enterprise-grade AI orchestration
- 📊 Integration with Microsoft Fabric for data collection
- 📝 Automated content generation with engaging narratives
- 🎨 Cartoon-style image generation inspired by Wile E. Coyote and Road Runner
- 🖼️ Hugo-compatible markdown output with featured images
- 🔄 Workflow orchestration and quality control
- 📈 Configurable writing styles and content parameters
- 🔍 Built-in validation and quality checks

## Installation

### Prerequisites

- Python 3.8 or higher
- Azure subscription with Azure AI Foundry access
- Azure Blob Storage account with bird detection data files

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/toddwhitehead/agentic-blog-bird.git
cd agentic-blog-bird
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your Azure AI Foundry environment:
```bash
cp config/.env.template config/.env
# Edit config/.env with your Azure AI Foundry credentials and API keys
```

Required environment variables:
- `AZURE_AI_PROJECT_CONNECTION_STRING` - Your Azure AI Foundry project connection string
- `AZURE_AI_PROJECT_NAME` - Your Azure AI Foundry project name
- `AZURE_AI_DEPLOYMENT_NAME` - Your model deployment name
- `AZURE_STORAGE_CONNECTION_STRING` - Azure Storage connection string for blob storage
- `AZURE_STORAGE_ACCOUNT_NAME` - Azure Storage account name
- `BLOB_CONTAINER_NAME` - Blob container name (default: bird-detection-data)
- `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY` - API key for image generation (optional)

4. Update configuration (optional):
```bash
# Edit config/config.yaml to customize agent behavior
```

## Usage

### Basic Usage

Generate a blog post for today:
```bash
python main.py
```

Generate a blog post for a specific date:
```bash
python main.py --date 2024-01-15
```

Generate blog posts for all data files in blob storage:
```bash
python main.py --all-files
```

### Advanced Options

```bash
python main.py \
  --all-files \
  --config config/custom_config.yaml \
  --output-dir content/posts \
  --verbose
```

### Running the Demo

See the system in action with the demo script:
```bash
python examples/demo.py
```

## Configuration

### Main Configuration File (`config/config.yaml`)

The configuration file controls all aspects of the agent system:

- **Researcher**: Data collection settings, Azure Blob Storage connection
- **CopyWriter**: Writing style, tone, word count targets
- **Artist**: Image generation settings, cartoon style preferences
- **Publisher**: Hugo settings, output paths, metadata
- **Editor**: Quality thresholds, workflow settings
- **LLM**: Azure AI Foundry configuration (deployment name, parameters)

### Environment Variables (`.env`)

Required environment variables:
- `AZURE_AI_PROJECT_CONNECTION_STRING` - Azure AI Foundry project connection string
- `AZURE_AI_PROJECT_NAME` - Azure AI Foundry project name
- `AZURE_AI_DEPLOYMENT_NAME` - Model deployment name
- `AZURE_TENANT_ID` - Azure tenant ID
- `AZURE_CLIENT_ID` - Azure client ID (for service principal auth)
- `AZURE_CLIENT_SECRET` - Azure client secret (for service principal auth)
- `AZURE_STORAGE_CONNECTION_STRING` - Azure Storage connection string for blob storage
- `AZURE_STORAGE_ACCOUNT_NAME` - Azure Storage account name
- `BLOB_CONTAINER_NAME` - Blob container name (default: bird-detection-data)
- `OPENAI_API_KEY` - OpenAI API key for image generation (optional)
- `AZURE_OPENAI_API_KEY` - Azure OpenAI API key (alternative to OPENAI_API_KEY)
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint (when using Azure OpenAI)

## Architecture

### Agent Roles

**Editor Agent** (`src/agents/editor.py`)
- Coordinates all other agents using Microsoft Agent Framework
- Manages workflow execution on Azure AI Foundry
- Reviews content for quality
- Tracks workflow history

**Researcher Agent** (`src/agents/researcher.py`)
- Retrieves bird detection data from Azure Blob Storage
- Supports multiple data file formats (JSON, CSV)
- Analyzes patterns and trends
- Generates research summaries
- Identifies notable events

**CopyWriter Agent** (`src/agents/copywriter.py`)
- Creates engaging headlines
- Writes introductions, body, and conclusions
- Maintains consistent tone and style
- Formats narratives from data

**Artist Agent** (`src/agents/artist.py`)
- Generates original cartoon-style images
- Inspired by Wile E. Coyote and Road Runner aesthetics
- Creates visuals based on blog post content
- Integrates images with Hugo front matter

**Publisher Agent** (`src/agents/publisher.py`)
- Generates Hugo front matter
- Formats markdown content
- Creates SEO-friendly URLs
- Validates output format

All agents inherit from `BaseAgent` which provides common functionality for Microsoft Agent Framework integration.

### Technology Stack

- **Framework**: Microsoft Agent Framework
- **Platform**: Azure AI Foundry
- **Data Source**: Azure Blob Storage
- **Output**: Hugo static site generator
- **Language**: Python 3.8+

### Workflow

```
┌─────────────────────────────────────────────────┐
│              Editor Agent                       │
│         (Orchestrates Workflow)                 │
└─────────────────────────────────────────────────┘
                      │
      ┌───────────────┼───────────────┬──────────┐
      ▼               ▼               ▼          ▼
┌──────────┐   ┌──────────┐   ┌──────────┐ ┌──────────┐
│Researcher│──▶│CopyWriter│──▶│  Artist  │─│Publisher │
└──────────┘   └──────────┘   └──────────┘ └──────────┘
     │              │              │             │
     ▼              ▼              ▼             ▼
  Data          Content        Cartoon         Hugo
Collection     Generation      Images          Output
```

## Output Format

Blog posts are generated in Hugo-compatible markdown format with proper front matter:

```markdown
---
title: "A Day in the Life of Our Feathered Backyard Visitors"
date: 2024-01-15T10:00:00Z
draft: false
author: "Backyard Bird AI"
description: "Daily highlights from our backyard bird monitoring system"
tags: ["birds", "wildlife", "backyard", "AI monitoring"]
categories: ["Daily Updates"]
---

[Blog post content...]
```

## Project Structure

```
agentic-blog-bird/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py    # Base agent class for Microsoft Agent Framework
│   │   ├── editor.py        # Editor agent
│   │   ├── researcher.py    # Researcher agent
│   │   ├── copywriter.py    # CopyWriter agent
│   │   ├── artist.py        # Artist agent (image generation)
│   │   └── publisher.py     # Publisher agent
│   └── utils/
│       ├── __init__.py
│       └── config.py         # Configuration management
├── config/
│   ├── config.yaml           # Main configuration
│   └── .env.template         # Environment template
├── examples/
│   └── demo.py               # Demo script
├── content/
│   └── posts/                # Generated blog posts
│       └── images/           # Generated images
├── main.py                   # Main entry point
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Development

### Adding Custom Agents

To add a new agent using Microsoft Agent Framework, create a new class in `src/agents/`:

```python
from .base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__(name="CustomAgent", config=config)
        self._initialize_agent_client()
    
    def get_system_message(self):
        return "System message defining agent role..."
```

### Extending Functionality

- **Data Sources**: Modify `researcher.py` to add new data sources or change blob storage patterns
- **Content Styles**: Update `copywriter.py` for different writing styles
- **Output Formats**: Extend `publisher.py` for additional formats

### Data File Formats

The Researcher agent supports the following data file formats in blob storage:

**JSON Format:**
```json
{
  "date": "2024-01-15",
  "total_detections": 42,
  "species": ["Cardinal", "Blue Jay", "Sparrow"],
  "detections": [
    {
      "species": "Cardinal",
      "time": "08:30:00",
      "confidence": 0.95
    }
  ],
  "notable_events": ["First Cardinal sighting of the day"],
  "environmental_conditions": {
    "temperature": "45F",
    "weather": "sunny"
  }
}
```

**CSV Format:**
```csv
species,time,confidence
Cardinal,08:30:00,0.95
Blue Jay,09:15:00,0.92
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

[MIT License](LICENSE)

## Acknowledgments

- Built with Microsoft Agent Framework on Azure AI Foundry
- Integrated with Microsoft Fabric for data collection
- Designed for Hugo static site generator
- Inspired by multi-agent AI systems and autonomous workflows
