---
name: learn-explore
description: Browse and query the knowledge graph — search concepts, view clusters, find gaps, check recent additions
user_invocable: true
arguments:
  - name: query
    description: Search text, or a mode keyword (clusters, recent, gaps, questions, stats)
    required: false
---

# Learn-Explore Skill

You help the user browse their personal concept graph conversationally. The graph lives at `personal/learning/concept_graph.json` (relative to the repo root). The Python module at `plugins/concept-graph/` provides all operations you need.

## Loading the Graph

Always start by loading the graph with a Python snippet via Bash:

```bash
python3 -c "
import sys, json
sys.path.insert(0, 'plugins/concept-graph')
import graph as G
g = G.load('personal/learning/concept_graph.json')
# ... your query here ...
"
```

Run all Python from the **repo root directory**: `/Users/akarnik/experiments/AmazingGenAITools/.worktrees/learning-os`

If the graph file does not exist yet, `G.load()` returns an empty graph. In that case, tell the user their graph is empty and suggest using `/learn-capture` to add content.

## Modes

Parse the `query` argument to determine the mode. If the argument is empty or absent, show a brief help summary of available modes.

### 1. Text Search (default)

Triggered when the argument is not one of the reserved keywords (`clusters`, `recent`, `gaps`, `questions`, `stats`).

```python
results = G.find_nodes(g, text="<query>")
```

For each result, display:
- **Name** and **type** (concept, resource, idea, note, task)
- **Depth** (for concepts) or **resource_type** (for resources)
- **Tags** and **clusters**
- **Confidence** (for concepts) or **quality** (for resources)
- **Questions** the node answers (if any)
- Number of **connections** (count edges where the node is source or target)

Sort results by relevance: concepts first, then resources, then others. Limit to 15 results but mention total count if more exist.

After showing results, offer: "Want me to dive deeper into any of these? I can show connections, related concepts, or the full node details."

### 2. Clusters — `clusters`

```python
tree = G.get_cluster_tree(g)
stats = G.stats(g)
cluster_sizes = stats["cluster_sizes"]
```

Display the cluster hierarchy as an indented tree. Next to each cluster name, show the concept count from `cluster_sizes`. Example:

```
Machine Learning (12 concepts)
  Transformers (5 concepts)
    Attention Mechanisms (3 concepts)
  Classical ML (4 concepts)
```

If there are no clusters, say so and suggest the user organize concepts into clusters.

### 3. Recent — `recent`

```python
from datetime import datetime, timedelta, timezone
cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
recent = [n for n in g["nodes"].values() if n.get("created", "") >= cutoff]
recent.sort(key=lambda n: n.get("created", ""), reverse=True)
```

Group results by date (just the date portion of the ISO timestamp). For each node show name, type, and tags. If nothing was added in the last 7 days, mention that and show the most recent 5 nodes instead.

### 4. Gaps — `gaps`

Find concept nodes with incomplete representations:

```python
concepts = G.find_nodes(g, type="concept")
gaps = []
for c in concepts:
    reps = c.get("representations", {})
    missing = [k for k, v in reps.items() if v is None]
    if missing:
        gaps.append({"node": c, "missing": missing})
gaps.sort(key=lambda x: len(x["missing"]), reverse=True)
```

Display each gap as:
- **Concept name** — missing: summary, audio, diagram, flashcards (whichever are None)
- Suggest which representation to fill first based on priority: summary > flashcards > diagram > audio

Group by severity: nodes missing 3-4 representations first, then 2, then 1. Offer to help create the missing representations.

### 5. Questions — `questions "<search text>"`

When the argument starts with `questions`, treat everything after it as the search text.

```python
results = G.find_questions(g, "<search_text>")
```

Display each result as:
- **Question** (the matching question text)
- Answered by: **Node name** (node type)

Group by node if multiple questions from the same node match. Offer to explore any of the answering nodes in detail.

### 6. Stats — `stats`

```python
s = G.stats(g)
```

Present the statistics conversationally:
- Total nodes and edges
- Breakdown by node type (concept, resource, task, idea, note)
- Top 5 clusters by size
- Edge relationship distribution
- Graph last updated timestamp from `g["metadata"]["last_updated"]`

## Presentation Guidelines

- Be conversational and helpful, not robotic.
- Use markdown tables or bullet lists depending on what fits best.
- Always mention the total count when truncating results.
- When showing connections for a node, use `G.get_neighbors(g, node_id)` and show the relationship type and direction.
- After every response, suggest a natural next step: exploring a specific node, checking gaps, searching for something related, etc.
- If the graph is empty or very small (< 3 nodes), encourage the user to add content and explain what kinds of things they can capture.
