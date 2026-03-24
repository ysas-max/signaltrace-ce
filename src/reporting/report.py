from __future__ import annotations

import json
from collections import Counter
from typing import Any, Dict, List


def _compute_summary(clusters: List[Dict[str, Any]], total_events: int) -> Dict[str, Any]:
    """Computa estatísticas agregadas para um conjunto de clusters."""
    total_clusters = len(clusters)
    # coletar marcadores e domínios
    marker_counter: Counter[str] = Counter()
    domain_counter: Counter[str] = Counter()
    for cluster in clusters:
        fps = cluster.get("fingerprints", [])
        for fp in fps:
            # cada fingerprint possui um conjunto de markers e um domínio opcional
            for m in getattr(fp, "markers", []):
                marker_counter[m] += 1
            dom = getattr(fp, "domain", None)
            if dom:
                domain_counter[dom] += 1
    top_markers = [m for m, _ in marker_counter.most_common(3)]
    top_domains = [d for d, _ in domain_counter.most_common(3)]
    average_score = sum(cluster.get("score", 0.0) for cluster in clusters) / total_clusters if total_clusters else 0.0
    warnings = [
        "Correlação e score são apenas indicadores, não constituem prova.",
    ]
    if total_clusters == 0:
        warnings.append("Nenhum cluster foi encontrado; todos os eventos podem ser únicos ou benignos.")
    return {
        "total_events": total_events,
        "total_clusters": total_clusters,
        "top_markers": top_markers,
        "top_domains": top_domains,
        "average_score": round(average_score, 3),
        "warnings": warnings,
    }


def generate_analysis_result(clusters: List[Dict[str, Any]], events_count: int) -> Dict[str, Any]:
    """Gera o objeto analysis_result com clusters e resumo."""
    # preparar clusters para saída: remover fingerprints (não precisam ser serializados)
    serialized_clusters: List[Dict[str, Any]] = []
    for idx, cluster in enumerate(clusters, start=1):
        serialized_clusters.append({
            "cluster_id": f"cluster-{idx}",
            "members": cluster.get("members", []),
            "score": round(cluster.get("score", 0.0), 3),
            "level": cluster.get("level", "desconhecido"),
            "explanation": cluster.get("explanation", ""),
        })
    summary = _compute_summary(clusters, events_count)
    return {
        "clusters": serialized_clusters,
        "summary": summary,
    }


def generate_json_report(clusters: List[Dict[str, Any]], events_count: int, output_path: str) -> None:
    """Gera e grava um relatório JSON em `output_path`."""
    result = generate_analysis_result(clusters, events_count)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def generate_markdown_report(clusters: List[Dict[str, Any]], events_count: int, output_path: str) -> None:
    """Gera e grava um relatório em Markdown legível."""
    result = generate_analysis_result(clusters, events_count)
    lines: List[str] = []
    summary = result["summary"]
    lines.append("# Relatório de Análise SignalTrace CE")
    lines.append("")
    lines.append(f"**Total de eventos:** {summary['total_events']}")
    lines.append(f"**Total de clusters:** {summary['total_clusters']}")
    lines.append(f"**Média de score:** {summary['average_score']:.2f}")
    if summary["top_markers"]:
        lines.append(f"**Marcadores mais frequentes:** {', '.join(summary['top_markers'])}")
    if summary["top_domains"]:
        lines.append(f"**Domínios mais frequentes:** {', '.join(summary['top_domains'])}")
    lines.append("")
    lines.append("## Clusters")
    for cluster in result["clusters"]:
        lines.append("")
        lines.append(f"### {cluster['cluster_id']}")
        lines.append(f"- **Membros:** {', '.join(cluster['members'])}")
        lines.append(f"- **Score:** {cluster['score']:.2f} ({cluster['level']})")
        lines.append(f"- **Explicação:** {cluster['explanation']}")
    lines.append("")
    lines.append("## Avisos")
    for warn in summary["warnings"]:
        lines.append(f"- {warn}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def print_summary(clusters: List[Dict[str, Any]], events_count: int) -> None:
    """Imprime no terminal um resumo agregado dos clusters e eventos."""
    summary = _compute_summary(clusters, events_count)
    print(f"Total de eventos: {summary['total_events']}")
    print(f"Total de clusters: {summary['total_clusters']}")
    print(f"Média de score: {summary['average_score']:.2f}")
    if summary["top_markers"]:
        print(f"Marcadores mais frequentes: {', '.join(summary['top_markers'])}")
    if summary["top_domains"]:
        print(f"Domínios mais frequentes: {', '.join(summary['top_domains'])}")
    for warn in summary["warnings"]:
        print(f"Aviso: {warn}")
