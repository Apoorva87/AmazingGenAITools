"""Pure functions operating on a concept-graph dict.

The graph dict has the shape::

    {
        "nodes": { "<id>": { ...node fields... }, ... },
        "edges": [ { source, target, relationship, context, weight, created }, ... ],
        "clusters": { "<id>": { id, name, parent, created }, ... },
        "metadata": { "total_nodes": int, "total_edges": int, "last_updated": str }
    }

Every public function takes a graph dict as its first argument and returns
either the (mutated) graph dict or a query result.  No wrapper classes.
"""

from __future__ import annotations

import dataclasses
import json
import os
from typing import Dict, List, Optional

try:
    from .schema import (
        Relationship,
        _NODE_CLASS,
        make_node,
        make_edge,
        make_cluster,
        now_iso as _now_iso,
    )
except ImportError:
    from schema import (  # type: ignore[no-redef]
        Relationship,
        _NODE_CLASS,
        make_node,
        make_edge,
        make_cluster,
        now_iso as _now_iso,
    )


def _refresh_metadata(graph: dict) -> dict:
    graph["metadata"]["total_nodes"] = len(graph["nodes"])
    graph["metadata"]["total_edges"] = len(graph["edges"])
    graph["metadata"]["last_updated"] = _now_iso()
    return graph


def _empty_graph() -> dict:
    return {
        "nodes": {},
        "edges": [],
        "clusters": {},
        "metadata": {
            "total_nodes": 0,
            "total_edges": 0,
            "last_updated": _now_iso(),
        },
    }


# ---------------------------------------------------------------------------
# Load / Save
# ---------------------------------------------------------------------------

def load(path: str) -> dict:
    """Read JSON file, return graph dict. If file doesn't exist, return empty graph."""
    if not os.path.exists(path):
        return _empty_graph()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(graph: dict, path: str) -> None:
    """Write graph dict to JSON file, creating parent directories if needed."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Node operations
# ---------------------------------------------------------------------------

def add_node(graph: dict, node: dict) -> dict:
    """Add a node to the graph.

    *node* must contain at least ``id``, ``name``, and ``type``.
    Timestamps are auto-set.  The node is validated via ``schema.make_node``.
    """
    now = _now_iso()
    node = {**node, "created": node.get("created", now), "updated": now}
    validated = make_node(node)
    graph["nodes"][validated["id"]] = validated
    return _refresh_metadata(graph)


def update_node(graph: dict, id: str, fields: dict) -> dict:
    """Partial update of an existing node. Bumps ``updated``.

    Raises ValueError if *fields* contains unknown field names for the node's
    type, or if *fields* attempts to change the node's ``type``.
    """
    if id not in graph["nodes"]:
        raise KeyError(f"Node not found: {id}")
    existing = graph["nodes"][id]

    # Reject type changes.
    if "type" in fields and fields["type"] != existing["type"]:
        raise ValueError(
            f"Cannot change node type from '{existing['type']}' to '{fields['type']}'"
        )

    # Reject unknown fields.
    node_type = existing["type"]
    cls = _NODE_CLASS[node_type]
    valid_fields = {f.name for f in dataclasses.fields(cls)}
    unknown = set(fields) - valid_fields
    if unknown:
        raise ValueError(
            f"Invalid field(s) for node type '{node_type}': {sorted(unknown)}"
        )

    existing.update(fields)
    existing["updated"] = _now_iso()
    # Re-validate the merged node
    graph["nodes"][id] = make_node(existing)
    return _refresh_metadata(graph)


def remove_node(graph: dict, id: str) -> dict:
    """Remove a node and all edges that reference it."""
    if id not in graph["nodes"]:
        raise KeyError(f"Node not found: {id}")
    del graph["nodes"][id]
    graph["edges"] = [
        e for e in graph["edges"] if e["source"] != id and e["target"] != id
    ]
    return _refresh_metadata(graph)


def get_node(graph: dict, id: str) -> Optional[dict]:
    """Lookup a node by ID, return None if not found."""
    return graph["nodes"].get(id)


# ---------------------------------------------------------------------------
# Edge operations
# ---------------------------------------------------------------------------

def add_edge(
    graph: dict,
    source: str,
    target: str,
    relationship: str,
    context: Optional[str] = None,
    weight: float = 0.5,
) -> dict:
    """Create an edge between two existing nodes.

    Raises ValueError if an edge with the same source, target, and relationship
    already exists.
    """
    if source not in graph["nodes"]:
        raise KeyError(f"Source node not found: {source}")
    if target not in graph["nodes"]:
        raise KeyError(f"Target node not found: {target}")
    for e in graph["edges"]:
        if e["source"] == source and e["target"] == target and e["relationship"] == relationship:
            raise ValueError(
                f"Duplicate edge: {source} --[{relationship}]--> {target} already exists"
            )
    edge_data = {
        "source": source,
        "target": target,
        "relationship": relationship,
        "context": context,
        "weight": weight,
    }
    validated = make_edge(edge_data)
    graph["edges"].append(validated)
    return _refresh_metadata(graph)


def remove_edge(
    graph: dict,
    source: str,
    target: str,
    relationship: Optional[str] = None,
) -> dict:
    """Remove edge(s) matching source+target, optionally filtered by relationship."""
    def _keep(e: dict) -> bool:
        if e["source"] != source or e["target"] != target:
            return True
        if relationship is not None and e["relationship"] != relationship:
            return True
        return False

    graph["edges"] = [e for e in graph["edges"] if _keep(e)]
    return _refresh_metadata(graph)


# ---------------------------------------------------------------------------
# Query operations
# ---------------------------------------------------------------------------

def find_nodes(
    graph: dict,
    type: Optional[str] = None,
    tags: Optional[List[str]] = None,
    cluster: Optional[str] = None,
    text: Optional[str] = None,
) -> list:
    """Filter/search nodes.

    - *type*: filter by node type
    - *tags*: nodes must have ALL listed tags
    - *cluster*: node must belong to this cluster
    - *text*: substring match (case-insensitive) on name, body, and tags
    """
    results = []
    text_lower = text.lower() if text else None

    for node in graph["nodes"].values():
        if type is not None and node.get("type") != type:
            continue
        if tags is not None and not all(t in node.get("tags", []) for t in tags):
            continue
        if cluster is not None and cluster not in node.get("clusters", []):
            continue
        if text_lower is not None:
            searchable = " ".join([
                node.get("name", ""),
                node.get("body", ""),
                " ".join(node.get("tags", [])),
            ]).lower()
            if text_lower not in searchable:
                continue
        results.append(node)
    return results


def get_neighbors(
    graph: dict,
    id: str,
    relationship: Optional[str] = None,
) -> list:
    """Return nodes connected to *id*, optionally filtered by edge relationship.

    Considers edges in both directions (id as source or target).
    """
    neighbor_ids: list[str] = []
    for e in graph["edges"]:
        if relationship is not None and e["relationship"] != relationship:
            continue
        if e["source"] == id:
            neighbor_ids.append(e["target"])
        elif e["target"] == id:
            neighbor_ids.append(e["source"])
    return [graph["nodes"][nid] for nid in neighbor_ids if nid in graph["nodes"]]


def find_questions(graph: dict, query: str) -> list:
    """Substring match across nodes' questions fields.

    Returns a list of dicts with ``node_id``, ``node_name``, and ``question``.
    """
    query_lower = query.lower()
    results = []
    for node in graph["nodes"].values():
        for q in node.get("questions", []):
            if query_lower in q.lower():
                results.append({
                    "node_id": node["id"],
                    "node_name": node["name"],
                    "question": q,
                })
    return results


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------

def add_cluster(
    graph: dict,
    id: str,
    name: str,
    parent: Optional[str] = None,
) -> dict:
    """Create a cluster, optionally nested under a parent."""
    if parent is not None and parent not in graph["clusters"]:
        raise KeyError(f"Parent cluster not found: {parent}")
    validated = make_cluster({"id": id, "name": name, "parent": parent})
    graph["clusters"][id] = validated
    return _refresh_metadata(graph)


def get_cluster_tree(graph: dict) -> dict:
    """Return hierarchical cluster structure.

    Returns a dict where each key is a root cluster ID and the value is::

        { "id": ..., "name": ..., "children": [ ... ] }
    """
    clusters = graph.get("clusters", {})
    tree_nodes: Dict[str, dict] = {}
    for cid, c in clusters.items():
        tree_nodes[cid] = {"id": cid, "name": c["name"], "children": []}

    roots: list[dict] = []
    for cid, c in clusters.items():
        parent = c.get("parent")
        if parent and parent in tree_nodes:
            tree_nodes[parent]["children"].append(tree_nodes[cid])
        else:
            roots.append(tree_nodes[cid])

    return {r["id"]: r for r in roots}


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def stats(graph: dict) -> dict:
    """Counts by type, cluster sizes, edge relationship counts."""
    type_counts: Dict[str, int] = {}
    for node in graph["nodes"].values():
        t = node.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    cluster_sizes: Dict[str, int] = {}
    for node in graph["nodes"].values():
        for cid in node.get("clusters", []):
            cluster_sizes[cid] = cluster_sizes.get(cid, 0) + 1

    edge_counts: Dict[str, int] = {}
    for e in graph["edges"]:
        r = e["relationship"]
        edge_counts[r] = edge_counts.get(r, 0) + 1

    return {
        "total_nodes": len(graph["nodes"]),
        "total_edges": len(graph["edges"]),
        "nodes_by_type": type_counts,
        "cluster_sizes": cluster_sizes,
        "edges_by_relationship": edge_counts,
    }
