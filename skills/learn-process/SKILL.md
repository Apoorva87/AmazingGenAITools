---
name: learn-process
description: Process a raw notes file — fetch URLs, extract concepts, build knowledge graph, suggest learning tools
user_invocable: true
arguments:
  - name: file
    description: "Filename in personal/learning/raw_notes/ (e.g., 'llm-optimization.md')"
    required: true
---

# /learn-process — Ingest and Process Raw Learning Notes

You are the ingestion engine for the Personal Learning OS. Given a raw notes file, you will parse it, fetch referenced content, extract concepts, build a knowledge graph, and suggest learning tools.

## Inputs

- **file**: `$file` — a markdown file located at `personal/learning/raw_notes/$file`

Read the file now. If it does not exist, tell the user and stop.

---

## Step 1: Parse the Raw Notes

Read `personal/learning/raw_notes/$file` and classify every piece of content:

### 1a. Extract URLs

Find all URLs in the file. Classify each by type:

| Pattern | Resource Type |
|---------|--------------|
| `arxiv.org`, `semanticscholar.org`, `openreview.net` | `paper` |
| `youtube.com`, `youtu.be`, `vimeo.com` | `video` |
| `*.edu/course*`, `coursera.org`, `edx.org` | `course` |
| Contains "book" in path, or `amazon.com/dp/` | `book` |
| Everything else (medium.com, blog posts, docs) | `blog` |

### 1b. Extract Personal Annotations

Lines starting with `>` (blockquotes) or `NOTE:` are personal annotations. Collect them with surrounding context (the nearest heading or URL they follow).

### 1c. Extract Free Text

All remaining non-URL, non-annotation text is free-text notes. Group by the nearest heading.

Report what you found:

```
Parsed $file:
  - X URLs found (Y papers, Z blogs, ...)
  - N personal annotations
  - M text sections
```

---

## Step 2: Fetch URL Content

For each URL extracted in Step 1a:

1. **Try the `firecrawl` skill first** (if available) for high-quality extraction.
2. **Fall back to WebFetch** if firecrawl is not available or fails.
3. If both fail, note the URL as "unfetched" and proceed with whatever context the user provided around the URL.

For each successfully fetched URL, keep:
- The page title
- The main body text (first ~3000 words is sufficient)
- Any extracted metadata (authors, date, abstract)

Do NOT block on fetch failures. Log them and move on.

### 2a. Do Targeted Online Research When It Adds Real Value

When the notes mention a paper title, named method, framework, or topic that would benefit from external context, use web search tools to look for a small number of genuinely helpful supporting resources.

Prioritize, in this order:

1. A free, downloadable, complete version of the paper if one is available legally.
2. High-quality explanatory resources such as strong blog posts, official docs, research project pages, lecture notes, or videos/YouTube talks that explain the idea clearly.
3. Other reputable references only if they materially improve understanding.

This research is optional, not mandatory. Do it only when you find something meaningfully useful. Do not pad the output with mediocre links.

When evaluating candidate resources:

- Read enough of the source to verify it is actually helpful, accurate, and substantial.
- Do not rely on titles, snippets, or superficial skimming alone.
- Prefer resources that explain the core idea, assumptions, tradeoffs, examples, or intuition clearly.
- Prefer primary sources and technically strong secondary sources over shallow summaries.
- Keep the set small: a couple of very helpful links is better than many weak ones.

If nothing strong is found, say so briefly and continue without forcing extra links.

---

## Step 3: Understand and Extract Concepts

For **each** piece of content (fetched URL content + free-text sections), analyze and extract:

### 3a. Concept Extraction

For each distinct concept or topic identified, determine:

| Field | Description | Values |
|-------|-------------|--------|
| `id` | URL-safe slug | e.g., `kv-cache`, `attention-mechanism` |
| `name` | Human-readable name | e.g., "KV Cache", "Attention Mechanism" |
| `depth` | How deep this content goes | `intro` / `intermediate` / `research` |
| `subtopics` | List of sub-concept IDs | e.g., `["multi-head-attention", "scaled-dot-product"]` |
| `questions` | 2-4 questions this concept helps answer | e.g., `["How does KV cache reduce inference latency?"]` |
| `tags` | Descriptive tags | e.g., `["llm", "optimization", "inference"]` |
| `cluster` | Which cluster this belongs to | existing cluster ID or suggest a new one |

### 3b. Resource Assessment

For each URL/resource, also determine:

| Field | Description | Values |
|-------|-------------|--------|
| `quality` | Content quality rating | 1-5 integer |
| `quality_reason` | Why this rating | Brief explanation |
| `descriptiveness` | How well it explains its topic | `low` / `medium` / `high` |
| `descriptiveness_reason` | Why this rating | Brief explanation |

### 3c. Relationship Mapping

For each concept, identify relationships to other concepts (both newly extracted and potentially existing in the graph). Use these relationship types:

- `depends_on` — concept A requires understanding concept B first
- `enables` — concept A makes concept B possible
- `extends` — concept A builds on concept B
- `specializes` — concept A is a specific case of concept B
- `related_to` — general association
- `contrasts_with` — concept A is an alternative to or differs from concept B
- `similar_to` — concept A and concept B are closely related approaches

For each relationship, assign a `weight` (0.0-1.0) indicating strength and provide brief `context` explaining the relationship.

---

## Step 4: Build the Knowledge Graph

Use the concept-graph Python module to update the graph. The graph lives at:

```
personal/learning/concept_graph.json
```

The module is at `plugins/concept-graph/`. Run all operations via Bash calling Python.

### 4a. Load the Graph

```bash
python3 -c "
import sys; sys.path.insert(0, 'plugins/concept-graph')
from graph import load
import json
g = load('personal/learning/concept_graph.json')
print(json.dumps(g.get('clusters', {}), indent=2))
"
```

Inspect existing clusters and nodes first so you can assign concepts to existing clusters or create new ones.

### 4b. Create/Update Clusters

For each cluster needed, check if it already exists. If not, create it:

```bash
python3 -c "
import sys; sys.path.insert(0, 'plugins/concept-graph')
from graph import load, save, add_cluster

g = load('personal/learning/concept_graph.json')
g = add_cluster(g, id='CLUSTER_ID', name='CLUSTER_NAME', parent=PARENT_OR_NONE)
save(g, 'personal/learning/concept_graph.json')
print('Cluster added: CLUSTER_ID')
"
```

### 4c. Add Concept Nodes

For each concept extracted in Step 3:

```bash
python3 -c "
import sys; sys.path.insert(0, 'plugins/concept-graph')
from graph import load, save, add_node

g = load('personal/learning/concept_graph.json')
g = add_node(g, {
    'id': 'CONCEPT_ID',
    'name': 'CONCEPT_NAME',
    'type': 'concept',
    'depth': 'DEPTH',
    'subtopics': ['SUB1', 'SUB2'],
    'questions': ['Q1?', 'Q2?'],
    'tags': ['tag1', 'tag2'],
    'clusters': ['CLUSTER_ID'],
    'confidence': 1
})
save(g, 'personal/learning/concept_graph.json')
print('Concept added: CONCEPT_ID')
"
```

### 4d. Add Resource Nodes

For each URL/resource:

```bash
python3 -c "
import sys; sys.path.insert(0, 'plugins/concept-graph')
from graph import load, save, add_node

g = load('personal/learning/concept_graph.json')
g = add_node(g, {
    'id': 'RESOURCE_ID',
    'name': 'RESOURCE_TITLE',
    'type': 'resource',
    'url': 'URL',
    'resource_type': 'paper',
    'quality': 4,
    'quality_reason': 'Well-written with clear examples',
    'descriptiveness': 'high',
    'descriptiveness_reason': 'Covers topic thoroughly with diagrams',
    'source_file': '$file',
    'tags': ['tag1', 'tag2'],
    'clusters': ['CLUSTER_ID'],
    'questions': ['Q1?']
})
save(g, 'personal/learning/concept_graph.json')
print('Resource added: RESOURCE_ID')
"
```

### 4e. Add Note Nodes

For each personal annotation extracted in Step 1b:

```bash
python3 -c "
import sys; sys.path.insert(0, 'plugins/concept-graph')
from graph import load, save, add_node

g = load('personal/learning/concept_graph.json')
g = add_node(g, {
    'id': 'note-SLUG',
    'name': 'Brief title for the note',
    'type': 'note',
    'body': 'The full annotation text',
    'source_file': '$file',
    'tags': ['relevant', 'tags'],
    'clusters': ['CLUSTER_ID']
})
save(g, 'personal/learning/concept_graph.json')
print('Note added: note-SLUG')
"
```

### 4f. Add Edges

Create edges between nodes. Always add nodes before their edges.

**Concept-to-Resource edges** (learned_from):

```bash
python3 -c "
import sys; sys.path.insert(0, 'plugins/concept-graph')
from graph import load, save, add_edge

g = load('personal/learning/concept_graph.json')
g = add_edge(g,
    source='CONCEPT_ID',
    target='RESOURCE_ID',
    relationship='learned_from',
    context='Concept was explained in this resource',
    weight=0.8
)
save(g, 'personal/learning/concept_graph.json')
print('Edge added: CONCEPT_ID -> RESOURCE_ID')
"
```

**Concept-to-Concept edges**:

```bash
python3 -c "
import sys; sys.path.insert(0, 'plugins/concept-graph')
from graph import load, save, add_edge

g = load('personal/learning/concept_graph.json')
g = add_edge(g,
    source='CONCEPT_A',
    target='CONCEPT_B',
    relationship='depends_on',
    context='Why A depends on B',
    weight=0.7
)
save(g, 'personal/learning/concept_graph.json')
print('Edge added: CONCEPT_A -> CONCEPT_B')
"
```

**Important**: Batch your graph operations. You can add multiple nodes and edges in a single Python invocation to reduce overhead. For example:

```bash
python3 -c "
import sys; sys.path.insert(0, 'plugins/concept-graph')
from graph import load, save, add_node, add_edge, add_cluster

g = load('personal/learning/concept_graph.json')

# Add all clusters
g = add_cluster(g, id='cluster-1', name='Cluster One')

# Add all concept nodes
g = add_node(g, {'id': 'concept-1', 'name': 'Concept One', 'type': 'concept', 'clusters': ['cluster-1'], 'tags': ['tag1']})
g = add_node(g, {'id': 'concept-2', 'name': 'Concept Two', 'type': 'concept', 'clusters': ['cluster-1'], 'tags': ['tag2']})

# Add all resource nodes
g = add_node(g, {'id': 'res-1', 'name': 'Resource One', 'type': 'resource', 'url': 'https://...', 'resource_type': 'blog', 'quality': 4, 'descriptiveness': 'high', 'source_file': '$file', 'clusters': ['cluster-1']})

# Add all edges
g = add_edge(g, source='concept-1', target='res-1', relationship='learned_from', weight=0.8)
g = add_edge(g, source='concept-1', target='concept-2', relationship='depends_on', weight=0.7)

save(g, 'personal/learning/concept_graph.json')
print('Graph updated successfully')
"
```

### 4g. Print Graph Stats

After all updates:

```bash
python3 -c "
import sys; sys.path.insert(0, 'plugins/concept-graph')
from graph import load, stats
import json

g = load('personal/learning/concept_graph.json')
print(json.dumps(stats(g), indent=2))
"
```

---

## Step 5: Store Processed Output

Create a processed summary file at:

```
personal/learning/processed/$FILE_STEM-processed.md
```

Where `$FILE_STEM` is the filename without the `.md` extension.

Use this format:

```markdown
# Processed: [Original File Name]

**Source**: personal/learning/raw_notes/$file
**Processed**: [current date/time]
**Concepts extracted**: N
**Resources processed**: N
**Connections created**: N

---

## Concepts

### [Concept Name] (`concept-id`)
- **Depth**: intro / intermediate / research
- **Cluster**: cluster-name
- **Subtopics**: sub1, sub2
- **Key questions**:
  - Question 1?
  - Question 2?
- **Relationships**:
  - depends_on → other-concept
  - related_to → another-concept

---

## Resources

### [Resource Title] (`resource-id`)
- **URL**: https://...
- **Type**: paper / blog / video / book / course
- **Quality**: 4/5 — reason
- **Descriptiveness**: high — reason
- **Teaches concepts**: concept-1, concept-2

---

## Personal Notes

### [Note title] (`note-id`)
- **Context**: What heading/resource this appeared under
- **Body**: The annotation text

---

## New Connections Discovered

- concept-a **depends_on** concept-b — explanation
- concept-c **extends** concept-d — explanation
- ...

---

## Graph Stats (after update)

- Total nodes: X
- Total edges: Y
- Nodes by type: concept=A, resource=B, note=C
- Clusters: list
```

---

## Step 6: Notion Sync

After processing is complete, inform the user:

> The processed content has been saved. You can sync to Notion by running:
> ```
> /learn-sync
> ```

If the `/learn-sync` skill is available, offer to invoke it. Do not auto-invoke without user confirmation.

---

## Step 7: Suggest Learning Tools

For each concept cluster identified, suggest tools from the catalog. Present suggestions interactively for user approval.

### Tool Suggestion Matrix

| When the concept needs... | Suggest |
|---------------------------|---------|
| Audio overview / podcast-style summary | **NotebookLM** — upload the resource and generate an audio overview |
| Academic depth / paper discovery | **Elicit** or **SciSpace** — systematic review or equation understanding |
| Memorization / retention | **Anki** — generate flashcards from the extracted questions |
| Visual mind map | **Mapify** or **XMind** — convert concept relationships into a mind map |
| Knowledge gaps / latest research | **Perplexity** — search for recent developments on weak areas |
| Interactive exploration | **NotebookLM** — multi-doc QA across related resources |
| Code experimentation | **Jupyter/Colab** — hands-on notebook for the concept |

### Suggestion Format

Present suggestions grouped by cluster:

```
## Tool Suggestions

### Cluster: [Cluster Name]

Concepts: concept-1, concept-2, concept-3

| # | Tool | Action | Why |
|---|------|--------|-----|
| 1 | NotebookLM | Upload [resource-1], [resource-2] for audio summary | You have 3 resources on this cluster — an audio overview will consolidate them |
| 2 | Anki | Generate flashcards from extracted questions | 8 questions identified across this cluster |
| 3 | Perplexity | Search "latest developments in [topic]" | Your notes mention this is a fast-moving area |

Would you like me to prepare inputs for any of these? (Enter numbers, or 'skip')
```

Wait for the user to respond before taking any action on tool suggestions.

---

## Final Summary

After all steps, present a summary:

```
## Processing Complete: $file

| Metric | Count |
|--------|-------|
| Concepts extracted | N |
| Resources processed | N |
| Notes captured | N |
| Edges created | N |
| Clusters (new/existing) | X new, Y existing |
| Unfetched URLs | N |

### New concepts added to graph:
- concept-name-1 (cluster: cluster-name)
- concept-name-2 (cluster: cluster-name)

### Key connections discovered:
- concept-a depends_on concept-b
- concept-c extends concept-d

Output saved to: personal/learning/processed/$FILE_STEM-processed.md
```

---

## Error Handling

- **File not found**: Stop and tell the user the file does not exist. List available files in `personal/learning/raw_notes/`.
- **Fetch failure**: Log the URL, note it as unfetched, continue processing with available context.
- **Duplicate node**: If a node ID already exists in the graph, use `update_node` from the graph module instead of `add_node` to merge new information.
- **Duplicate edge**: If an edge already exists (same source, target, relationship), skip it and note it was already present.
- **Empty file**: Stop and tell the user the file is empty.
