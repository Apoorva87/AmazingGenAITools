# Concept Graph Design Spec

> Personal Learning OS knowledge graph — the foundation for organizing thoughts, tasks, resources, and ideas.

## Design Decisions

- **Multi-type knowledge graph** — concepts, resources, tasks, ideas, and notes are all first-class nodes
- **Fixed typed edges + freeform annotation** — 14 relationship types for structure/querying, optional `context` field for nuance
- **Multi-membership hierarchical clusters** — nodes can belong to multiple clusters, clusters can nest
- **Simple JSON storage** — dict-based lookups, no database, designed for dozens to low hundreds of nodes
- **Questions field** — concepts and resources track "questions this helps answer" for future lookup
- **Functions, not classes** — graph.py operates on a plain dict. Load, mutate, save.

## Node Types

All nodes share a common base:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Slug identifier (e.g., `flash_attention`) |
| `name` | string | Display name (e.g., "Flash Attention") |
| `type` | enum | `concept`, `resource`, `task`, `idea`, `note` |
| `created` | ISO datetime | When the node was added |
| `updated` | ISO datetime | Last modification time |
| `tags` | string[] | Cross-cutting labels |
| `clusters` | string[] | Cluster IDs this node belongs to |

### concept

Knowledge you're learning about.

| Field | Type | Description |
|-------|------|-------------|
| `depth` | enum | `intro`, `intermediate`, `research` |
| `subtopics` | string[] | Broken-down sub-topics |
| `confidence` | int 1-5 | How well you understand this |
| `representations` | object | `{summary, diagram, audio, flashcards}` — each null or a reference |
| `questions` | string[] | Questions this concept helps answer |

### resource

Materials you learn from.

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | URL of the resource |
| `resource_type` | enum | `paper`, `video`, `blog`, `book`, `course`, `tool` |
| `quality` | int 1-5 | Authority, accuracy, rigor |
| `quality_reason` | string | Why this rating |
| `descriptiveness` | enum | `low`, `medium`, `high` |
| `descriptiveness_reason` | string | Why this rating |
| `source_file` | string | Which raw_notes file this came from |
| `questions` | string[] | Questions this resource helps answer |

### task

Actionable items related to learning.

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | `todo`, `in_progress`, `done`, `blocked` |
| `priority` | enum | `low`, `medium`, `high` |
| `due_date` | ISO date or null | Optional deadline |

### idea

Your own thinking and hypotheses.

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | `seed`, `developing`, `validated`, `archived` |
| `body` | string | Freeform text |

### note

Raw captured material, not yet processed.

| Field | Type | Description |
|-------|------|-------------|
| `body` | string | Raw text |
| `source_file` | string | Which file this came from |

## Edges

Directed connections between any two nodes.

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Source node ID |
| `target` | string | Target node ID |
| `relationship` | enum | One of the 14 fixed types |
| `context` | string or null | Freeform annotation — why this link exists |
| `weight` | float 0-1 | Defaults to 0.5, useful for force-directed layout |
| `created` | ISO datetime | When the edge was created |

### Relationship Types

| Category | Types |
|----------|-------|
| Structural | `part_of`, `contains` |
| Knowledge | `depends_on`, `enables`, `extends`, `specializes` |
| Associative | `related_to`, `contrasts_with`, `similar_to` |
| Provenance | `derived_from`, `learned_from`, `supports` |
| Action | `action_for`, `produces`, `blocked_by` |

**Convention:** Edges are stored in one direction only. Use `part_of` (child → parent), not `contains`. Use `depends_on` (dependent → dependency), not `enables` from the other side. When both directions are meaningful and distinct, both edges may exist. The `contains` and `enables` types exist for cases where the semantics are genuinely different from the inverse.

## Clusters

Organizational containers stored separately from nodes.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Slug identifier |
| `name` | string | Display name |
| `parent` | string or null | Parent cluster ID for hierarchy |
| `created` | ISO datetime | When the cluster was created |

Nodes reference clusters via their `clusters` list. A node can belong to multiple clusters. Clusters can nest via `parent`.

## JSON File Structure

```json
{
  "nodes": {
    "<node_id>": { "...node fields..." }
  },
  "edges": [
    { "source": "...", "target": "...", "relationship": "...", "context": null, "weight": 0.5, "created": "..." }
  ],
  "clusters": {
    "<cluster_id>": { "id": "...", "name": "...", "parent": null, "created": "..." }
  },
  "metadata": {
    "total_nodes": 0,
    "total_edges": 0,
    "last_updated": "..."
  }
}
```

## Python Module: `plugins/concept-graph/`

### Files

- `schema.py` — dataclass definitions for all node types, edges, clusters
- `graph.py` — pure functions operating on a dict
- `requirements.txt` — dependencies (likely none)

### Operations (`graph.py`)

All functions take and return plain dicts. No wrapper classes.

| Function | Signature | Description |
|----------|-----------|-------------|
| `load` | `(path: str) -> dict` | Read JSON file, return graph dict |
| `save` | `(graph: dict, path: str) -> None` | Write graph dict to JSON file |
| `add_node` | `(graph: dict, node: dict) -> dict` | Add node, auto-set timestamps, update metadata |
| `update_node` | `(graph: dict, id: str, fields: dict) -> dict` | Partial update, bump `updated` |
| `remove_node` | `(graph: dict, id: str) -> dict` | Remove node + all its edges |
| `add_edge` | `(graph: dict, source: str, target: str, relationship: str, context: str = None, weight: float = 0.5) -> dict` | Create an edge between two nodes |
| `remove_edge` | `(graph: dict, source: str, target: str, relationship: str = None) -> dict` | Remove edge(s), optionally filtered by relationship |
| `get_node` | `(graph: dict, id: str) -> dict or None` | Lookup by ID |
| `find_nodes` | `(graph: dict, type: str = None, tags: list = None, cluster: str = None, text: str = None) -> list` | Filter/search nodes. `text` does substring match on `name`, `body`, and `tags`. |
| `get_neighbors` | `(graph: dict, id: str, relationship: str = None) -> list` | Connected nodes, optionally filtered by edge type |
| `get_cluster_tree` | `(graph: dict) -> dict` | Hierarchical cluster structure |
| `find_questions` | `(graph: dict, query: str) -> list` | Substring match across nodes' questions fields |
| `add_cluster` | `(graph: dict, id: str, name: str, parent: str = None) -> dict` | Create a cluster, optionally nested under a parent |
| `stats` | `(graph: dict) -> dict` | Counts by type, cluster sizes, edge counts |

### Schema validation

`schema.py` defines dataclasses for type hints and validation, but the graph itself is always a plain dict (JSON-serializable). Dataclasses are used for construction and validation, then converted to dicts via `dataclasses.asdict()`.

## 3D Visualization Compatibility

The graph structure is already compatible with common 3D visualization tools:

- **d3-force-3d / 3d-force-graph**: expects `{nodes: [], links: []}` — trivial transform from our format
- **Cosmograph**: CSV/JSON with node and edge lists
- **Neo4j**: Cypher import from JSON
- **vis.js / sigma.js**: similar node/link JSON format

An `export_for_visualization(graph)` function can produce the format needed by any of these tools. Not part of MVP — add when ready for visualization.

## Integration with Skills

- **`/learn-process`**: Calls `add_node`, `add_edge`, `add_cluster` to build the graph from processed content
- **`/learn-explore`**: Calls `find_nodes`, `get_neighbors`, `find_questions`, `get_cluster_tree`, `stats` to browse
- **`/learn-suggest`**: Reads `representations` field on concept nodes to find gaps
- **`/learn-sync`**: Reads full graph to sync to Notion databases

## Non-Goals

- No database layer — JSON file is sufficient for target scale
- No custom 3D visualization — use existing tools (3d-force-graph, Cosmograph, etc.)
- No real-time sync — batch sync to Notion via skill
- No ML/embeddings for semantic search — simple substring matching for now
