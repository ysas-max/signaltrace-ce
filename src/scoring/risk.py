from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Tuple

from ..fingerprint.event import EventFingerprint


class RiskScorer:
    """Calcula scores de risco e gera explicações para clusters de eventos."""

    DEFAULT_WEIGHTS = {
        "domain": 0.3,
        "tokens": 0.25,
        "markers": 0.2,
        "time": 0.15,
        "risk_flags": 0.1,
    }

    def __init__(self, weights: Dict[str, float] | None = None) -> None:
        self.weights = dict(self.DEFAULT_WEIGHTS)
        if weights:
            self.weights.update(weights)
        total = sum(self.weights.values()) or 1.0
        for k in self.weights:
            self.weights[k] /= total

    def _metric_domain_repetition(self, fps: List[EventFingerprint]) -> float:
        domains = [fp.domain for fp in fps if fp.domain]
        if not domains:
            return 0.0
        return Counter(domains).most_common(1)[0][1] / len(fps)

    def _metric_token_similarity(self, fps: List[EventFingerprint]) -> float:
        if len(fps) < 2:
            return 0.0
        total = 0.0
        count = 0
        for i in range(len(fps)):
            for j in range(i + 1, len(fps)):
                union = len(fps[i].tokens | fps[j].tokens)
                sim = len(fps[i].tokens & fps[j].tokens) / union if union else 0.0
                total += sim
                count += 1
        return total / count if count else 0.0

    def _metric_marker_presence(self, fps: List[EventFingerprint]) -> float:
        return (sum(1 for fp in fps if fp.markers) / len(fps)) if fps else 0.0

    def _metric_time_proximity(self, fps: List[EventFingerprint]) -> float:
        if not fps:
            return 0.0
        times = [fp.observed_time for fp in fps]
        delta_seconds = (max(times) - min(times)).total_seconds()
        window = 7 * 24 * 3600.0
        if delta_seconds >= window:
            return 0.0
        return 1.0 - (delta_seconds / window)

    def _metric_risk_flags(self, fps: List[EventFingerprint]) -> float:
        return (sum(1 for fp in fps if fp.risk_flags) / len(fps)) if fps else 0.0

    def _calculate_score(self, cluster: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        fps: List[EventFingerprint] = cluster.get("fingerprints", [])
        metrics = {
            "domain": self._metric_domain_repetition(fps),
            "tokens": self._metric_token_similarity(fps),
            "markers": self._metric_marker_presence(fps),
            "time": self._metric_time_proximity(fps),
            "risk_flags": self._metric_risk_flags(fps),
        }
        score = sum(self.weights[k] * v for k, v in metrics.items())
        return score, metrics

    def _risk_level(self, score: float) -> str:
        if score < 0.25:
            return "baixo"
        if score < 0.5:
            return "moderado"
        if score < 0.75:
            return "alto"
        return "crítico"

    def _explain(self, metrics: Dict[str, float]) -> str:
        contribs = sorted(((k, v, self.weights[k] * v) for k, v in metrics.items()), key=lambda x: x[2], reverse=True)
        return "; ".join(f"{k}: {v:.2f} (peso {self.weights[k]:.2f})" for k, v, _ in contribs)

    def score(self, clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        scored = []
        for cluster in clusters:
            score, metrics = self._calculate_score(cluster)
            scored.append({
                **cluster,
                "score": score,
                "level": self._risk_level(score),
                "explanation": self._explain(metrics),
            })
        return scored
