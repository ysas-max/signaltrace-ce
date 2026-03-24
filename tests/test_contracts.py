"""Testes de conformidade de contratos de saída.

Este teste valida que o objeto ``analysis_result`` produzido pela
função de geração de relatórios está em conformidade com o schema
JSON definido em ``schemas/analysis_result_schema_v1.json``.
"""

import json
from pathlib import Path

import jsonschema
import pytest

from src.io.event_reader import load_events
from src.runner import run_pipeline
from src.reporting.report import generate_analysis_result


DATASET_PATH = "examples/synthetic/events_dataset_v1.json"


def test_analysis_result_schema_validation():
    # carregar eventos sintéticos e executar pipeline
    events = load_events(DATASET_PATH)
    clusters = run_pipeline(DATASET_PATH)
    analysis_result = generate_analysis_result(clusters, len(events))
    # carregar schema
    schema_path = Path("schemas/analysis_result_schema_v1.json")
    schema = json.load(schema_path.open("r", encoding="utf-8"))
    # validar; deve levantar exceção em caso de não conformidade
    jsonschema.validate(analysis_result, schema)