# Azure AI Foundry Inventory — `rg-Todd-7349_ai`

> Generated: 2026-06-10
> Subscription: `9b74f21e-b3c6-43af-ac50-a0be4c425cf4`
> Resource group: `rg-Todd-7349_ai`
> Region: `eastus2`

This document captures the current state of the Azure AI Foundry environment: the
agents and their settings, knowledge bases, and data sources. It reflects a live
inventory taken from both the Azure control plane (ARM) and the Foundry/Azure
OpenAI data plane.

## Summary

| Item | Count | Status |
| --- | --- | --- |
| Foundry / hub projects | 0 | No child projects under the hub |
| Agents (assistants) | 0 | None configured |
| Model deployments | 0 | None configured |
| Knowledge bases (vector stores) | 0 | None configured |
| Uploaded files | 0 | None |
| Data sources (connections) | 0 | None configured |

The environment is a freshly provisioned **hub-based** Foundry setup. The
backing resources exist, but no agents, models, knowledge bases, or data
connections have been created yet.

## Foundry environment

### AI Services (Foundry) account

| Property | Value |
| --- | --- |
| Name | `ai-todd8532ai716490062784` |
| Type | `Microsoft.CognitiveServices/accounts` |
| Kind | `AIServices` |
| SKU | `S0` |
| Location | `eastus2` |
| Custom subdomain | `ai-todd8532ai716490062784` |
| Public network access | `Enabled` |
| Managed identity | System-assigned |
| Project management | Disabled (`allowProjectManagement = false`) |

### Hub workspace

| Property | Value |
| --- | --- |
| Name | `todd-8532_ai` |
| Friendly name | `Todd-8532_ai` |
| Type | `Microsoft.MachineLearningServices/workspaces` |
| Kind | `Hub` |
| SKU | `Basic` |
| Location | `eastus2` |
| Managed identity | System-assigned (`principalId: 7461d90b-b433-4574-b31e-a5b841df071f`) |
| Linked storage | `sttodd8532ai716490062784` |
| Linked key vault | `kv-todd8532716490062784` |
| Public network access | `Enabled` |
| High business impact | `false` |

### Endpoints

| API | Endpoint |
| --- | --- |
| AI Foundry API | `https://ai-todd8532ai716490062784.services.ai.azure.com/` |
| Azure AI Model Inference API | `https://ai-todd8532ai716490062784.services.ai.azure.com/` |
| Azure OpenAI | `https://ai-todd8532ai716490062784.openai.azure.com/` |
| Cognitive Services | `https://ai-todd8532ai716490062784.cognitiveservices.azure.com/` |

## Agents

**No agents are currently configured.**

The Azure OpenAI / Foundry Assistants data plane returns an empty collection:

- `GET /openai/assistants` → `0` results
- No agent instructions, tools, model bindings, or tool resources exist to document.

When agents are created, each one will carry settings such as:

- `name` and `description`
- `model` (the deployment the agent runs on — see [Model deployments](#model-deployments))
- `instructions` (system prompt)
- `tools` (e.g. `code_interpreter`, `file_search`, `function`, `bing_grounding`, `azure_ai_search`)
- `tool_resources` (e.g. attached vector stores or file IDs)
- `temperature`, `top_p`, response format, and metadata

> Note: This is distinct from the application-level Python agents in this repo
> (`Editor`, `Researcher`, `CopyWriter`, `Artist`, `Publisher`, `Committer` under
> [src/agents](../src/agents)). Those are orchestrated in code and are documented in
> [docs/ARCHITECTURE.md](ARCHITECTURE.md); they are not Foundry-hosted agents.

## Model deployments

**No model deployments exist.**

- `az cognitiveservices account deployment list` → empty
- Agents and inference calls require at least one deployment (for example a
  `gpt-4o` or `gpt-4o-mini` chat model, or a `text-embedding-3-large` embedding
  model for knowledge bases). None are present.

## Knowledge bases

**No knowledge bases (vector stores) exist.**

- `GET /openai/vector_stores` → `0` results
- `GET /openai/files` → `0` results

A knowledge base in Foundry is typically backed by a **vector store** (for the
`file_search` tool) or an **Azure AI Search** index (for the `azure_ai_search`
tool). Neither a vector store nor an Azure AI Search resource/connection is
present in this environment.

## Data sources

**No data sources (connections) are configured.**

- Hub connections (`Microsoft.MachineLearningServices/workspaces/connections`) → empty

Data sources in Foundry are represented as hub/project **connections** to
external services such as:

- Azure AI Search (for retrieval-augmented generation)
- Azure Blob Storage / Azure Data Lake
- Azure OpenAI or other model providers
- Bing Search (grounding)
- API keys / custom connections

No such connections exist yet. The only storage attached is the hub's default
workspace storage account (`sttodd8532ai716490062784`), which is infrastructure
backing for the hub rather than a queryable agent data source.

## How this inventory was collected

```powershell
# Account, endpoints, project settings
az cognitiveservices account show --name ai-todd8532ai716490062784 -g rg-Todd-7349_ai

# Model deployments
az cognitiveservices account deployment list --name ai-todd8532ai716490062784 -g rg-Todd-7349_ai

# Hub connections (data sources) and child projects
az rest --method get --url "https://management.azure.com/<hub-id>/connections?api-version=2025-09-01"

# Agents, knowledge bases, files (data plane)
$cog = az account get-access-token --resource "https://cognitiveservices.azure.com" --query accessToken -o tsv
Invoke-RestMethod -Uri "https://ai-todd8532ai716490062784.openai.azure.com/openai/assistants?api-version=2024-07-01-preview"    -Headers @{ Authorization = "Bearer $cog" }
Invoke-RestMethod -Uri "https://ai-todd8532ai716490062784.openai.azure.com/openai/vector_stores?api-version=2024-07-01-preview" -Headers @{ Authorization = "Bearer $cog" }
Invoke-RestMethod -Uri "https://ai-todd8532ai716490062784.openai.azure.com/openai/files?api-version=2024-07-01-preview"         -Headers @{ Authorization = "Bearer $cog" }
```

The infrastructure that provisions these resources is defined in
[infra/rg-Todd-7349_ai/main.bicep](../infra/rg-Todd-7349_ai/main.bicep).
