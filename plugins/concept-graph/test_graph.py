"""Tests for the concept-graph module.

Run with:  python -m pytest plugins/concept-graph/test_graph.py -v
"""

import json
import os
import sys
import tempfile

# The directory is named "concept-graph" (with a hyphen), so normal Python
# package imports don't work.  We add the directory to sys.path and import
# the modules directly.
sys.path.insert(0, os.path.dirname(__file__))

import pytest

import schema
from schema import (
    make_node,
    make_edge,
    make_cluster,
    now_iso,
    NodeType,
    Relationship,
)
import graph


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def empty_graph():
    return graph._empty_graph()


@pytest.fixture
def sample_graph(empty_graph):
    """Graph with a few nodes, edges, and clusters pre-populated."""
    g = empty_graph
    g = graph.add_cluster(g, "ml", "Machine Learning")
    g = graph.add_cluster(g, "dl", "Deep Learning", parent="ml")

    g = graph.add_node(g, {
        "id": "attention",
        "name": "Attention Mechanism",
        "type": "concept",
        "depth": "intermediate",
        "confidence": 3,
        "tags": ["nlp", "transformers"],
        "clusters": ["dl"],
        "questions": ["How does multi-head attention work?"],
    })
    g = graph.add_node(g, {
        "id": "flash_attention",
        "name": "Flash Attention",
        "type": "concept",
        "depth": "research",
        "confidence": 2,
        "tags": ["optimization", "transformers"],
        "clusters": ["dl"],
        "questions": ["What is the IO complexity of flash attention?"],
    })
    g = graph.add_node(g, {
        "id": "vaswani_2017",
        "name": "Attention Is All You Need",
        "type": "resource",
        "resource_type": "paper",
        "url": "https://arxiv.org/abs/1706.03762",
        "quality": 5,
        "tags": ["seminal"],
        "questions": ["What are the key innovations in the transformer architecture?"],
    })
    g = graph.add_node(g, {
        "id": "read_vaswani",
        "name": "Read Vaswani et al. 2017",
        "type": "task",
        "status": "todo",
        "priority": "high",
    })
    g = graph.add_node(g, {
        "id": "sparse_attention_idea",
        "name": "Sparse attention for long docs",
        "type": "idea",
        "status": "seed",
        "body": "Could we combine flash attention with sparse patterns?",
    })
    g = graph.add_node(g, {
        "id": "meeting_note",
        "name": "Meeting notes 2024-01-15",
        "type": "note",
        "body": "Discussed transformer scaling laws with the team.",
        "source_file": "notes/2024-01-15.md",
    })

    g = graph.add_edge(g, "flash_attention", "attention", "depends_on")
    g = graph.add_edge(g, "attention", "vaswani_2017", "learned_from", context="foundational paper")
    g = graph.add_edge(g, "read_vaswani", "vaswani_2017", "action_for")

    return g


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------

class TestSchema:
    def test_make_concept_node(self):
        node = make_node({
            "id": "test",
            "name": "Test Concept",
            "type": "concept",
            "depth": "intro",
            "confidence": 3,
        })
        assert node["type"] == "concept"
        assert node["depth"] == "intro"
        assert node["confidence"] == 3
        assert node["representations"]["summary"] is None

    def test_make_resource_node(self):
        node = make_node({
            "id": "res1",
            "name": "A Blog Post",
            "type": "resource",
            "resource_type": "blog",
            "quality": 4,
            "descriptiveness": "high",
        })
        assert node["quality"] == 4
        assert node["descriptiveness"] == "high"

    def test_make_task_node(self):
        node = make_node({
            "id": "t1",
            "name": "Do something",
            "type": "task",
            "status": "in_progress",
            "priority": "low",
        })
        assert node["status"] == "in_progress"

    def test_make_idea_node(self):
        node = make_node({
            "id": "i1",
            "name": "Idea",
            "type": "idea",
            "status": "developing",
            "body": "some text",
        })
        assert node["body"] == "some text"

    def test_make_note_node(self):
        node = make_node({
            "id": "n1",
            "name": "Note",
            "type": "note",
            "body": "raw text",
            "source_file": "a.md",
        })
        assert node["source_file"] == "a.md"

    def test_invalid_node_type(self):
        with pytest.raises(ValueError):
            make_node({"id": "x", "name": "X", "type": "invalid"})

    def test_confidence_out_of_range(self):
        with pytest.raises(ValueError):
            make_node({
                "id": "x",
                "name": "X",
                "type": "concept",
                "confidence": 6,
            })

    def test_quality_out_of_range(self):
        with pytest.raises(ValueError):
            make_node({
                "id": "x",
                "name": "X",
                "type": "resource",
                "quality": 0,
            })

    def test_invalid_relationship(self):
        with pytest.raises(ValueError):
            make_edge({
                "source": "a",
                "target": "b",
                "relationship": "nonsense",
            })

    def test_weight_out_of_range(self):
        with pytest.raises(ValueError):
            make_edge({
                "source": "a",
                "target": "b",
                "relationship": "related_to",
                "weight": 1.5,
            })

    def test_valid_edge(self):
        edge = make_edge({
            "source": "a",
            "target": "b",
            "relationship": "depends_on",
            "context": "test",
            "weight": 0.8,
        })
        assert edge["relationship"] == "depends_on"
        assert edge["weight"] == 0.8

    def test_valid_cluster(self):
        cluster = make_cluster({"id": "c1", "name": "Cluster 1"})
        assert cluster["parent"] is None


# ---------------------------------------------------------------------------
# Load / Save tests
# ---------------------------------------------------------------------------

class TestLoadSave:
    def test_load_nonexistent_returns_empty(self):
        g = graph.load("/tmp/_nonexistent_concept_graph_test_.json")
        assert g["nodes"] == {}
        assert g["edges"] == []
        assert g["clusters"] == {}

    def test_save_and_load_roundtrip(self, sample_graph):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            graph.save(sample_graph, path)
            loaded = graph.load(path)
            assert set(loaded["nodes"].keys()) == set(sample_graph["nodes"].keys())
            assert len(loaded["edges"]) == len(sample_graph["edges"])
            assert set(loaded["clusters"].keys()) == set(sample_graph["clusters"].keys())
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# Node operation tests
# ---------------------------------------------------------------------------

class TestNodeOps:
    def test_add_node(self, empty_graph):
        g = graph.add_node(empty_graph, {
            "id": "n1",
            "name": "Node 1",
            "type": "concept",
        })
        assert "n1" in g["nodes"]
        assert g["metadata"]["total_nodes"] == 1

    def test_add_node_sets_timestamps(self, empty_graph):
        g = graph.add_node(empty_graph, {
            "id": "n1",
            "name": "Node 1",
            "type": "concept",
        })
        node = g["nodes"]["n1"]
        assert "created" in node
        assert "updated" in node

    def test_update_node(self, sample_graph):
        g = graph.update_node(sample_graph, "attention", {"confidence": 5})
        assert g["nodes"]["attention"]["confidence"] == 5

    def test_update_node_not_found(self, empty_graph):
        with pytest.raises(KeyError):
            graph.update_node(empty_graph, "missing", {"name": "x"})

    def test_remove_node(self, sample_graph):
        g = graph.remove_node(sample_graph, "attention")
        assert "attention" not in g["nodes"]
        # Edges referencing attention should be gone
        for e in g["edges"]:
            assert e["source"] != "attention"
            assert e["target"] != "attention"

    def test_remove_node_not_found(self, empty_graph):
        with pytest.raises(KeyError):
            graph.remove_node(empty_graph, "missing")

    def test_get_node(self, sample_graph):
        node = graph.get_node(sample_graph, "attention")
        assert node is not None
        assert node["name"] == "Attention Mechanism"

    def test_get_node_missing(self, sample_graph):
        assert graph.get_node(sample_graph, "nope") is None


# ---------------------------------------------------------------------------
# Edge operation tests
# ---------------------------------------------------------------------------

class TestEdgeOps:
    def test_add_edge(self, sample_graph):
        initial_count = len(sample_graph["edges"])
        g = graph.add_edge(
            sample_graph, "flash_attention", "vaswani_2017", "learned_from"
        )
        assert len(g["edges"]) == initial_count + 1

    def test_add_edge_invalid_source(self, sample_graph):
        with pytest.raises(KeyError):
            graph.add_edge(sample_graph, "missing", "attention", "related_to")

    def test_add_edge_invalid_target(self, sample_graph):
        with pytest.raises(KeyError):
            graph.add_edge(sample_graph, "attention", "missing", "related_to")

    def test_remove_edge(self, sample_graph):
        initial_count = len(sample_graph["edges"])
        g = graph.remove_edge(sample_graph, "flash_attention", "attention", "depends_on")
        assert len(g["edges"]) == initial_count - 1

    def test_remove_edge_all_between_pair(self, sample_graph):
        # Add a second edge between same pair
        g = graph.add_edge(
            sample_graph, "flash_attention", "attention", "related_to"
        )
        count_before = len(g["edges"])
        g = graph.remove_edge(g, "flash_attention", "attention")
        # Both edges between that pair should be removed
        remaining = [
            e for e in g["edges"]
            if e["source"] == "flash_attention" and e["target"] == "attention"
        ]
        assert len(remaining) == 0


# ---------------------------------------------------------------------------
# Query tests
# ---------------------------------------------------------------------------

class TestQueries:
    def test_find_nodes_by_type(self, sample_graph):
        concepts = graph.find_nodes(sample_graph, type="concept")
        assert len(concepts) == 2
        assert all(n["type"] == "concept" for n in concepts)

    def test_find_nodes_by_tags(self, sample_graph):
        results = graph.find_nodes(sample_graph, tags=["transformers"])
        ids = {n["id"] for n in results}
        assert "attention" in ids
        assert "flash_attention" in ids

    def test_find_nodes_by_cluster(self, sample_graph):
        results = graph.find_nodes(sample_graph, cluster="dl")
        ids = {n["id"] for n in results}
        assert "attention" in ids

    def test_find_nodes_by_text(self, sample_graph):
        results = graph.find_nodes(sample_graph, text="flash")
        ids = {n["id"] for n in results}
        assert "flash_attention" in ids
        # The idea node body also contains "flash attention"
        assert "sparse_attention_idea" in ids
        assert len(results) == 2

    def test_find_nodes_text_searches_body(self, sample_graph):
        results = graph.find_nodes(sample_graph, text="scaling laws")
        assert len(results) == 1
        assert results[0]["id"] == "meeting_note"

    def test_find_nodes_text_searches_tags(self, sample_graph):
        results = graph.find_nodes(sample_graph, text="seminal")
        assert len(results) == 1
        assert results[0]["id"] == "vaswani_2017"

    def test_find_nodes_combined_filters(self, sample_graph):
        results = graph.find_nodes(
            sample_graph, type="concept", tags=["transformers"], text="flash"
        )
        assert len(results) == 1
        assert results[0]["id"] == "flash_attention"

    def test_get_neighbors(self, sample_graph):
        neighbors = graph.get_neighbors(sample_graph, "attention")
        ids = {n["id"] for n in neighbors}
        assert "flash_attention" in ids  # flash_attention -> attention
        assert "vaswani_2017" in ids  # attention -> vaswani_2017

    def test_get_neighbors_filtered(self, sample_graph):
        neighbors = graph.get_neighbors(
            sample_graph, "attention", relationship="depends_on"
        )
        ids = {n["id"] for n in neighbors}
        assert "flash_attention" in ids
        assert "vaswani_2017" not in ids

    def test_find_questions(self, sample_graph):
        results = graph.find_questions(sample_graph, "attention")
        assert len(results) >= 2  # at least from attention and flash_attention
        questions_text = [r["question"] for r in results]
        assert any("multi-head" in q for q in questions_text)
        assert any("IO complexity" in q for q in questions_text)

    def test_find_questions_no_match(self, sample_graph):
        results = graph.find_questions(sample_graph, "xyznonexistent")
        assert results == []


# ---------------------------------------------------------------------------
# Cluster tests
# ---------------------------------------------------------------------------

class TestClusters:
    def test_add_cluster(self, empty_graph):
        g = graph.add_cluster(empty_graph, "root", "Root Cluster")
        assert "root" in g["clusters"]

    def test_add_nested_cluster(self, empty_graph):
        g = graph.add_cluster(empty_graph, "parent", "Parent")
        g = graph.add_cluster(g, "child", "Child", parent="parent")
        assert g["clusters"]["child"]["parent"] == "parent"

    def test_add_cluster_invalid_parent(self, empty_graph):
        with pytest.raises(KeyError):
            graph.add_cluster(empty_graph, "child", "Child", parent="missing")

    def test_get_cluster_tree(self, sample_graph):
        tree = graph.get_cluster_tree(sample_graph)
        assert "ml" in tree
        assert len(tree["ml"]["children"]) == 1
        assert tree["ml"]["children"][0]["id"] == "dl"
        # dl should not be a root
        assert "dl" not in tree


# ---------------------------------------------------------------------------
# Stats tests
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats(self, sample_graph):
        s = graph.stats(sample_graph)
        assert s["total_nodes"] == 6
        assert s["total_edges"] == 3
        assert s["nodes_by_type"]["concept"] == 2
        assert s["nodes_by_type"]["resource"] == 1
        assert s["nodes_by_type"]["task"] == 1
        assert s["nodes_by_type"]["idea"] == 1
        assert s["nodes_by_type"]["note"] == 1
        assert s["edges_by_relationship"]["depends_on"] == 1
        assert s["cluster_sizes"]["dl"] == 2


# ---------------------------------------------------------------------------
# Tests for bug-fix issues 1-4
# ---------------------------------------------------------------------------

class TestNowIsoExported:
    """Issue 1: now_iso() should be importable from schema."""

    def test_now_iso_returns_string(self):
        ts = now_iso()
        assert isinstance(ts, str)

    def test_now_iso_is_utc_iso8601(self):
        ts = now_iso()
        # Must contain timezone offset or 'Z'; basic structural check.
        assert "+" in ts or ts.endswith("+00:00") or "+00:00" in ts

    def test_graph_does_not_define_own_now_iso(self):
        """graph module should not have its own _now_iso definition."""
        import inspect
        import graph as g_mod
        src = inspect.getsource(g_mod)
        # After the fix, graph.py must not contain a standalone def _now_iso
        assert "def _now_iso" not in src


class TestUpdateNodeInvalidFields:
    """Issue 2: update_node should reject unknown field names."""

    def test_rejects_unknown_field(self, sample_graph):
        with pytest.raises(ValueError, match="Invalid field"):
            graph.update_node(sample_graph, "attention", {"nonexistent_field": "val"})

    def test_rejects_multiple_unknown_fields(self, sample_graph):
        with pytest.raises(ValueError, match="Invalid field"):
            graph.update_node(sample_graph, "attention", {"foo": 1, "bar": 2})

    def test_rejects_field_wrong_for_type(self, sample_graph):
        # 'quality' is a ResourceNode field, not valid on a concept node
        with pytest.raises(ValueError, match="Invalid field"):
            graph.update_node(sample_graph, "attention", {"quality": 4})

    def test_accepts_valid_field(self, sample_graph):
        g = graph.update_node(sample_graph, "attention", {"confidence": 4})
        assert g["nodes"]["attention"]["confidence"] == 4


class TestUpdateNodeTypeChange:
    """Issue 3: update_node should prevent changing the node type."""

    def test_rejects_type_change(self, sample_graph):
        with pytest.raises(ValueError, match="Cannot change node type"):
            graph.update_node(sample_graph, "attention", {"type": "resource"})

    def test_allows_same_type(self, sample_graph):
        # Setting type to the same value should be fine (no-op on type)
        g = graph.update_node(sample_graph, "attention", {"type": "concept", "confidence": 2})
        assert g["nodes"]["attention"]["type"] == "concept"


class TestDuplicateEdgePrevention:
    """Issue 4: add_edge should raise ValueError on duplicate edges."""

    def test_duplicate_edge_raises(self, sample_graph):
        # flash_attention --[depends_on]--> attention already exists in sample_graph
        with pytest.raises(ValueError, match="Duplicate edge"):
            graph.add_edge(sample_graph, "flash_attention", "attention", "depends_on")

    def test_same_pair_different_relationship_allowed(self, sample_graph):
        # Same source/target but different relationship should succeed
        initial_count = len(sample_graph["edges"])
        g = graph.add_edge(sample_graph, "flash_attention", "attention", "related_to")
        assert len(g["edges"]) == initial_count + 1

    def test_reversed_direction_allowed(self, sample_graph):
        # Reversing source/target is a different edge
        initial_count = len(sample_graph["edges"])
        g = graph.add_edge(sample_graph, "attention", "flash_attention", "depends_on")
        assert len(g["edges"]) == initial_count + 1
