"""
Schema loading utilities for SignalTrace CE.

This module defines functions to load JSON schema definitions used for
input validation and contract documentation.  Schemas are stored in
the top‑level ``schemas`` directory and are versioned by filename.  For
example, the event schema is stored in ``schemas/event_schema_v1.json``.

The ``load_schema`` function reads and returns the JSON object from
a given schema file name.  It performs no validation of the schema
itself.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def load_schema(name: str) -> Dict[str, Any]:
    """Load a JSON schema by file name from the ``schemas`` directory.

    Args:
        name: The file name of the schema, e.g. ``"event_schema_v1.json"``.

    Returns:
        A dictionary representing the parsed JSON schema.

    Raises:
        FileNotFoundError: If the specified schema file does not exist.
        json.JSONDecodeError: If the schema file contains invalid JSON.
    """
    # Compute path to the repository root (two levels up from this file)
    base_dir = Path(__file__).resolve().parents[2]
    schema_path = base_dir / "schemas" / name
    if not schema_path.is_file():
        raise FileNotFoundError(f"Schema não encontrado: {schema_path}")
    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)
