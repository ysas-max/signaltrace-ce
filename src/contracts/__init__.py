"""
Contracts package for SignalTrace CE.

This package provides helpers for loading and working with JSON
schemas used throughout the system.  The Community Edition uses
versioned schemas stored in the top‑level ``schemas`` directory.  The
helpers here centralise loading so that API and CLI code can depend
on a single function to fetch the appropriate schema without
duplicating file paths.
"""

from .schema import load_schema  # noqa: F401

__all__ = ["load_schema"]
