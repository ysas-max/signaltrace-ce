"""Testes para as funções de geração de relatórios.

Este conjunto de testes exercita diretamente as funções do módulo
``src.reporting.report`` para garantir que os objetos retornados
possuem a estrutura esperada e que os arquivos de saída são gerados
corretamente.  Não avalia a estética do Markdown, apenas a
integridade de dados.
"""

import json
from pathlib import Path

import pytest

from src.io.event_reader import load_events
from src.runner import run_pipeline
from src.reporting.report import (
    generate_analysis_result,
    generate_json_report,
    generate_markdown_report,
)


DATASET_PATH = "examples/synthetic/events_dataset_v1.json"


def test_generate_analysis_result_structure():
    events = load_events(DATASET_PATH)
    clusters = run_pipeline(DATASET_PATH)
    result = generate_analysis_result(clusters, len(events))
    assert isinstance(result, dict)
    assert "clusters" in result and "summary" in result
    summary = result["summary"]
    # total de eventos deve coincidir com o número de entradas
    assert summary["total_events"] == len(events)
    # cluster_ids devem ser únicos
    cluster_ids = [c["cluster_id"] for c in result["clusters"]]
    assert len(cluster_ids) == len(set(cluster_ids))
    # cada cluster deve conter campos obrigatórios
    for cl in result["clusters"]:
        for field in ["cluster_id", "members", "score", "level", "explanation"]:
            assert field in cl


def test_generate_json_report(tmp_path: Path):
    events = load_events(DATASET_PATH)
    clusters = run_pipeline(DATASET_PATH)
    output_file = tmp_path / "out.json"
    generate_json_report(clusters, len(events), str(output_file))
    assert output_file.exists()
    data = json.load(output_file.open("r", encoding="utf-8"))
    assert "clusters" in data and "summary" in data


def test_generate_markdown_report(tmp_path: Path):
    events = load_events(DATASET_PATH)
    clusters = run_pipeline(DATASET_PATH)
    output_file = tmp_path / "out.md"
    generate_markdown_report(clusters, len(events), str(output_file))
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    # deve conter título e pelo menos um cluster identificado
    assert "# Relatório" in content or "Relatório de Análise" in content
    assert "Cluster" in content