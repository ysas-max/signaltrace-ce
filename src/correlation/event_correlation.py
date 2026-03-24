from __future__ import annotations

from datetime import timedelta
from typing import Any, Dict, List, Set

from ..fingerprint.event import EventFingerprint


class EventCorrelationEngine:
    def __init__(self, threshold: float = 0.5, weights: Dict[str, float] | None = None, time_window_hours: float = 48.0) -> None:
        self.threshold = threshold
        self.weights = weights or {"domain": 0.3, "tokens": 0.3, "markers": 0.2, "time": 0.2}
        total = sum(self.weights.values()) or 1.0
        for k in self.weights:
            self.weights[k] /= total
        self.time_window = timedelta(hours=time_window_hours)

    def _token_similarity(self, a: EventFingerprint, b: EventFingerprint) -> float:
        if not a.tokens and not b.tokens:
            return 0.0
        union = len(a.tokens | b.tokens)
        return len(a.tokens & b.tokens) / union if union else 0.0

    def _marker_similarity(self, a: EventFingerprint, b: EventFingerprint) -> float:
        if not a.markers or not b.markers:
            return 0.0
        return 1.0 if (a.markers & b.markers) else 0.0

    def _time_similarity(self, a: EventFingerprint, b: EventFingerprint) -> float:
        delta = abs(a.observed_time - b.observed_time)
        if delta >= self.time_window:
            return 0.0
        return 1.0 - (delta / self.time_window)

    def _domain_similarity(self, a: EventFingerprint, b: EventFingerprint) -> float:
        return 1.0 if a.domain and b.domain and a.domain == b.domain else 0.0

    def _similarity(self, a: EventFingerprint, b: EventFingerprint) -> float:
        return (
            self.weights["domain"] * self._domain_similarity(a, b)
            + self.weights["tokens"] * self._token_similarity(a, b)
            + self.weights["markers"] * self._marker_similarity(a, b)
            + self.weights["time"] * self._time_similarity(a, b)
        )

    def correlate(self, fingerprints: List[EventFingerprint]) -> List[Dict[str, Any]]:
        clusters: List[Dict[str, Any]] = []
        assigned: Set[str] = set()
        for fp in fingerprints:
            if fp.event_id in assigned:
                continue
            cluster_members = [fp]
            assigned.add(fp.event_id)
            for other in fingerprints:
                if other.event_id in assigned:
                    continue
                if self._similarity(fp, other) >= self.threshold:
                    cluster_members.append(other)
                    assigned.add(other.event_id)
            clusters.append({
                "center": fp.event_id,
                "members": [m.event_id for m in cluster_members],
                "fingerprints": cluster_members,
            })
        return clusters
