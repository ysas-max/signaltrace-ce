"""Report generation functions for SignalTrace CE.

This module defines functions to run the SignalTrace CE analysis
pipeline on a batch of events and to produce structured outputs.
The outputs are designed to be both machine consumable (JSON) and
human consumable (Markdown) and include summary statistics and
explicit warnings about the limitations of the analysis.
"""

from __future__ import annotations

import datetime
import json
from typing import Any, Dict, List, Tuple

from ..normalization.normalizer import Normalizer
from ..fingerprint.event import EventFingerprint, EventFingerprintExtractor
from ..correlation.event_correlation import EventCorrelationEngine
from ..scoring.risk import RiskScorer


def _fingerprint_to_dict(fp: EventFingerprint) -> Dict[str, Any]:
    return {
        "event_id": fp.event_id,
        "features": fp.features,
        "tokens": sorted(list(fp.tokens)),
        "domain": fp.domain,
        "markers": sorted(list(fp.markers)),
        "observed_time": fp.observed_time.isoformat(),
        "risk_flags": sorted(list(fp.risk_flags)),
    }


def _cluster_to_dict(cluster: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "cluster_id": cluster.get("center"),
        "members": cluster.get("members", []),
        "fingerprints": [
            _fingerprint_to_dict(fp) for fp in cluster.get("fingerprints", [])
        ],
    }


def _compute_summary(scored_clusters: List[Dict[str, Any]], total_events: int) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "total_events": total_events,
        "total_clusters": len(scored_clusters),
        "risk_levels": {},
        "top_markers": [],
        "top_risk_flags": [],
        "warning": "A correlação não constitui prova categórica."
    }
    levels: Dict[str, int] = {}
    marker_counts: Dict[str, int] = {}
    flag_counts: Dict[str, int] = {}
    for cluster in scored_clusters:
        level = cluster.get("level", "desconhecido")
        levels[level] = levels.get(level, 0) + 1
        for fp in cluster.get("fingerprints", []):
            if isinstance(fp, EventFingerprint):
                markers = fp.markers
                flags = fp.risk_flags
            else:
                markers = set(fp.get("markers", []))
                flags = set(fp.get("risk_flags", []))
            for m in markers:
                marker_counts[m] = marker_counts.get(m, 0) + 1
            for f in flags:
                flag_counts[f] = flag_counts.get(f, 0) + 1
    summary["risk_levels"] = levels
    top_markers = sorted(marker_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    summary["top_markers"] = [m for m, _ in top_markers]
    top_flags = sorted(flag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    summary["top_risk_flags"] = [f for f, _ in top_flags]
    return summary


def generate_analysis_result(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run the full analysis pipeline and return a structured result.

    Args:
        events: A list of event dictionaries conforming to the event
            schema.  Data must be synthetic and non‑identifying.

    Returns:
        A dictionary with keys ``clusters``, ``summary`` and
        ``schema_version``.  ``clusters`` contains scored clusters with
        explanations.  ``summary`` contains aggregated statistics.
    """
    normalizer = Normalizer()
    extractor = EventFingerprintExtractor(suspicious_keywords=normalizer.suspicious_keywords)
    correlator = EventCorrelationEngine()
    scorer = RiskScorer()
    normalized = [normalizer.normalize(evt) for evt in events]
    fps = extractor.extract_batch(normalized)
    clusters = correlator.correlate(fps)
    scored = scorer.score(clusters)
    clusters_serialised: List[Dict[str, Any]] = []
    for sc in scored:
        cs = _cluster_to_dict(sc)
        cs["score"] = sc.get("score")
        cs["level"] = sc.get("level")
        cs["explanation"] = sc.get("explanation")
        clusters_serialised.append(cs)
    summary = _compute_summary(scored, total_events=len(events))
    return {
        "clusters": clusters_serialised,
        "summary": summary,
        "schema_version": "analysis_result_v1",
    }


def generate_markdown_report(result: Dict[str, Any]) -> str:
    """Generate a Markdown report from an analysis result.

    The report contains a high level summary followed by per‑cluster
    details.  It emphasises that correlations and scores are merely
    indicators and not proof.  Long explanations or large tables are
    avoided to ensure readability.

    Args:
        result: The analysis result as returned by
            :func:`generate_analysis_result`.

    Returns:
        A string containing Markdown formatted text.
    """
    summary = result.get("summary", {})
    clusters = result.get("clusters", [])
    lines: List[str] = []
    lines.append("# Relatório de Análise SignalTrace CE\n")
    lines.append("## Resumo\n")
    lines.append(f"- Total de eventos analisados: {summary.get('total_events', 0)}")
    lines.append(f"- Total de clusters encontrados: {summary.get('total_clusters', 0)}")
    # Format risk level distribution
    risk_levels = summary.get("risk_levels", {})
    if risk_levels:
        lines.append("- Distribuição de níveis de risco:")
        for level, count in risk_levels.items():
            lines.append(f"  - {level}: {count}")
    top_markers = summary.get("top_markers", [])
    if top_markers:
        lines.append("- Marcadores mais frequentes: " + ", ".join(top_markers))
    top_flags = summary.get("top_risk_flags", [])
    if top_flags:
        lines.append("- Sinais de risco mais frequentes: " + ", ".join(top_flags))
    lines.append(f"- Aviso: {summary.get('warning')}\n")

    for idx, cluster in enumerate(clusters, start=1):
        lines.append(f"\n## Cluster {idx}")
        lines.append(f"- ID do cluster: {cluster.get('cluster_id')}")
        members = cluster.get("members", [])
        lines.append(f"- Eventos: {', '.join(members) if members else 'nenhum'}")
        score = cluster.get("score", 0.0)
        level = cluster.get("level", '')
        lines.append(f"- Score: {score:.2f} ({level})")
        explanation = cluster.get("explanation", "")
        if explanation:
            lines.append(f"- Justificativa: {explanation}")
    # Append a final note emphasising the non‑proof nature of the analysis
    lines.append(
        "\n**Nota:** Os resultados apresentados são indicativos. "
        "A correlação de eventos e o cálculo de scores não constituem prova categórica de "
        "atividade maliciosa. Use estes dados apenas como guia em investigações "
        "defensivas."
    )
    return "\n".join(lines)
