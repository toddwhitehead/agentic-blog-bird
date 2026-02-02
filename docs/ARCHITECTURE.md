# Architecture Documentation

## Overview

Agentic Blog Bird is a multi-agent system designed to automatically generate blog posts from bird detection events. The system follows a collaborative agent architecture where specialized agents work together under the coordination of an Editor agent.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Agentic Blog Bird                        │
│                  Multi-Agent System                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Editor Agent                            │
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
│  Researcher  │───▶│  CopyWriter  │───▶│  Publisher   │
│    Agent     │    │    Agent     │    │    Agent     │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
  Data Query         Content Creation      Hugo Output
  & Analysis         & Narrative          & Formatting
```

## Agent Specifications

### 1. Editor Agent

**Location**: `src/agents/editor.py`

**Purpose**: Central orchestrator responsible for coordinating all other agents and ensuring quality standards.

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

### 4. Publisher Agent

**Location**: `src/agents/publisher.py`

**Purpose**: Format and publish blog posts in Hugo-compatible markdown format.

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
5. **Publishing** - Publisher formats and saves Hugo markdown
6. **Validation** - Editor validates final output format

## Data Flow

```
Raw Data (Fabric) → Researcher → Research Summary
                                       ↓
                               CopyWriter → Blog Post Content
                                       ↓
                               Publisher → Hugo Markdown File
```

## Configuration System

The system uses YAML-based configuration with environment variable support:

- `config/config.yaml` - Main configuration file
- `config/.env` - Environment-specific secrets and credentials
- `src/utils/config.py` - Configuration management utilities

## Extension Points

### Adding New Agents

Create agent class in `src/agents/` and integrate with Editor agent.

### Custom Data Sources

Modify `researcher.py` to add new data source integrations.

### Custom Output Formats

Extend `publisher.py` for additional output format support.

## Future Enhancements

- LLM integration for enhanced content generation
- Multi-language support
- Image generation from detection data
- Social media auto-posting
- Analytics integration
- Real-time generation capabilities
