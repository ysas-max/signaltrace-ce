"""Testes para a CLI pública do SignalTrace CE.

As chamadas invocam diretamente o ``main`` da CLI com argumentos
específicos.  Eventos sintéticos são escritos em arquivos temporários
para garantir isolamento dos testes.  O capsys é utilizado para
capturar a saída do stdout.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.cli.main import main as cli_main


def _write_events_tmp(events: List[Dict[str, Any]]) -> str:
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(events, f)
    return path


@pytest.fixture
def sample_events_path() -> str:
    events = [
        {
            "event_id": "e1",
            "source_type": "sms",
            "observed_at": "2025-01-01T00:00:00Z",
            "message_text": "Promoção incrível! Clique agora para bônus",
            "sender_handle": "user1",
            "sender_hash": "A" * 64,
            "domain_hint": "promo.bonus.com",
            "campaign_markers": ["promo1"],
        },
        {
            "event_id": "e2",
            "source_type": "sms",
            "observed_at": "2025-01-01T01:00:00Z",
            "message_text": "Oferta grátis disponível, clique e ganhe bônus",
            "sender_handle": "user2",
            "sender_hash": "B" * 64,
            "domain_hint": "bonus.example.com",
            "campaign_markers": ["promo1"],
        },
    ]
    path = _write_events_tmp(events)
    yield path
    os.unlink(path)


def test_cli_validate(sample_events_path: str, capsys: pytest.CaptureFixture[str]) -> None:
    cli_main(["validate", "--input", sample_events_path])
    captured = capsys.readouterr()
    assert "Dataset válido" in captured.out


def test_cli_run(sample_events_path: str, capsys: pytest.CaptureFixture[str]) -> None:
    cli_main(["run", "--input", sample_events_path])
    captured = capsys.readouterr()
    # Expect summary lines
    assert "Total de eventos" in captured.out
    assert "Total de clusters" in captured.out


def test_cli_reports(sample_events_path: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    json_output = tmp_path / "report.json"
    md_output = tmp_path / "report.md"
    cli_main(["report-json", "--input", sample_events_path, "--output", str(json_output)])
    cli_main(["report-md", "--input", sample_events_path, "--output", str(md_output)])
    # Verify files exist and contain expected keys
    with json_output.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert "clusters" in data and "summary" in data
    with md_output.open("r", encoding="utf-8") as f:
        md = f.read()
    assert "Relatório de Análise" in md
    assert "Cluster" in md


def test_cli_summary(sample_events_path: str, capsys: pytest.CaptureFixture[str]) -> None:
    cli_main(["summary", "--input", sample_events_path])
    captured = capsys.readouterr()
    assert "Total de eventos" in captured.out
    assert "Aviso" in captured.out