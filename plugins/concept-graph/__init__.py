"""Concept-graph plugin for the Personal Learning OS.

Provides schema definitions and pure-function graph operations for
managing a knowledge graph stored as a single JSON file.
"""

try:
    from . import schema
    from . import graph
except ImportError:
    import schema  # type: ignore[no-redef]
    import graph  # type: ignore[no-redef]

__all__ = ["schema", "graph"]
