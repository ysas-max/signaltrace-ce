"""Módulo de cálculo de pontuação.

Calcula scores de risco ou similaridade para clusters resultantes da
correlação de fingerprints. A lógica aqui é simplista e serve como
exemplo, priorizando transparência sobre complexidade.
"""

from __future__ import annotations

from typing import Any, Dict, List


class ScoreEngine:
    """Aplica um score básico a clusters de fingerprints."""

    def score(self, clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Atribui scores a cada cluster."""
        scored_clusters: List[Dict[str, Any]] = []
        for cluster in clusters:
            member_count = len(cluster.get("members", []))
            score_value = 1.0 / member_count if member_count else 0.0
            explanation = (
                f"Cluster com {member_count} membro(s). "
                "Score calculado como 1/size, indicando "
                "maior confiança em clusters menores."
            )
            scored_clusters.append(
                {
                    **cluster,
                    "score": score_value,
                    "explanation": explanation,
                }
            )
        return scored_clusters
