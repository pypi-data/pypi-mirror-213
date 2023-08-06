"""Wrappers on top of docstores."""
from langplus.docstore.in_memory import InMemoryDocstore
from langplus.docstore.wikipedia import Wikipedia

__all__ = ["InMemoryDocstore", "Wikipedia"]
