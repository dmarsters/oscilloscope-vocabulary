"""Oscilloscope Vocabulary MCP Server - Visual vocabulary for harmonic-guided image generation."""

__version__ = "0.1.0"
__author__ = "Dal"

__all__ = ["create_server"]

# Lazy import to avoid issues in cloud environment
def __getattr__(name):
    if name == "create_server":
        from .server import create_server
        return create_server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
