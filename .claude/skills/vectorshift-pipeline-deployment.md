---
name: deploy-pipeline
description: Deploy or update a VectorShift pipeline. Use this when iterating on pipelines, deploying new versions, updating the registry, or troubleshooting deployment issues.
---

# VectorShift Pipeline Iteration & Deployment Guide

## Overview

This skill covers how to iterate on and deploy VectorShift pipelines in this codebase. The codebase uses a structured approach with:
- Pipeline definitions in `vs_pipelines/`
- Prompt templates in `prompts/{pipeline_name}/`
- A central registry in `vs_pipelines/registry.py`

## Key Files

| Location | Purpose |
|----------|---------|
| `vs_pipelines/{name}.py` | Pipeline definition (nodes, connections, configuration) |
| `prompts/{name}/*.md` | Prompt templates for LLM nodes |
| `vs_pipelines/registry.py` | Central registry of all pipeline IDs and metadata |
| `vs_pipelines/config.py` | Shared configuration (API keys, file references, `load_prompt()`) |
| `cli/create_{name}.py` | CLI script to deploy the pipeline |

## Valid Model Names Reference

**CRITICAL:** Always use exact model IDs from this table. Do NOT use informal names like "Gemini 2.0 Flash" - use `gemini-2.0-flash-exp`.

### Google/Gemini Models

| Model ID | Context | Use Case |
|----------|---------|----------|
| `gemini-2.0-flash-exp` | 1M tokens | Fast extraction, large docs (RECOMMENDED for extractors) |
| `gemini-2.0-flash-001` | 1M tokens | Stable 2.0 Flash |
| `gemini-2.0-flash-thinking-exp` | 1M tokens | Reasoning with thinking |
| `gemini-1.5-pro` | 2M tokens | Complex reasoning, largest context |
| `gemini-1.5-flash` | 1M tokens | Fast, cost-effective |
| `gemini-3-pro-preview` | - | Latest preview model |

### Anthropic/Claude Models

| Model ID | Use Case |
|----------|----------|
| `claude-opus-4-5-20251101` | Most capable, complex tasks |
| `claude-haiku-4-5-20251001` | Fast, lightweight tasks |
| `claude-3-5-sonnet-20241022` | Strong reasoning |
| `claude-3-5-haiku-20241022` | Fast Claude 3.5 |
| `claude-3-opus-20240229` | Previous flagship |

### Perplexity/Sonar Models

| Model ID | Use Case |
|----------|----------|
| `sonar-deep-research` | Web research with citations (ASYNC) |
| `sonar-reasoning-pro` | Reasoning with visible thinking |
| `sonar-pro` | Standard web search |
| `llama-3.1-sonar-huge-128k-online` | Large context online search |

### OpenAI Models

| Model ID | Use Case |
|----------|----------|
| `gpt-4o` | Flagship multimodal |
| `gpt-4o-mini` | Cost-effective |
| `o1` | Advanced reasoning |
| `o1-mini` | Fast reasoning |
| `o3-mini` | Latest fast reasoning |
| `gpt-4-turbo` | Previous flagship |

### Provider Names

```python
provider="google"      # For Gemini models
provider="anthropic"   # For Claude models
provider="perplexity"  # For Sonar models
provider="openai"      # For GPT/O-series models
```

## Critical Rules

### 1. Escape Curly Braces in Prompts

Prompt templates use Python's `.format()` method. Any curly braces `{}` that are NOT template variables must be doubled:

```markdown
# WRONG - will cause KeyError
```json
{
  "title": "Example"
}
```

# CORRECT - escaped for .format()
```json
{{
  "title": "Example"
}}
```
```

**Common places this matters:**
- JSON examples in prompts
- Code blocks showing JSON structure
- Any literal `{` or `}` characters

### 2. Updating Existing Pipelines (Now Works!)

The VectorShift API's `pipeline.save()` method **CAN work** for in-place updates. Previously documented as unreliable, but testing shows it works when done correctly.

#### Successful Update Pattern

```python
import vectorshift
from vectorshift.pipeline import Pipeline, InputNode, LlmNode, OutputNode
from vs_pipelines.config import VECTORSHIFT_API_KEY

vectorshift.api_key = VECTORSHIFT_API_KEY

# 1. Create all nodes with STRINGS (not bytes!)
my_input = InputNode(
    node_name="my_input",
    dependencies=[""],      # String, NOT b""
    file_parser="default",
)

my_llm = LlmNode(
    node_name="MyLLM",
    model="gpt-5.2",
    provider="openai",
    finetuned_model="",     # String, NOT b""
    deployment_id="",       # String, NOT b""
    base_url="",            # String, NOT b""
    api_key="",             # String, NOT b""
    endpoint="",            # String, NOT b""
    json_schema="",         # String, NOT b""
    dependencies=[""],      # String, NOT b""
    # ... other params
)

my_output = OutputNode(
    node_name="my_output",
    value=my_llm.response,
    dependencies=[""],      # String, NOT b""
)

# 2. Fetch existing pipeline
pipeline = Pipeline.fetch(id="YOUR_PIPELINE_ID")

# 3. Replace nodes
pipeline.nodes = [my_input, my_llm, my_output]

# 4. Save - this DOES work!
result = pipeline.save()
print(f"Save result: {result}")  # {'status': 'success'}
```

#### Critical Pitfall: Bytes vs Strings

The **#1 cause of update failures** is using bytes literals (`b""`) instead of strings (`""`):

```python
# WRONG - causes TypeError: Object of type bytes is not JSON serializable
dependencies=[b""],
finetuned_model=b"",

# CORRECT - use strings
dependencies=[""],
finetuned_model="",
```

This error happens **before** the API call, so it looks like a local issue, not an API issue.

#### When to Update vs Create New

| Scenario | Recommendation |
|----------|----------------|
| Simple model/param change | Update existing (`pipeline.save()`) |
| Quick iteration during dev | Update existing |
| Major structural changes | Create new pipeline |
| Production deployment | Create new (for rollback safety) |
| Adding new nodes | Can update, but test carefully |

#### Fallback: Create New Pipeline

If `pipeline.save()` fails with a 500 error (can still happen for some pipelines), create a new one:

```python
# Fallback if save() fails
pipeline = Pipeline.new(
    name="Pipeline Name v2",
    nodes=nodes,
)
```

### 3. Use Unique, Descriptive Pipeline Names

When deploying, use names that indicate the version and changes:
- `"Individual Lecture JSON v2 (Optimized KB + Structured Input)"`
- `"Longevity Research Assistant V7"`

### 4. Update the Registry After Deployment

After successful deployment, update `vs_pipelines/registry.py`:

1. Add new pipeline entry with the new ID
2. Mark previous version as `DEPRECATED`
3. Set `supersedes` to link versions

```python
"my_pipeline": PipelineInfo(
    name="My Pipeline v2",
    id="NEW_PIPELINE_ID_HERE",
    module="vs_pipelines.my_pipeline",
    status=PipelineStatus.ACTIVE,
    version="v2",
    description="Description of changes",
    supersedes="OLD_PIPELINE_ID",
),

"my_pipeline_v1": PipelineInfo(
    name="My Pipeline v1",
    id="OLD_PIPELINE_ID",
    status=PipelineStatus.DEPRECATED,
    ...
),
```

## Adding a New Node

### Step 1: Load the Prompt Template (if needed)

```python
# In build_pipeline():
my_new_template = load_prompt("pipeline_name/my_new_prompt.md")
```

### Step 2: Create the Prompt with Variable Substitution

```python
# For prompts using .format():
my_prompt = my_template.format(
    input_var=some_node.response,
    other_var=other_node.text,
)

# For prompts using .replace() (when you have {{placeholders}}):
my_prompt = my_template.replace(
    "{{placeholder}}", f"{some_node.response}"
)
```

### Step 3: Define the Node

```python
MyNewNode = LlmNode(
    id="MyNewNode",           # Unique ID (required for stable references)
    node_name="MyNewNode",    # Display name in VectorShift UI
    provider="anthropic",     # or "google", "perplexity", etc.
    model="claude-haiku-4-5-20251001",
    max_tokens=2048,
    temperature=0.3,
    json_response=True,       # Set True if expecting JSON output
    use_personal_api_key=False,
    dependencies=[""],
    system="System prompt here",
    prompt=my_prompt,
    # ... other required fields
)
```

### Step 4: Add to Nodes List

```python
nodes = [
    # Inputs
    input_node_1,
    input_node_2,
    # Processing nodes (order matters for dependencies)
    ExtractContext,
    MyNewNode,        # Add in correct position
    NextNode,
    # Outputs
    output_node_1,
]
```

### Step 5: Create Output Node (if exposing the output)

```python
my_output = OutputNode(
    id="my_output",
    node_name="my_output",
    dependencies=[""],
    value=MyNewNode.response,
)
```

## Node Attribute Reference

| Node Type | Common Attributes |
|-----------|-------------------|
| InputNode | `.text`, `.processed_text`, `.processed_texts` (for vec<file>) |
| LlmNode | `.response` |
| KnowledgeBaseNode | `.formatted_text`, `.chunks` |
| FileNode | `.processed_text` |
| YoutubeNode | `.output` |

## Deployment Workflow

### 1. Make Changes

Edit the pipeline file and/or prompt templates.

### 2. Test Locally (Syntax Check)

```bash
cd /Users/anantvinjamoori/Vectorshift\ Pipelines
python3 -c "from vs_pipelines.my_pipeline import build_pipeline; print('Syntax OK')"
```

### 3. Deploy

```bash
python3 -c "
from vs_pipelines.my_pipeline import build_pipeline
pipeline = build_pipeline(name='My Pipeline v2')
print(f'Pipeline ID: {pipeline.id}')
"
```

### 4. Verify

```bash
python3 -c "
import vectorshift
from vectorshift.pipeline import Pipeline
from vs_pipelines.config import VECTORSHIFT_API_KEY

vectorshift.api_key = VECTORSHIFT_API_KEY
pipeline = Pipeline.fetch(id='NEW_PIPELINE_ID')
print(f'Nodes: {len(pipeline.nodes)}')
"
```

### 5. Update Registry

Edit `vs_pipelines/registry.py` with the new pipeline ID.

## Parallelization Patterns

Parallelization is a critical optimization strategy for VectorShift pipelines. Use parallel architectures when encountering:

1. **Exceptionally long prompts** (>4000 tokens)
2. **High risk of context window saturation** (multi-axis analysis, comprehensive reports)
3. **Large file inputs** (50+ page PDFs, multiple source documents)
4. **Extensive vector database search results** (multiple KB queries)

### When to Parallelize

| Signal | Problem | Solution |
|--------|---------|----------|
| Pipeline timeout | LLM node taking >90s | Split into parallel workers |
| Degraded output quality | Model attention degrading on long outputs | Focused workers with merger |
| Large KB results | Too much context from vector search | Parallel KB queries + merge |
| Multi-axis analysis | Single model analyzing 10+ dimensions | Split by domain/axis groups |

### Parallel Worker Pattern

Split a large analysis task across multiple workers, then merge results:

```
                    ┌─────────────────────┐
                    │   Input (Data)      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐
    │  Worker A       │ │  Worker B       │ │ Worker C     │
    │  (Domain 1-3)   │ │  (Domain 4-6)   │ │  (Domain 7+) │
    └────────┬────────┘ └────────┬────────┘ └──────┬───────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 ▼
                    ┌─────────────────────┐
                    │  Merger Node        │
                    └─────────────────────┘
```

**Implementation:**

```python
# Worker A: Focused on subset of analysis
worker_a = LlmNode(
    id="worker_a",
    node_name="worker_a",
    provider="anthropic",
    model="claude-sonnet-4-20250514",  # Fast, capable for focused analysis
    max_tokens=16000,  # Smaller output = faster
    temperature=0.3,
    dependencies=[""],  # No dependency on other workers = PARALLEL
    system="You analyze domains 1-3 only.",
    prompt=worker_a_prompt.format(input=input_node.text),
)

# Worker B: Different subset, runs IN PARALLEL with Worker A
worker_b = LlmNode(
    id="worker_b",
    node_name="worker_b",
    provider="anthropic",
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    temperature=0.3,
    dependencies=[""],  # No dependency = PARALLEL execution
    system="You analyze domains 4-6 only.",
    prompt=worker_b_prompt.format(input=input_node.text),
)

# Merger: Waits for both workers, synthesizes results
merger = LlmNode(
    id="merger",
    node_name="merger",
    provider="anthropic",
    model="claude-sonnet-4-20250514",
    max_tokens=24000,
    temperature=0.4,  # Slightly higher for creative synthesis
    dependencies=[""],
    system="You synthesize parallel analyses into a cohesive report.",
    prompt=merger_prompt.format(
        worker_a_output=worker_a.response,  # Dependency creates correct ordering
        worker_b_output=worker_b.response,
    ),
)
```

### Parallel KB Search Pattern

Run multiple knowledge base searches in parallel:

```python
# Search KB 1 (e.g., Protocols)
kb_protocols = KnowledgeBaseNode(
    id="kb_protocols",
    query=query_generator.response,
    dependencies=[""],
)

# Search KB 2 (e.g., Research) - runs IN PARALLEL
kb_research = KnowledgeBaseNode(
    id="kb_research",
    query=query_generator.response,
    dependencies=[""],
)

# Combine results
kb_merge = MergeNode(
    id="kb_merge",
    function="join",
    fields=[
        f"## Protocol Insights\n{kb_protocols.formatted_text}",
        f"## Research Insights\n{kb_research.formatted_text}",
    ],
)
```

### Parallel File Processing Pattern

For large file inputs, split extraction across parallel workers:

```python
# File input (multi-file)
source_files = InputNode(
    id="source_files",
    input_type="vec<file>",
    file_parser="default",
)

# Extractor 1: First batch of files
extractor_1 = LlmNode(
    id="extractor_1",
    model="gemini-3-flash-preview",  # Large context for file processing
    prompt=f"Extract from files 1-10:\n{source_files.processed_texts[:10]}",
    dependencies=[""],
)

# Extractor 2: Second batch - PARALLEL
extractor_2 = LlmNode(
    id="extractor_2",
    model="gemini-3-flash-preview",
    prompt=f"Extract from files 11-20:\n{source_files.processed_texts[10:20]}",
    dependencies=[""],
)

# Combiner merges all extractions
combiner = LlmNode(
    id="combiner",
    prompt=combiner_prompt.format(
        batch_1=extractor_1.response,
        batch_2=extractor_2.response,
    ),
)
```

### Model Selection for Parallelization

| Role | Recommended Model | Rationale |
|------|-------------------|-----------|
| Workers | `claude-sonnet-4-20250514` | Fast, capable, good for focused tasks |
| Merger | `claude-sonnet-4-20250514` | Good reasoning for synthesis |
| Extractors | `gemini-3-flash-preview` | 1M context, fast, cost-effective |
| Complex Synthesis | `claude-opus-4-5-20251101` | When synthesis requires deep reasoning |

### Prompt Design for Parallelization

**Worker prompts should:**
- Explicitly state which domains/axes the worker handles
- Produce structured output (consistent sections)
- Be self-contained (not reference other workers)
- Output 1500-2000 words (not 4000+)

**Merger prompts should:**
- Accept outputs from all workers as inputs
- Focus on SYNTHESIS, not repetition
- Identify cross-domain connections
- Prioritize and consolidate recommendations

**Example Worker Prompt Structure:**
```markdown
You analyze AXES 1-5 ONLY. Another worker handles Axes 6-10.

Your assigned axes:
1. Axis Name - description
2. ...
5. ...

For EACH axis, provide:
### AXIS [N]: [Name]
**Status**: [Active/Suppressed/Optimal]
**Evidence**: [biomarker values]
**Interpretation**: [mechanistic analysis]
**Interventions**: [targeted recommendations]

Total output: 1500-2000 words across all 5 axes.
```

**Example Merger Prompt Structure:**
```markdown
You have received parallel analyses:
- Worker A: Axes 1-5
- Worker B: Axes 6-10

Your task: SYNTHESIZE (not copy) into unified report.

Output sections:
1. Executive Summary (cross-domain patterns)
2. Integrated Map (connections between axes)
3. Prioritized Interventions (non-redundant)
4. Monitoring Plan
```

### Case Study: Patient Lab Report v4.1

**Problem:** v4 (monolithic) was timing out at the base_report node. Single LLM analyzing 10 cell signaling axes with 4000+ word output.

**Solution:** v4.1 parallel architecture
- Worker A: Axes 1-5 (Metabolic & Hormonal)
- Worker B: Axes 6-10 (Structural & Defense)
- KB Enrichment: runs in parallel with workers
- Merger: synthesizes all outputs

**Results:**
- No more timeouts
- Better attention quality per worker
- Faster overall execution (parallelism)
- More structured output

## Common Patterns

### QueryGenerator Pattern (for KB Optimization)

Instead of sending raw context to KnowledgeBaseNode, use an intermediate LLM to generate optimized queries:

```python
# Generate optimized queries
QueryGenerator = LlmNode(
    id="QueryGenerator",
    provider="anthropic",
    model="claude-haiku-4-5-20251001",
    temperature=0.3,
    json_response=True,
    prompt=query_gen_prompt,
)

# Use optimized queries for KB search
KBSearch = KnowledgeBaseNode(
    query=QueryGenerator.response,  # Instead of raw context
    ...
)
```

### Structured Input Pattern

Allow users to provide structured markdown or JSON input that gets parsed by the first LLM:

```markdown
## INPUT FORMATS

### Format A: Simple
Just a title or identifier.

### Format B: Structured Markdown
# Title
...
## Outline
- ...
## Description
...

### Format C: JSON (escaped for .format())
{{
  "title": "...",
  "outline": [...],
  "description": "..."
}}
```

### Required Slide Pattern

Force the LLM to always include a specific slide (like references):

```markdown
13. ALWAYS INCLUDE REFERENCES SLIDE: The LAST slide must be a references slide

═══════════════════════════════════════════════════════════════
REQUIRED: REFERENCES SLIDE (MUST BE LAST SLIDE)
═══════════════════════════════════════════════════════════════

The LAST slide in every lecture MUST be a references slide with this structure:
{{
  "id": "references",
  ...
}}
```

## Output Retrieval Fallback Pattern

When pipeline execution completes in VectorShift but output capture fails locally (common with long-running pipelines or interrupted processes), use the **task ID fallback** to retrieve results automatically.

### Key Update: Task ID = Span ID

**VectorShift confirmed:** The `task_id` (or `run_id`) returned when you submit a pipeline job can be used directly in place of `span_id` to query results. This eliminates the need to manually visit the VectorShift UI to fetch span IDs.

```
task_id from submission response == span_id for status queries
```

### When the Fallback Triggers

- Agent timed out waiting for results (>10 minutes of no detected output)
- Background process was interrupted (exit code 137)
- SSL/network issues caused output loss
- Pipeline shows "completed" in UI but local script didn't capture output

### Automatic Recovery (No User Intervention Required)

Since `task_id` is available immediately upon job submission, the fallback is now **fully automated**:

```python
import time

def run_pipeline_with_fallback(pipeline_id, inputs, timeout_minutes=10):
    """Run pipeline with automatic task_id fallback on timeout."""

    # Submit job - task_id is returned immediately
    response = submit_pipeline_job(pipeline_id, inputs)
    task_id = response.get("task_id")

    print(f"Job submitted. Task ID: {task_id}")

    # Poll for completion
    start = time.time()
    while (time.time() - start) < timeout_minutes * 60:
        result = poll_job_status(pipeline_id, task_id)
        if result["status"] == "completed":
            return result["result"]
        if result["status"] == "failed":
            raise Exception(result["error"])
        time.sleep(5)

    # Timeout - use task_id directly (no UI visit needed!)
    print(f"\nPipeline timed out after {timeout_minutes} minutes.")
    print(f"Attempting automatic recovery using task_id: {task_id}")

    # Automatic fallback - task_id works as span_id
    result = fetch_pipeline_result_by_task_id(pipeline_id, task_id)
    if result["status"] == "completed":
        print("✓ Recovery successful!")
        return result["result"]
    elif result["status"] == "in_progress":
        print("Pipeline still running. Re-run fallback later or check VectorShift UI.")
    else:
        print(f"Pipeline failed: {result.get('error', 'Unknown error')}")

    return None
```

### Using the CLI Fallback

```bash
cd /Users/anantvinjamoori/Vectorshift\ Pipelines

# Use task_id directly (same as span_id)
python3 cli/fetch_by_span_id.py <PIPELINE_ID> <TASK_ID>

# Save results to files
python3 cli/fetch_by_span_id.py <PIPELINE_ID> <TASK_ID> --output-dir ./output

# Use registry key instead of pipeline ID
python3 cli/fetch_by_span_id.py every_newsletter_generator_v2 <TASK_ID>

# Output raw JSON
python3 cli/fetch_by_span_id.py <PIPELINE_ID> <TASK_ID> --json
```

### Using the Python Utility

```python
from vs_pipelines.config import fetch_pipeline_result_by_span_id

# task_id works directly - no need to get span_id from UI
task_id = "6961e088862a01eeb682196b"  # From job submission response

result = fetch_pipeline_result_by_span_id(
    pipeline_id="6967e132451a2ec1a57fb7da",
    span_id=task_id  # task_id works here!
)

# Check status
if result["status"] == "completed":
    html_output = result["result"].get("html_output", "")
    diagrams = result["result"].get("diagrams_output", "")
    newsletter = result["result"].get("output_0", "")
elif result["status"] == "failed":
    print(f"Error: {result['error']}")
elif result["status"] == "in_progress":
    print("Still running...")
```

### API Endpoint Reference

```
GET https://api.vectorshift.ai/v1/pipeline/{PIPELINE_ID}/run/status/{TASK_ID}
Authorization: Bearer {VECTORSHIFT_API_KEY}

Response:
{
  "status": "completed" | "failed" | "in_progress",
  "result": {
    "output_0": "...",
    "html_output": "...",
    ...
  },
  "error": null | "error message"
}
```

**Note:** `{TASK_ID}` is the value returned in the `task_id` field when you submit the job. It can be used interchangeably with `span_id` or `run_id`.

### Manual UI Lookup (Rarely Needed)

In rare cases where the task_id was lost (e.g., process crashed before logging), you can still find the span_id in the VectorShift UI:

1. Go to VectorShift UI: https://app.vectorshift.ai
2. Navigate to **Pipelines > [Your Pipeline] > Runs**
3. Find the specific run (recent timestamp)
4. Click to expand run details
5. Copy the **span ID** from the root span

## Troubleshooting

### KeyError on Deploy

**Cause:** Unescaped curly braces in prompt template.

**Fix:** Double all `{` and `}` that aren't template variables.

### TypeError: Object of type bytes is not JSON serializable

**Cause:** Using bytes literals (`b""`) instead of strings (`""`) in node parameters.

**Fix:** Replace all `b""` with `""` in your node definitions:

```python
# WRONG
dependencies=[b""],
finetuned_model=b"",
endpoint=b"",

# CORRECT
dependencies=[""],
finetuned_model="",
endpoint="",
```

**Note:** This error occurs locally before the API call, so it's not a server issue.

### 500 Error on Save

**Cause:** VectorShift API update endpoint sometimes fails for certain pipelines.

**Fix:**
1. First, check for bytes literals (see above)
2. If still failing, create a new pipeline instead of updating

### AttributeError: 'Pipeline' object has no attribute 'name'

**Cause:** The Pipeline object doesn't expose all attributes after creation.

**Fix:** This is benign - the pipeline was created. Use the ID from the output.

### Node Not Receiving Data

**Cause:** Dependencies not correctly wired.

**Fix:** Ensure you access node attributes (`.response`, `.text`) in the prompt format call, not just the node object.

```python
# WRONG - node object, not its output
prompt = template.format(data=my_node)

# CORRECT - access the attribute
prompt = template.format(data=my_node.response)
```

## Checklist for Pipeline Changes

- [ ] Prompt templates have escaped curly braces (`{{` and `}}`)
- [ ] **No bytes literals** - all `b""` replaced with `""`
- [ ] New nodes have unique `id` and `node_name`
- [ ] New nodes are added to `nodes` list in correct order
- [ ] Output nodes created for any new outputs to expose
- [ ] Prompt template loaded with `load_prompt()`
- [ ] Registry updated with new pipeline ID (if creating new)
- [ ] Previous version marked as DEPRECATED (if creating new)
- [ ] Docstring updated with new architecture/features

## Risks of Full Redeployment

When you deploy a "new" pipeline, you're rebuilding EVERYTHING from the Python code.
This means:

1. **All prompts are loaded fresh** - If prompt files changed since last deploy, those changes are included
2. **No diffing** - There's no comparison between old and new pipeline
3. **Silent regressions** - A prompt that was working might now be different

### Common Pitfalls

| Symptom | Likely Cause |
|---------|--------------|
| Output format changed | Wrong prompt file being loaded |
| Feature stopped working | Prompt was modified for another purpose |
| New errors appearing | Escaped braces reverted, or prompt variables changed |

### Example: The Script Prompt Problem

The codebase has TWO script prompts for `individual_lecture_json`:
- `script_gen.md` - Outputs markdown with headers and `[CUE:]` markers
- `voiceover_script.md` - Outputs plain text for ElevenLabs

If the code loads the wrong one, the pipeline "works" but the output is wrong for ElevenLabs.

**This actually happened in v2** - it loaded `script_gen.md` instead of `voiceover_script.md`, breaking the ElevenLabs workflow.

## Pre-Deployment Checklist

Before deploying any pipeline iteration:

### 1. Review All Loaded Prompts
```bash
# Check which prompts the pipeline loads
grep "load_prompt" vs_pipelines/my_pipeline.py
```
Verify each prompt file is the correct version for your use case.

### 2. Compare Against Previous Version
- What was the previous pipeline doing?
- Which prompts was it using?
- What specific changes are you making?

### 3. Test Locally (if possible)
```python
# Verify prompts load without errors
python3 -c "from vs_pipelines.my_pipeline import build_pipeline; print('OK')"
```

### 4. Document Changes
Before deploying, write down:
- [ ] What I'm changing
- [ ] What I'm NOT changing (should stay the same)
- [ ] Expected behavior of each output

### 5. Verify After Deployment
- Run the pipeline with test inputs
- Check EACH output, not just the primary one
- Compare against previous version's output if available

## Prompt File Inventory Pattern

For critical pipelines, maintain a comment block at the top of the pipeline file listing all prompt files:

```python
"""
My Pipeline

PROMPT FILES USED BY THIS PIPELINE:
- extract_context.md      → ExtractContext node
- voiceover_script.md     → ScriptGen node (ElevenLabs-ready)
- lecture_json.md         → LectureJSON node
- perplexity_refs.md      → PerplexityReferences node

WARNING: script_gen.md exists but is NOT used (outputs markdown, not ElevenLabs-ready)
"""
```

This makes it clear which prompts are intentionally used vs. which exist but shouldn't be loaded.

### Why This Matters

When iterating on a pipeline, you might:
1. See `script_gen.md` in the prompts folder
2. Assume it's the right prompt for the ScriptGen node
3. Load it without realizing `voiceover_script.md` was the correct one

The inventory comment prevents this by documenting intent.
