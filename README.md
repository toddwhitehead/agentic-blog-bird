# Agentic Blog Bird 🐦

A multi-agent system for automatically generating entertaining blog posts based on bird detection events and telemetry data from backyard AI and IoT monitoring systems.

## Overview

This system uses a team of specialized AI agents working together to produce high-quality blog posts from bird detection data:

1. **Editor Agent** - Orchestrates the entire workflow and ensures quality
2. **Researcher Agent** - Collects and analyzes data from Microsoft Fabric
3. **CopyWriter Agent** - Creates engaging narratives from the data
4. **Publisher Agent** - Formats content for Hugo-based static sites

## Features

- ✨ Multi-agent architecture with specialized roles
- 📊 Integration with Microsoft Fabric for data collection
- 📝 Automated content generation with engaging narratives
- 🎨 Hugo-compatible markdown output
- 🔄 Workflow orchestration and quality control
- 📈 Configurable writing styles and content parameters
- 🔍 Built-in validation and quality checks

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

3. Configure your environment:
```bash
cp config/.env.template config/.env
# Edit config/.env with your API keys and credentials
```

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

### Advanced Options

```bash
python main.py \
  --date 2024-01-15 \
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

- **Researcher**: Data collection settings, Fabric connection
- **CopyWriter**: Writing style, tone, word count targets
- **Publisher**: Hugo settings, output paths, metadata
- **Editor**: Quality thresholds, workflow settings
- **LLM**: AI model configuration (OpenAI/Azure)

### Environment Variables (`.env`)

Required environment variables:
- `OPENAI_API_KEY` - OpenAI API key (if using OpenAI)
- `AZURE_OPENAI_KEY` - Azure OpenAI key (if using Azure)
- `FABRIC_WORKSPACE` - Microsoft Fabric workspace
- `FABRIC_TOKEN` - Fabric authentication token

## Architecture

### Agent Roles

**Editor Agent** (`src/agents/editor.py`)
- Coordinates all other agents
- Manages workflow execution
- Reviews content for quality
- Tracks workflow history

**Researcher Agent** (`src/agents/researcher.py`)
- Queries Microsoft Fabric for bird detection data
- Analyzes patterns and trends
- Generates research summaries
- Identifies notable events

**CopyWriter Agent** (`src/agents/copywriter.py`)
- Creates engaging headlines
- Writes introductions, body, and conclusions
- Maintains consistent tone and style
- Formats narratives from data

**Publisher Agent** (`src/agents/publisher.py`)
- Generates Hugo front matter
- Formats markdown content
- Creates SEO-friendly URLs
- Validates output format

### Workflow

```
┌─────────────────────────────────────────────────┐
│              Editor Agent                       │
│         (Orchestrates Workflow)                 │
└─────────────────────────────────────────────────┘
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│Researcher│──▶│CopyWriter│──▶│Publisher │
└──────────┘   └──────────┘   └──────────┘
     │              │              │
     ▼              ▼              ▼
  Data          Content         Hugo
Collection     Generation       Output
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
│   │   ├── editor.py       # Editor agent
│   │   ├── researcher.py   # Researcher agent
│   │   ├── copywriter.py   # CopyWriter agent
│   │   └── publisher.py    # Publisher agent
│   └── utils/
│       ├── __init__.py
│       └── config.py        # Configuration management
├── config/
│   ├── config.yaml          # Main configuration
│   └── .env.template        # Environment template
├── examples/
│   └── demo.py              # Demo script
├── content/
│   └── posts/               # Generated blog posts
├── main.py                  # Main entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Development

### Adding Custom Agents

To add a new agent, create a new class in `src/agents/`:

```python
class CustomAgent:
    def __init__(self, config=None):
        self.config = config or {}
        self.name = "CustomAgent"
    
    def get_system_message(self):
        return "System message defining agent role..."
```

### Extending Functionality

- **Data Sources**: Modify `researcher.py` to add new data sources
- **Content Styles**: Update `copywriter.py` for different writing styles
- **Output Formats**: Extend `publisher.py` for additional formats

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

[MIT License](LICENSE)

## Acknowledgments

- Built for integration with Microsoft Fabric for data collection
- Designed for Hugo static site generator
- Inspired by multi-agent AI systems and autonomous workflows
