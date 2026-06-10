# Azure AI Foundry Model Recommendations

This document provides detailed recommendations for Azure AI Foundry model deployments to optimize each agent's performance in the Agentic Blog Bird system.

## Overview

The multi-agent system uses different models based on each agent's specific needs. Choosing the right model for each agent ensures optimal performance, cost-efficiency, and quality output.

## Model Selection by Agent

### 1. Editor Agent (Orchestrator)
**Primary Purpose:** Workflow orchestration, quality control, and content review

**Recommended Models:**
- **Primary:** GPT-4o (gpt-4o) - Latest optimized GPT-4 model
- **Alternative:** GPT-4 Turbo (gpt-4-turbo)
- **Budget-Friendly:** GPT-3.5 Turbo (gpt-3.5-turbo)

**Rationale:**
- Requires strong reasoning to coordinate multiple agents
- Needs excellent judgment for quality assessment
- Must understand complex workflows and dependencies
- Benefits from multimodal capabilities for image review

**Deployment Configuration:**
```yaml
deployment_name: "gpt-4o-editor"
model: "gpt-4o"
temperature: 0.3  # Lower temperature for consistent decision-making
max_tokens: 2000
top_p: 0.95
```

**Azure Foundry Settings:**
- **Capacity:** Standard (can handle orchestration without premium throughput)
- **Rate Limit:** 60K tokens/minute recommended
- **Concurrent Requests:** 10-20 for workflow management

### 2. Researcher Agent (Data Analysis)
**Primary Purpose:** Data collection, pattern analysis, and research summarization

**Recommended Models:**
- **Primary:** GPT-4o Mini (gpt-4o-mini) - Cost-effective for structured data
- **Alternative:** GPT-3.5 Turbo (gpt-3.5-turbo)
- **Advanced:** GPT-4o (for complex pattern analysis)

**Rationale:**
- Primarily works with structured JSON/CSV data
- Requires reliable data parsing and summarization
- Cost-effective option for high-frequency data processing
- GPT-4o Mini provides excellent value for structured tasks

**Deployment Configuration:**
```yaml
deployment_name: "gpt-4o-mini-researcher"
model: "gpt-4o-mini"
temperature: 0.5  # Balanced for factual analysis
max_tokens: 3000  # Higher limit for comprehensive summaries
top_p: 0.9
```

**Azure Foundry Settings:**
- **Capacity:** Standard (data processing doesn't require premium)
- **Rate Limit:** 80K tokens/minute for batch processing
- **Concurrent Requests:** 20-50 for multiple file processing

### 3. CopyWriter Agent (Content Creation)
**Primary Purpose:** Creative narrative writing and engaging blog post generation

**Recommended Models:**
- **Primary:** GPT-4o (gpt-4o) - Best for creative, engaging content
- **Alternative:** GPT-4 Turbo (gpt-4-turbo)
- **Budget Option:** GPT-3.5 Turbo 16K (for longer context)

**Rationale:**
- Requires strong creative writing capabilities
- Must maintain consistent tone and personality
- Benefits from understanding nuance and humor
- Needs to weave data into engaging narratives

**Deployment Configuration:**
```yaml
deployment_name: "gpt-4o-copywriter"
model: "gpt-4o"
temperature: 0.8  # Higher temperature for creativity
max_tokens: 4000  # Allow for longer blog posts
top_p: 0.95
presence_penalty: 0.3  # Encourage diverse vocabulary
frequency_penalty: 0.3  # Reduce repetition
```

**Azure Foundry Settings:**
- **Capacity:** Standard to Premium (for consistent quality)
- **Rate Limit:** 40K tokens/minute
- **Concurrent Requests:** 5-10 (content generation is sequential)

### 4. Artist Agent (Image Generation)
**Primary Purpose:** Generating cartoon-style images for blog posts

**Recommended Models:**
- **Primary:** DALL-E 3 (dall-e-3) - Best quality and style control
- **Alternative:** DALL-E 2 (dall-e-2) - More cost-effective

**Rationale:**
- Requires image generation capabilities
- Needs fine control over style (cartoon/Looney Tunes aesthetic)
- DALL-E 3 provides better prompt understanding and quality
- Style consistency is crucial for brand identity

**Deployment Configuration:**
```yaml
deployment_name: "dall-e-3-artist"
model: "dall-e-3"
image_size: "1024x1024"
quality: "standard"  # Use "hd" for premium quality
style: "vivid"  # For vibrant cartoon colors
```

**Azure Foundry Settings:**
- **Capacity:** Standard (image generation has built-in rate limiting)
- **Rate Limit:** 5 images/minute typical
- **Concurrent Requests:** 1-3 (images generate sequentially)

**Prompt Engineering for Artist Agent:**
The Artist agent should include style-specific instructions:
- "In the style of classic Warner Bros. Looney Tunes cartoons"
- "Vibrant colors, exaggerated expressions, dynamic poses"
- "Inspired by Chuck Jones and Wile E. Coyote animation style"

### 5. Publisher Agent (Formatting & Metadata)
**Primary Purpose:** Hugo markdown formatting, front matter generation, SEO optimization

**Recommended Models:**
- **Primary:** GPT-4o Mini (gpt-4o-mini) - Perfect for structured formatting
- **Alternative:** GPT-3.5 Turbo (gpt-3.5-turbo)
- **Advanced:** GPT-4o (if handling complex SEO analysis)

**Rationale:**
- Primarily handles structured formatting tasks
- Requires consistency and accuracy over creativity
- Cost-effective model is sufficient for this role
- Deterministic output is more valuable than creative variation

**Deployment Configuration:**
```yaml
deployment_name: "gpt-4o-mini-publisher"
model: "gpt-4o-mini"
temperature: 0.2  # Very low for consistent formatting
max_tokens: 2000
top_p: 0.9
```

**Azure Foundry Settings:**
- **Capacity:** Standard (formatting doesn't require high throughput)
- **Rate Limit:** 60K tokens/minute
- **Concurrent Requests:** 10-15

### 6. Committer Agent (Git Operations)
**Primary Purpose:** Git repository management and commit operations

**Model Requirements:**
- **No LLM required** - This agent performs programmatic git operations
- Uses Azure DevOps REST API and git commands directly
- No AI model deployment needed

**Note:** The Committer agent doesn't require AI model access as it performs deterministic git operations using Azure DevOps APIs.

## Cost Optimization Strategies

### 1. Tiered Model Deployment
Use different model tiers based on agent criticality:
- **Premium (GPT-4o):** Editor, CopyWriter
- **Standard (GPT-4o Mini):** Researcher, Publisher  
- **Specialized (DALL-E 3):** Artist

### 2. Token Management
```yaml
# Recommended token limits by agent
editor_max_tokens: 2000
researcher_max_tokens: 3000
copywriter_max_tokens: 4000
publisher_max_tokens: 2000
```

### 3. Batch Processing
For multiple blog posts, use the Researcher agent with GPT-4o Mini to process all data files efficiently before invoking more expensive models.

### 4. Caching Strategy
Implement response caching for:
- Common research patterns
- Frequently used formatting templates
- Standard front matter structures

## Performance Benchmarks

### Expected Response Times (Azure AI Foundry)
- **Editor Agent:** 3-5 seconds per orchestration decision
- **Researcher Agent:** 2-4 seconds per data file analysis
- **CopyWriter Agent:** 8-15 seconds per blog post generation
- **Artist Agent:** 10-20 seconds per image generation
- **Publisher Agent:** 1-3 seconds per formatting operation

### Throughput Recommendations
- **Single Blog Post:** ~30-45 seconds end-to-end
- **Batch Processing (10 posts):** ~5-8 minutes
- **Concurrent Agent Operations:** Up to 3 agents in parallel

## Deployment Best Practices

### 1. Multi-Model Deployment
Deploy separate model instances for each agent role:
```bash
# Editor
az ml online-deployment create --name gpt-4o-editor --model gpt-4o

# Researcher  
az ml online-deployment create --name gpt-4o-mini-researcher --model gpt-4o-mini

# CopyWriter
az ml online-deployment create --name gpt-4o-copywriter --model gpt-4o

# Artist
az ml online-deployment create --name dall-e-3-artist --model dall-e-3

# Publisher
az ml online-deployment create --name gpt-4o-mini-publisher --model gpt-4o-mini
```

### 2. Environment Variables
Configure agent-specific model endpoints:
```bash
AZURE_EDITOR_DEPLOYMENT_NAME="gpt-4o-editor"
AZURE_RESEARCHER_DEPLOYMENT_NAME="gpt-4o-mini-researcher"
AZURE_COPYWRITER_DEPLOYMENT_NAME="gpt-4o-copywriter"
AZURE_ARTIST_DEPLOYMENT_NAME="dall-e-3-artist"
AZURE_PUBLISHER_DEPLOYMENT_NAME="gpt-4o-mini-publisher"
```

### 3. Fallback Configuration
Implement model fallback for resilience:
```yaml
editor:
  primary_model: "gpt-4o"
  fallback_model: "gpt-4-turbo"
  
copywriter:
  primary_model: "gpt-4o"
  fallback_model: "gpt-3.5-turbo-16k"
```

## Monitoring and Optimization

### Key Metrics to Track
1. **Token Usage per Agent:** Monitor costs by agent type
2. **Response Latency:** Identify bottlenecks in workflow
3. **Quality Scores:** Editor agent quality assessments
4. **Error Rates:** Model failures or timeout issues

### Azure AI Foundry Monitoring
Use Azure AI Foundry's built-in monitoring to track:
- Request/response logs per deployment
- Token consumption patterns
- Model performance metrics
- Cost breakdown by agent

### Optimization Triggers
Consider model adjustments if:
- **Editor:** Consistently poor quality assessments → Upgrade to GPT-4o
- **Researcher:** Slow data processing → Increase concurrent requests
- **CopyWriter:** Repetitive content → Adjust temperature and penalties
- **Artist:** Style inconsistency → Switch to DALL-E 3 or refine prompts
- **Publisher:** Formatting errors → Lower temperature for consistency

## Agent-Specific Tuning

### Editor Agent Tuning
```python
# System message emphasis
- Emphasize quality criteria in system message
- Provide clear rubrics for content evaluation
- Include examples of high-quality vs. low-quality outputs

# Temperature tuning
- Start with 0.3 for consistency
- Increase to 0.5 if decisions are too rigid
```

### Researcher Agent Tuning
```python
# Data processing optimization
- Use structured output formats (JSON mode)
- Implement data validation in prompts
- Request specific analysis formats

# Batch processing
- Process multiple files in single context when possible
- Use consistent analysis templates
```

### CopyWriter Agent Tuning
```python
# Creativity controls
- Temperature: 0.7-0.9 for varied, engaging content
- Presence penalty: 0.2-0.4 to encourage new topics
- Frequency penalty: 0.3-0.5 to reduce repetition

# Style consistency
- Provide example blog posts in system message
- Use few-shot prompting for tone consistency
- Include brand voice guidelines
```

### Artist Agent Tuning
```python
# Image generation optimization
- Detailed style prompts with specific references
- Consistent composition instructions
- Color palette specifications
- Size optimization based on Hugo requirements

# Prompt templates
- Create reusable prompt templates for common scenes
- A/B test different style descriptions
- Maintain prompt library for successful generations
```

### Publisher Agent Tuning
```python
# Formatting precision
- Very low temperature (0.1-0.2) for deterministic output
- Structured output formats (JSON mode)
- Template-based generation with variable substitution
- Strict validation of Hugo front matter
```

## Security and Compliance

### Content Safety
Enable Azure AI Content Safety for:
- **CopyWriter Agent:** Filter inappropriate content
- **Artist Agent:** Image safety checks
- **Publisher Agent:** Metadata validation

### Data Privacy
- **Researcher Agent:** Handle bird detection data with appropriate privacy controls
- **All Agents:** Ensure no PII in training or logs
- **Azure AI Foundry:** Use managed identity for secure authentication

## Conclusion

Selecting appropriate models for each agent optimizes the Agentic Blog Bird system for:
- **Performance:** Right model for each task
- **Cost:** Efficient use of premium models
- **Quality:** Best results for creative vs. analytical tasks
- **Reliability:** Consistent output with appropriate temperature settings

Regularly review model performance and adjust based on actual usage patterns, cost constraints, and quality requirements.
