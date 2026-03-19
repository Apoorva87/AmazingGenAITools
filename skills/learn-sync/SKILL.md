---
name: learn-sync
description: Sync the local concept graph to Notion databases (Concepts, Resources, Clusters)
user_invocable: true
arguments:
  - name: mode
    description: "full" for complete sync, "new" for only new items since last sync (default: full)
    required: false
---

# Learn Sync — Concept Graph to Notion

You sync the user's local concept graph to three Notion databases. Follow these instructions precisely.

## 1. Load the Concept Graph

Run this Python snippet to load and inspect the graph:

```python
import sys
sys.path.insert(0, "plugins/concept-graph")
import graph as G

g = G.load("personal/learning/concept_graph.json")
st = G.stats(g)
print(f"Nodes: {st['total_nodes']}, Edges: {st['total_edges']}")
print(f"By type: {st['nodes_by_type']}")
print(f"Clusters: {list(g['clusters'].keys())}")
```

Extract the three collections you need:

```python
concepts = G.find_nodes(g, type="concept")
resources = G.find_nodes(g, type="resource")
clusters = g["clusters"]  # dict of cluster_id -> {id, name, parent, created}
```

## 2. Determine Sync Mode

- If the `mode` argument is `"new"`, read the last sync timestamp from `personal/learning/.last_notion_sync` (ISO-8601 string). Only sync nodes whose `created` or `updated` timestamp is after that value. If the file does not exist, fall back to `"full"`.
- If the `mode` argument is `"full"` or omitted, sync everything.

## 3. Find or Create the Three Notion Databases

Search Notion for each database by name. Use the `Notion:search` skill or `Notion:find` skill:

- **"Learning: Concepts"**
- **"Learning: Resources"**
- **"Learning: Clusters"**

If a database is found, note its ID for later use. If a database is NOT found, tell the user which database(s) are missing and provide instructions:

> I could not find the Notion database "Learning: Concepts". Please create a database with that exact title in your Notion workspace, or tell me which Notion page to create it under and I will attempt to create it for you.

If the user provides a parent page, attempt to create the database using the Notion MCP tools with the schemas described below. Otherwise, wait for the user to confirm.

### Database Schemas

**Learning: Concepts** — properties:
| Property | Type | Notes |
|---|---|---|
| Name | title | Concept name |
| Node ID | rich_text | Graph node ID (used for matching on re-sync) |
| Depth | select | Options: intro, intermediate, research |
| Subtopics | rich_text | Comma-separated list |
| Confidence | number | 1-5 |
| Cluster | rich_text | Cluster name(s), comma-separated |
| Tags | multi_select | One tag per select option |
| Questions | rich_text | Newline-separated list of open questions |
| Related Resources | relation | Relation to "Learning: Resources" DB |
| Created | date | Node created timestamp |
| Updated | date | Node updated timestamp |
| Status | select | Options: active, archived (default: active) |

**Learning: Resources** — properties:
| Property | Type | Notes |
|---|---|---|
| Title | title | Resource name |
| Node ID | rich_text | Graph node ID |
| URL | url | Resource URL |
| Resource Type | select | Options: paper, video, blog, book, course, tool |
| Quality | number | 1-5 |
| Quality Reason | rich_text | Why this quality score |
| Descriptiveness | select | Options: low, medium, high |
| Source File | rich_text | Local file path |
| Linked Concepts | rich_text | Comma-separated concept names |
| Tags | multi_select | |
| Created | date | Node created timestamp |
| Status | select | Options: active, archived (default: active) |

**Learning: Clusters** — properties:
| Property | Type | Notes |
|---|---|---|
| Name | title | Cluster name |
| Cluster ID | rich_text | Graph cluster ID |
| Parent Cluster | rich_text | Parent cluster name (if any) |
| Concept Count | number | Number of concepts in this cluster |
| Created | date | Cluster created timestamp |

## 4. Sync Logic

Process each collection in order: Clusters first (no dependencies), then Concepts, then Resources (so relations can be wired up).

### For each item (concept, resource, or cluster):

1. **Query the Notion database** for a row where "Node ID" (or "Cluster ID" for clusters) matches the item's `id`. Use `Notion:database-query` with a filter on the rich_text property.

2. **If a matching row exists:**
   - Compare fields. If any field has changed, update the row using `Notion:update-page` or equivalent.
   - If nothing changed, skip it.
   - Track this as "updated" or "skipped" in your summary.

3. **If no matching row exists:**
   - Create a new row using `Notion:create-database-row`.
   - Track this as "new" in your summary.

4. **Archived nodes:** If running in `"full"` mode, after processing all items, query the Notion database for rows whose "Node ID" does NOT appear in the current graph. Set their "Status" property to "archived". Do NOT delete them.

### Field Mapping Details

**Concepts:**
- `name` -> Name (title)
- `id` -> Node ID
- `depth` -> Depth (select)
- `subtopics` -> Subtopics (join with ", ")
- `confidence` -> Confidence (number)
- `clusters` -> Cluster: look up cluster names from `g["clusters"]`, join with ", "
- `tags` -> Tags (multi_select)
- `questions` -> Questions (join with "\n")
- `created` -> Created (date)
- `updated` -> Updated (date)
- Related Resources: find neighbors with `G.get_neighbors(g, node_id)` where neighbor type is "resource", then look up their Notion page IDs from the Resources DB rows you already synced.

**Resources:**
- `name` -> Title (title)
- `id` -> Node ID
- `url` -> URL (url)
- `resource_type` -> Resource Type (select)
- `quality` -> Quality (number)
- `quality_reason` -> Quality Reason
- `descriptiveness` -> Descriptiveness (select)
- `source_file` -> Source File
- Linked Concepts: find neighbors with `G.get_neighbors(g, node_id)` where neighbor type is "concept", join names with ", "
- `tags` -> Tags (multi_select)
- `created` -> Created (date)

**Clusters:**
- `name` -> Name (title)
- `id` -> Cluster ID
- `parent` -> Parent Cluster: look up parent name from `g["clusters"]` if parent is set
- Concept Count: count nodes where `cluster_id in node["clusters"]`
- `created` -> Created (date)

## 5. Write the Sync Timestamp

After a successful sync, write the current UTC ISO-8601 timestamp to `personal/learning/.last_notion_sync`:

```python
from datetime import datetime, timezone
ts = datetime.now(timezone.utc).isoformat()
with open("personal/learning/.last_notion_sync", "w") as f:
    f.write(ts)
```

## 6. Print Summary

Display a summary table to the user:

```
Notion Sync Complete
====================
Mode: full

| Database            | New | Updated | Skipped | Archived |
|---------------------|-----|---------|---------|----------|
| Learning: Concepts  |   5 |       2 |      10 |        0 |
| Learning: Resources |   3 |       1 |       7 |        0 |
| Learning: Clusters  |   2 |       0 |       1 |        0 |

Timestamp: 2026-03-19T12:00:00+00:00
```

## Error Handling

- If the Notion MCP server is not available, tell the user: "The Notion MCP server does not appear to be connected. Please ensure it is configured and try again."
- If a database is not found and you cannot create it, list exactly which databases are missing and stop.
- If an individual row fails to sync, log the error, continue with the remaining rows, and include the failure count in the summary.
- Never delete Notion rows. Only archive by setting Status to "archived".
