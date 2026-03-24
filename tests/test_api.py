"""Testes para a API pública do SignalTrace CE.

Estes testes utilizam o cliente de testes do Flask para verificar
corretamente os endpoints implementados.  Todos os dados de entrada
são sintéticos e mínimos para manter o teste rápido.
"""

from __future__ import annotations

import json
from typing import Any, Dict

from flask.testing import FlaskClient

from src.api.server import create_app


def _sample_events() -> list[Dict[str, Any]]:
    """Retorna uma lista mínima de eventos sintéticos válidos."""
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


def test_health_and_schema() -> None:
    app = create_app()
    client: FlaskClient = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data is not None
    assert data["status"] == "ok"
    resp_schema = client.get("/schema/event")
    assert resp_schema.status_code == 200
    schema = resp_schema.get_json()
    assert schema is not None
    # Check that $id matches expected pattern
    assert schema.get("$id", "").endswith("/schema/event/v1")


def test_normalize_and_fingerprint() -> None:
    app = create_app()
    client: FlaskClient = app.test_client()
    events = _sample_events()
    resp_norm = client.post(
        "/normalize", data=json.dumps({"events": events}), content_type="application/json"
    )
    assert resp_norm.status_code == 200
    norm_data = resp_norm.get_json()
    assert isinstance(norm_data.get("normalized"), list)
    resp_fp = client.post(
        "/fingerprint", data=json.dumps({"events": norm_data["normalized"]}), content_type="application/json"
    )
    assert resp_fp.status_code == 200
    fps = resp_fp.get_json().get("fingerprints")
    assert isinstance(fps, list)
    assert len(fps) == len(events)


def test_correlate_and_score_and_analyze() -> None:
    app = create_app()
    client: FlaskClient = app.test_client()
    events = _sample_events()
    # Normalize and fingerprint via API
    resp_norm = client.post(
        "/normalize", data=json.dumps({"events": events}), content_type="application/json"
    )
    norm = resp_norm.get_json()["normalized"]
    resp_fp = client.post(
        "/fingerprint", data=json.dumps({"events": norm}), content_type="application/json"
    )
    fps = resp_fp.get_json()["fingerprints"]
    # Correlate
    resp_corr = client.post(
        "/correlate", data=json.dumps({"fingerprints": fps}), content_type="application/json"
    )
    assert resp_corr.status_code == 200
    clusters = resp_corr.get_json()["clusters"]
    # Score
    resp_score = client.post(
        "/score", data=json.dumps({"clusters": clusters}), content_type="application/json"
    )
    assert resp_score.status_code == 200
    scored = resp_score.get_json()["scored_clusters"]
    assert isinstance(scored, list)
    # Check fields exist
    assert all("score" in c and "level" in c and "explanation" in c for c in scored)
    # Analyze convenience endpoint
    resp_analysis = client.post(
        "/analyze", data=json.dumps({"events": events}), content_type="application/json"
    )
    assert resp_analysis.status_code == 200
    result = resp_analysis.get_json()
    assert "clusters" in result and "summary" in result
    assert result["summary"]["total_events"] == len(events)