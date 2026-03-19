"""Schema definitions for the concept graph.

Dataclasses define the shape and validation rules for nodes, edges, and clusters.
They are used for construction and validation, then converted to plain dicts
via dataclasses.asdict() for storage in the graph.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class NodeType(str, Enum):
    CONCEPT = "concept"
    RESOURCE = "resource"
    TASK = "task"
    IDEA = "idea"
    NOTE = "note"


class Depth(str, Enum):
    INTRO = "intro"
    INTERMEDIATE = "intermediate"
    RESEARCH = "research"


class ResourceType(str, Enum):
    PAPER = "paper"
    VIDEO = "video"
    BLOG = "blog"
    BOOK = "book"
    COURSE = "course"
    TOOL = "tool"


class Descriptiveness(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IdeaStatus(str, Enum):
    SEED = "seed"
    DEVELOPING = "developing"
    VALIDATED = "validated"
    ARCHIVED = "archived"


class Relationship(str, Enum):
    # Structural
    PART_OF = "part_of"
    CONTAINS = "contains"
    # Knowledge
    DEPENDS_ON = "depends_on"
    ENABLES = "enables"
    EXTENDS = "extends"
    SPECIALIZES = "specializes"
    # Associative
    RELATED_TO = "related_to"
    CONTRASTS_WITH = "contrasts_with"
    SIMILAR_TO = "similar_to"
    # Provenance
    DERIVED_FROM = "derived_from"
    LEARNED_FROM = "learned_from"
    SUPPORTS = "supports"
    # Action
    ACTION_FOR = "action_for"
    PRODUCES = "produces"
    BLOCKED_BY = "blocked_by"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Base node
# ---------------------------------------------------------------------------

@dataclass
class BaseNode:
    id: str
    name: str
    type: str  # validated against NodeType
    tags: List[str] = field(default_factory=list)
    clusters: List[str] = field(default_factory=list)
    created: str = field(default_factory=_now_iso)
    updated: str = field(default_factory=_now_iso)

    def __post_init__(self):
        # Validate type is a known NodeType
        NodeType(self.type)


# ---------------------------------------------------------------------------
# Specialised nodes
# ---------------------------------------------------------------------------

@dataclass
class ConceptNode(BaseNode):
    depth: str = "intro"  # validated against Depth
    subtopics: List[str] = field(default_factory=list)
    confidence: int = 1
    representations: Dict[str, Optional[str]] = field(
        default_factory=lambda: {
            "summary": None,
            "diagram": None,
            "audio": None,
            "flashcards": None,
        }
    )
    questions: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.type = NodeType.CONCEPT.value
        super().__post_init__()
        Depth(self.depth)
        if not (1 <= self.confidence <= 5):
            raise ValueError(f"confidence must be 1-5, got {self.confidence}")


@dataclass
class ResourceNode(BaseNode):
    url: Optional[str] = None
    resource_type: str = "blog"  # validated against ResourceType
    quality: int = 3
    quality_reason: Optional[str] = None
    descriptiveness: str = "medium"  # validated against Descriptiveness
    descriptiveness_reason: Optional[str] = None
    source_file: Optional[str] = None
    questions: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.type = NodeType.RESOURCE.value
        super().__post_init__()
        ResourceType(self.resource_type)
        Descriptiveness(self.descriptiveness)
        if not (1 <= self.quality <= 5):
            raise ValueError(f"quality must be 1-5, got {self.quality}")


@dataclass
class TaskNode(BaseNode):
    status: str = "todo"  # validated against TaskStatus
    priority: str = "medium"  # validated against Priority
    due_date: Optional[str] = None

    def __post_init__(self):
        self.type = NodeType.TASK.value
        super().__post_init__()
        TaskStatus(self.status)
        Priority(self.priority)


@dataclass
class IdeaNode(BaseNode):
    status: str = "seed"  # validated against IdeaStatus
    body: str = ""

    def __post_init__(self):
        self.type = NodeType.IDEA.value
        super().__post_init__()
        IdeaStatus(self.status)


@dataclass
class NoteNode(BaseNode):
    body: str = ""
    source_file: Optional[str] = None

    def __post_init__(self):
        self.type = NodeType.NOTE.value
        super().__post_init__()


# ---------------------------------------------------------------------------
# Edge
# ---------------------------------------------------------------------------

@dataclass
class Edge:
    source: str
    target: str
    relationship: str  # validated against Relationship
    context: Optional[str] = None
    weight: float = 0.5
    created: str = field(default_factory=_now_iso)

    def __post_init__(self):
        Relationship(self.relationship)
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"weight must be 0-1, got {self.weight}")


# ---------------------------------------------------------------------------
# Cluster
# ---------------------------------------------------------------------------

@dataclass
class Cluster:
    id: str
    name: str
    parent: Optional[str] = None
    created: str = field(default_factory=_now_iso)


# ---------------------------------------------------------------------------
# Factory / conversion helpers
# ---------------------------------------------------------------------------

_NODE_CLASS = {
    "concept": ConceptNode,
    "resource": ResourceNode,
    "task": TaskNode,
    "idea": IdeaNode,
    "note": NoteNode,
}


def make_node(data: dict) -> dict:
    """Validate *data* by constructing the appropriate dataclass, then return
    a plain dict ready for storage in the graph.

    *data* must contain at least ``id``, ``name``, and ``type``.
    """
    node_type = data.get("type")
    if node_type not in _NODE_CLASS:
        raise ValueError(f"Unknown node type: {node_type}")
    cls = _NODE_CLASS[node_type]
    # Filter data to only keys the dataclass accepts
    valid_fields = {f.name for f in dataclasses.fields(cls)}
    filtered = {k: v for k, v in data.items() if k in valid_fields}
    instance = cls(**filtered)
    return asdict(instance)


def make_edge(data: dict) -> dict:
    """Validate and return a plain dict for an edge."""
    instance = Edge(**data)
    return asdict(instance)


def make_cluster(data: dict) -> dict:
    """Validate and return a plain dict for a cluster."""
    instance = Cluster(**data)
    return asdict(instance)
