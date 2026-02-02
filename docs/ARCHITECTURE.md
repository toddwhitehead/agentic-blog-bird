# Architecture Documentation

## Overview

Agentic Blog Bird is a multi-agent system designed to automatically generate blog posts from bird detection events. The system follows a collaborative agent architecture where specialized agents work together under the coordination of an Editor agent, powered by **Microsoft Agent Framework on Azure AI Foundry**.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Agentic Blog Bird                        │
│         Multi-Agent System (Microsoft Agent Framework)       │
│                    Azure AI Foundry                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Editor Agent                            │
│                  (BaseAgent subclass)                        │
│                                                              │
│  Role: Workflow Orchestration & Quality Control             │
│  - Coordinates all other agents                             │
│  - Manages workflow execution                               │
│  - Reviews content quality                                  │
│  - Validates final output                                   │
└─────────────────────────────────────────────────────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Researcher  │───▶│  CopyWriter  │───▶│   Artist     │
│    Agent     │    │    Agent     │    │    Agent     │
│ (BaseAgent)  │    │ (BaseAgent)  │    │ (BaseAgent)  │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        │                    │                    ▼
        │                    │            ┌──────────────┐
        │                    │            │  Publisher   │
        │                    │            │    Agent     │
        │                    │            │ (BaseAgent)  │
        │                    │            └──────────────┘
        ▼                    ▼                    ▼
  Data Query         Content Creation      Hugo Output
  & Analysis         & Narrative          & Images
```

## Agent Specifications

### Base Agent Class

**Location**: `src/agents/base_agent.py`

**Purpose**: Provides common functionality for all agents using Microsoft Agent Framework.

**Key Features**:
- Azure AI Foundry client initialization
- Credential management for Azure services
- Common agent invocation methods
- Metadata tracking

**Key Methods**:
- `_get_azure_credentials()` - Retrieve Azure credentials from environment
- `_initialize_agent_client()` - Initialize Microsoft Agent Framework client
- `get_system_message()` - Define agent system prompt
- `_invoke_agent(prompt, context)` - Invoke agent with Microsoft Agent Framework
- `get_metadata()` - Get agent metadata

### 1. Editor Agent

**Location**: `src/agents/editor.py`

**Purpose**: Central orchestrator responsible for coordinating all other agents and ensuring quality standards using Microsoft Agent Framework.

**Inherits**: `BaseAgent`

**Responsibilities**:
- Initiate and manage the blog creation workflow
- Coordinate communication between agents
- Review research quality from Researcher agent
- Review content quality from CopyWriter agent
- Ensure publishing standards are met
- Track workflow history and metrics

**Key Methods**:
- `orchestrate_blog_creation(date: str)` - Main workflow orchestration
- `_conduct_research(date: str)` - Coordinate with Researcher
- `_create_content(research_summary: str)` - Coordinate with CopyWriter
- `_publish_content(blog_post: Dict, date: str)` - Coordinate with Publisher
- `_validate_output(filepath: str)` - Final validation

### 2. Researcher Agent

**Location**: `src/agents/researcher.py`

**Purpose**: Collect and analyze bird detection data from Microsoft Fabric.

**Inherits**: `BaseAgent`

**Responsibilities**:
- Query Microsoft Fabric for bird detection events
- Aggregate and analyze detection data
- Identify patterns and notable events
- Generate structured research summaries

**Key Methods**:
- `collect_bird_data(date: str)` - Query Fabric for raw data
- `analyze_patterns(data: Dict)` - Analyze patterns
- `generate_research_summary(date: str)` - Generate report

### 3. CopyWriter Agent

**Location**: `src/agents/copywriter.py`

**Purpose**: Transform research data into engaging blog post narratives.

**Inherits**: `BaseAgent`

**Responsibilities**:
- Create compelling headlines
- Write engaging introductions
- Develop narrative structure
- Balance entertainment with information
- Maintain consistent tone and style

**Key Methods**:
- `create_headline(research_data: str)` - Generate title
- `write_introduction(research_data: str, headline: str)` - Create opening
- `write_body(research_data: str)` - Develop main content
- `write_conclusion(research_data: str)` - Create ending
- `generate_blog_post(research_data: str)` - Complete content creation

### 4. Artist Agent

**Location**: `src/agents/artist.py`

**Purpose**: Generate original cartoon-style images to accompany blog posts.

**Inherits**: `BaseAgent`

**Responsibilities**:
- Analyze blog post content for visual themes
- Generate image prompts based on content
- Create cartoon-style images inspired by Wile E. Coyote and Road Runner
- Integrate images with Hugo front matter
- Save images to appropriate directories

**Key Methods**:
- `generate_image_prompt(blog_post_content: str)` - Create AI image prompt
- `generate_image(prompt: str, filename: str)` - Call image generation API
- `create_blog_image(blog_post_data: Dict)` - Complete image creation workflow
- `get_image_metadata(image_path: str)` - Get image information

**Image Style**:
- Vibrant, cartoon aesthetic inspired by classic Looney Tunes
- Bold colors and exaggerated expressions
- Dynamic action poses and comedic energy
- Desert/southwestern landscape elements

### 5. Publisher Agent

**Location**: `src/agents/publisher.py`

**Purpose**: Format and publish blog posts in Hugo-compatible markdown format.

**Inherits**: `BaseAgent`

**Responsibilities**:
- Generate Hugo front matter with metadata
- Format content as proper markdown
- Create SEO-friendly URL slugs
- Validate Hugo format compliance

**Key Methods**:
- `create_frontmatter(post_data: Dict)` - Generate YAML front matter
- `format_content(content: str)` - Format markdown
- `create_slug(title: str, date: str)` - Generate URL-friendly slug
- `publish_post(post_data: Dict)` - Write formatted post to file
- `validate_hugo_format(filepath: str)` - Validate output

## Workflow Sequence

1. **Research Phase** - Researcher collects data from Microsoft Fabric
2. **Research Review** - Editor validates research quality
3. **Content Creation** - CopyWriter creates blog post narrative
4. **Content Review** - Editor validates content quality
5. **Image Generation** - Artist creates cartoon-style featured image
6. **Publishing** - Publisher formats and saves Hugo markdown with image
7. **Validation** - Editor validates final output format

## Data Flow

```
Raw Data (Fabric) → Researcher → Research Summary
                                       ↓
                               CopyWriter → Blog Post Content
                                       ↓
                                   Artist → Featured Image
                                       ↓
                               Publisher → Hugo Markdown File + Image
```

## Configuration System

The system uses YAML-based configuration with environment variable support for Azure AI Foundry:

- `config/config.yaml` - Main configuration file
- `config/.env` - Environment-specific secrets and credentials (Azure AI Foundry, Fabric, etc.)
- `src/utils/config.py` - Configuration management utilities

## Technology Stack

- **Agent Framework**: Microsoft Agent Framework
- **Platform**: Azure AI Foundry
- **Data Source**: Microsoft Fabric
- **Programming Language**: Python 3.8+
- **Output Format**: Hugo-compatible Markdown
- **Authentication**: Azure Identity (service principal, managed identity)

## Extension Points

### Adding New Agents

Create agent class in `src/agents/` by inheriting from `BaseAgent` and integrate with Editor agent.

Example:
```python
from .base_agent import BaseAgent

class NewAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__(name="NewAgent", config=config)
        self._initialize_agent_client()
```

### Custom Data Sources

Modify `researcher.py` to add new data source integrations (Azure Data Explorer, other Fabric sources).

### Custom Output Formats

Extend `publisher.py` for additional output format support (WordPress, Medium, etc.).

## Future Enhancements

- Enhanced LLM integration with Azure AI Foundry
- Multi-language support using Microsoft Translator
- Advanced image generation with custom fine-tuned models
- Social media auto-posting
- Analytics integration with Azure Application Insights
- Real-time generation capabilities using Azure Functions
- Advanced agent collaboration patterns with Microsoft Agent Framework
