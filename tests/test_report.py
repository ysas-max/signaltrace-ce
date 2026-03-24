"""Testes para geração de relatórios no SignalTrace CE."""

from __future__ import annotations

from typing import Any, Dict, List

from src.report.generator import generate_analysis_result, generate_markdown_report


def _sample_events() -> list[Dict[str, Any]]:
    return [
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


def test_generate_analysis_result() -> None:
    events = _sample_events()
    result = generate_analysis_result(events)
    assert result["schema_version"] == "analysis_result_v1"
    assert "clusters" in result and "summary" in result
    assert result["summary"]["total_events"] == len(events)


def test_generate_markdown_report() -> None:
    events = _sample_events()
    result = generate_analysis_result(events)
    md = generate_markdown_report(result)
    # Basic checks on the Markdown content
    assert "Relatório de Análise" in md
    assert "Total de eventos" in md
    assert "Cluster" in md
    assert "Nota" in md