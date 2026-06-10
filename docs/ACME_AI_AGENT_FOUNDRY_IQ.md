# Foundry Agents & Foundry IQ Inventory — `acme-ai-agent`

Documents the live Azure AI Foundry configuration in the **acme-ai-agent** resource group:
Foundry Agent Service agents, Foundry IQ knowledge bases, knowledge sources (data sources),
and the backing Azure AI Search retrieval pipeline (indexes, skillsets, indexers).

- **Subscription:** `9b74f21e-b3c6-43af-ac50-a0be4c425cf4`
- **Captured:** 2026-06-10 (data plane, live)
- **Secrets:** All connection strings / API keys are intentionally **redacted** here; they are
  stored in the live resources and the Key Vault, never in this document.

---

## 1. Foundry Agent Service — Agents

Agents (a.k.a. assistants) are queried per project from the AI Foundry data plane.

| Project | Account | Region | Agents | Vector stores | Project indexes |
|---------|---------|--------|:------:|:-------------:|:---------------:|
| `acme-bird-agent` | `acme-bird-ai` | Australia East | **0** | 0 | 0 |
| `acme-bird-us` | `acme-bird-us-resource` | East US 2 | **0** | 0 | 0 |

> **No persistent Foundry agents are defined in either project.** Consequently there are
> **no agent system prompts / instructions, tools, or model bindings** to document at the
> Agent Service layer. The application-level agents in this repo (`src/agents/*.py`:
> researcher, copywriter, editor, artist, committer, publisher) are **not** Foundry Agent
> Service agents — they are orchestrated in code.

---

## 2. Foundry IQ — Knowledge Base

Foundry IQ knowledge bases are implemented as **knowledge agents** (agentic retrieval) inside
the Azure AI Search service **`acme-bird-agent`** (Australia East, `standard` SKU). The other
two search services (`acme-birdai`, `acme-bird-ai-srch` in Sweden Central) are **empty** — no
indexes, sources, skillsets, indexers, or knowledge agents.

### Knowledge agent: `knowledgebase678`

| Setting | Value |
|---------|-------|
| Name | `knowledgebase678` |
| Description | *(empty)* |
| **Retrieval instructions (prompt)** | *(empty — no custom routing/answer prompt set)* |
| Attached knowledge sources | `acme-bird-events` |
| Source params | `alwaysQuerySource`, `includeReferences`, `maxSubQueries`, `rerankerThreshold` → all default (null) |
| Answer-synthesis models | *(none configured)* |
| Output configuration | *(none)* |
| Request limits | *(none)* |
| Encryption key | Service-managed |

> The knowledge agent currently attaches **only** `acme-bird-events`. The other two knowledge
> sources (`acme-bird-knowledge`, `acme-kb-weather-web`) exist but are **not** wired into this
> knowledge agent. `retrievalInstructions` (the agent's natural-language prompt) is **blank**.

---

## 3. Knowledge Sources (Data Sources)

Three knowledge sources are defined in the `acme-bird-agent` search service. Their
**descriptions are the only natural-language "prompts"** present — agentic retrieval uses them
to decide source relevance/routing.

### 3.1 `acme-bird-events` — Azure Blob
| Setting | Value |
|---------|-------|
| Kind | `azureBlob` |
| Container | `bird-data` |
| Folder path | *(root)* |
| **Description (routing prompt)** | "Bird detection and classification event data from backyard ai sensors and detection stations. Detectors may use audio or video detection methods or a combination of the two." |
| Created pipeline | datasource `acme-bird-events-datasource`, indexer `acme-bird-events-indexer`, skillset `acme-bird-events-skillset`, index `acme-bird-events-index` |
| Connection string | *(redacted)* |

### 3.2 `acme-bird-knowledge` — Azure Blob
| Setting | Value |
|---------|-------|
| Kind | `azureBlob` |
| Container | `reference-info` |
| Folder path | *(root)* |
| **Description (routing prompt)** | "Contains reference information, environmental readings and bird detection data related to Australian birds especially scrub turkeys in Brisbane Australia" |
| Created pipeline | datasource `acme-bird-knowledge-datasource`, indexer `acme-bird-knowledge-indexer`, skillset `acme-bird-knowledge-skillset`, index `acme-bird-knowledge-index` |
| Connection string | *(redacted)* |

### 3.3 `acme-kb-weather-web` — Web
| Setting | Value |
|---------|-------|
| Kind | `web` |
| **Description (routing prompt)** | "web link to enable lookup of current or past weather conditions at a location" |
| Blob/index params | *(none)* |

---

## 4. Backing Retrieval Pipeline (Azure AI Search)

Each blob knowledge source generated a **datasource → skillset → indexer → index** chain.

### 4.1 Indexes

Both `acme-bird-events-index` and `acme-bird-knowledge-index` share an identical shape:

| Field | Type | Attributes |
|-------|------|-----------|
| `uid` | `Edm.String` | key, searchable, sortable, `keyword` analyzer |
| `snippet_parent_id` | `Edm.String` | filterable, retrievable |
| `blob_url` | `Edm.String` | filterable, retrievable |
| `snippet` | `Edm.String` | searchable, retrievable |
| `snippet_vector` | `Collection(Edm.Single)` | searchable, **1536 dims**, vector profile |

| Aspect | Configuration |
|--------|---------------|
| Similarity | BM25 (default `k1`/`b`) |
| Semantic config | default; content field = `snippet` (no title/keyword fields) |
| Vector algorithm | **HNSW** — metric `cosine`, `m=4`, `efConstruction=400`, `efSearch=500` |
| Vector compression | scalar quantization, `int8`, oversampling `4.0`, rerank with original vectors |
| Vectorizer | **Azure OpenAI `text-embedding-3-small`** @ `https://acme-bird-us-resource.openai.azure.com` (1536 dims) |

> The vectorizer points at the **East US 2** account's `text-embedding-3-small` deployment,
> even though the search service is in Australia East.

### 4.2 Skillsets

**`acme-bird-events-skillset`** — `Skillset for knowledge source 'acme-bird-events'`

1. `Microsoft.Skills.Text.SplitSkill` — split content into chunks
   - mode `pages`, **maxPageLength 2000**, **overlap 200**, language `en`
2. `Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill` — `text-embedding-3-small`, 1536 dims
   - source `/document/pages/*` → `text_vector`
- Index projection: `skipIndexingParentDocuments`; maps `snippet_vector`, `snippet`, `blob_url`.
- Cognitive Services: *(none attached)*

**`acme-bird-knowledge-skillset`** — `Skillset for knowledge source 'acme-bird-knowledge'`

1. `Microsoft.Skills.Util.ContentUnderstandingSkill` — `file_data` → `text_sections` + `normalized_images`
2. `Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill` — `text-embedding-3-small`, 1536 dims
   - source `/document/text_sections/*/content` → `text_vector`
- Index projection: `skipIndexingParentDocuments`; maps `snippet_vector`, `snippet`, `blob_url`.
- Cognitive Services: **AI Services by key** (`AIServicesByKey`).

> Neither skillset defines custom LLM prompt skills — there are **no `Microsoft.Skills.Custom`
> or prompt-template skills**, so no free-text prompts exist in the ingestion pipeline.

### 4.3 Indexers

| Setting | `acme-bird-events-indexer` | `acme-bird-knowledge-indexer` |
|---------|----------------------------|-------------------------------|
| Data source | `acme-bird-events-datasource` | `acme-bird-knowledge-datasource` |
| Skillset | `acme-bird-events-skillset` | `acme-bird-knowledge-skillset` |
| Target index | `acme-bird-events-index` | `acme-bird-knowledge-index` |
| Schedule | **daily (`P1D`)** | **daily (`P1D`)** |
| `maxFailedItems` | -1 | -1 |
| Data to extract | `contentAndMetadata` | `contentAndMetadata` |
| Parsing mode | `default` | `default` |
| `allowSkillsetToReadFileData` | `false` | `true` |
| Field mapping | `metadata_storage_path` → `blob_url` | `metadata_storage_path` → `blob_url` |
| Disabled | no | no |

---

## 5. Project Connections (search data source bindings)

Each Foundry project binds to the **same** `acme-bird-agent` search service via a default
connection. (These match the connections reproduced in `infra/acme-ai-agent/main.bicep`.)

| Project | Connection | Type | Auth | Target | Default |
|---------|-----------|------|------|--------|:-------:|
| `acme-bird-agent` (AU) | `acmebirdagent15jhr0` | CognitiveSearch | **AAD** | `https://acme-bird-agent.search.windows.net/` | yes |
| `acme-bird-us` (US) | `acmebirdagentd37uin` | CognitiveSearch | **ProjectManagedIdentity** | `https://acme-bird-agent.search.windows.net/` | yes |

> The US connection uses `ProjectManagedIdentity`. The Bicep template
> (`infra/acme-ai-agent/main.bicep`) models both as `AAD` for deployability, since
> `ProjectManagedIdentity` is not an accepted value in the connection resource's `authType`
> enum. Behaviour is equivalent (keyless / managed-identity).

---

## 6. Summary

| Item | Count / State |
|------|---------------|
| Foundry Agent Service agents | **0** (no prompts/instructions defined) |
| Foundry IQ knowledge agents (KB) | 1 — `knowledgebase678` (empty retrieval prompt; 1 source attached) |
| Knowledge sources (data sources) | 3 — 2 Azure Blob + 1 Web |
| Search indexes | 2 (vector, 1536-dim, HNSW + scalar quantization) |
| Skillsets | 2 (split/content-understanding + AOAI embedding) |
| Indexers | 2 (daily schedule) |
| Project search connections | 2 (one per project, both → `acme-bird-agent`) |
| Embedding model | `text-embedding-3-small` (East US 2 account) |

**Natural-language "prompts" in the system:** only the three knowledge-source *descriptions*
(used for agentic source routing). The knowledge agent's `retrievalInstructions` and
`description` are blank, and no Agent Service agents exist — so there are currently **no system
prompts or agent instructions** configured.
