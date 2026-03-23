"""Carregador de schemas JSON.

Este módulo contém funções para localizar e carregar schemas JSON
definidos no diretório `schemas/`. Os schemas são utilizados para
validar mensagens e clusters sintéticos.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


SCHEMAS_DIR = Path(__file__).resolve().parents[2] / "schemas"


def load_schema(name: str) -> Dict[str, Any]:
    """Carrega um schema JSON a partir do diretório de schemas.

    Args:
        name: Nome do arquivo de schema.

    Returns:
        Dicionário representando o schema JSON.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        json.JSONDecodeError: Se o arquivo não contiver JSON válido.
    """
    schema_path = SCHEMAS_DIR / name
    if not schema_path.is_file():
        raise FileNotFoundError(f"Schema não encontrado: {name}")
    with schema_path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)
