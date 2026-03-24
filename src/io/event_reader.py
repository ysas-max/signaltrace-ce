from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import jsonschema


def _load_schema(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_events(path: str) -> List[Dict[str, Any]]:
    """Carrega e valida uma lista de eventos a partir de um arquivo JSON."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # caminho do schema relativo ao pacote
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / "event_schema_v1.json"
    schema = _load_schema(schema_path)
    for item in data:
        jsonschema.validate(item, schema)
    return data
