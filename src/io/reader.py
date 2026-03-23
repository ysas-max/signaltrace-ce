"""Leitor de dados em formatos suportados.

Este módulo oferece funções para carregar mensagens sintéticas de um
arquivo JSON. Os dados carregados são validados contra o schema
correspondente para garantir consistência.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import jsonschema

from ..contracts.schema import load_schema


def load_messages(path: str) -> List[Dict[str, Any]]:
    """Carrega mensagens sintéticas e valida contra o schema."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with file_path.open("r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    schema = load_schema("message_schema_v1.json")
    for item in data:
        jsonschema.validate(item, schema)
    return data
