# Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Azure AI Foundry                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Microsoft Agent Framework                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Azure SDK
                              │
┌─────────────────────────────┼─────────────────────────────────┐
│         Agentic Blog Bird   │                                  │
│                             │                                  │
│  ┌──────────────────────────▼────────────────────────────┐   │
│  │           AgenticBlogBird Application                  │   │
│  │                  (src/main.py)                         │   │
│  └──────────────────┬──────────────────────────────────────┘   │
│                     │                                           │
│                     │ Initializes                               │
│                     ▼                                           │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              CoordinatorAgent                            │  │
│  │         (Orchestrates Multi-Agent Workflow)              │  │
│  └───┬──────────────────────────────────────────┬──────────┘  │
│      │                                           │              │
│      │ Manages                       Manages     │              │
│      │                                           │              │
│      ▼                                           ▼              │
│  ┌──────────────────────┐         ┌──────────────────────┐    │
│  │  DataCollectorAgent  │         │   BlogWriterAgent    │    │
│  │                      │         │                      │    │
│  │ - Process telemetry  │         │ - Generate blog posts│    │
│  │ - Parse notifications│────────▶│ - Create narratives  │    │
│  │ - Identify patterns  │  data   │ - Format content     │    │
│  └──────────────────────┘         └──────────────────────┘    │
│           ▲                                    │                │
└───────────┼────────────────────────────────────┼────────────────┘
            │                                    │
            │ Input                              │ Output
            │                                    │
┌───────────┴─────────┐              ┌──────────▼────────────┐
│  IoT Telemetry      │              │  Generated Blog Post  │
│  - Sensor readings  │              │  - Markdown format    │
│  - Notifications    │              │  - Engaging narrative │
│  - Events           │              │  - Data insights      │
└─────────────────────┘              └───────────────────────┘
```

## Component Interactions

### 1. Data Flow
```
IoT Data → DataCollectorAgent → Processed Data → BlogWriterAgent → Blog Post
```

### 2. Agent Communication
```
CoordinatorAgent.generate_blog_from_telemetry()
    ↓
    ├─→ DataCollectorAgent.process(raw_telemetry)
    │       └─→ Returns: processed_data + summary
    │
    └─→ BlogWriterAgent.process(processed_data)
            └─→ Returns: blog_post
```

## Class Hierarchy

```
BaseAgent (Abstract)
    │
    ├─→ DataCollectorAgent
    │       - Specializes in data processing
    │       - Maintains collection history
    │
    ├─→ BlogWriterAgent
    │       - Specializes in content generation
    │       - Customizable writing styles
    │
    └─→ CoordinatorAgent
            - Contains BlogWriterAgent instance
            - Contains DataCollectorAgent instance
            - Orchestrates workflows
```

## Configuration Flow

```
.env file
    ↓
Environment Variables
    ↓
src/config/settings.py
    ├─→ AzureAIConfig (Pydantic model)
    │       - Azure credentials
    │       - Endpoints
    │       - Model settings
    │
    └─→ AgentConfig (Pydantic model)
            - Agent names
            - Agent parameters
    ↓
Agents (initialized with config)
```

## Message Structure

```python
AgentMessage
    ├─ role: str           # "user" or "assistant"
    ├─ content: str        # Message content
    └─ metadata: Dict      # Optional context
```

## Workflow: Blog Generation

```
1. Application Start
   └─→ Initialize AgenticBlogBird
       └─→ Load Configuration
           └─→ Initialize CoordinatorAgent
               ├─→ Initialize DataCollectorAgent
               └─→ Initialize BlogWriterAgent

2. Generate Blog Post
   └─→ Call generate_blog_post(telemetry_data, title)
       └─→ CoordinatorAgent receives request
           │
           ├─→ Step 1: Data Collection
           │   └─→ DataCollectorAgent.process()
           │       ├─→ Parse sensor data
           │       ├─→ Parse notifications
           │       └─→ Generate summary
           │
           └─→ Step 2: Blog Generation
               └─→ BlogWriterAgent.process()
                   ├─→ Apply system prompt
                   ├─→ Process telemetry context
                   └─→ Generate markdown blog

3. Return Result
   └─→ Formatted blog post (string)
```

## Technology Stack

- **Language**: Python 3.12+
- **Framework**: Microsoft Agent Framework
- **Cloud Platform**: Azure AI Foundry
- **Key Libraries**:
  - azure-ai-projects (Agent framework integration)
  - azure-ai-agents (Core agent functionality)
  - azure-identity (Authentication)
  - pydantic (Configuration & validation)
  - asyncio (Async operations)

## Extensibility Points

1. **Add New Agents**: Extend `BaseAgent` class
2. **Custom Workflows**: Add methods to `CoordinatorAgent`
3. **Writing Styles**: Modify `BlogWriterAgent.writing_style`
4. **Data Sources**: Extend `DataCollectorAgent` parsing logic
5. **Azure Integration**: Configure inference client in base agent
