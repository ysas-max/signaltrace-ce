"""Motor de correlação simples.

Este módulo oferece uma implementação básica de correlação de
fingerprints com base em similaridade de features. Para fins de
demonstração, utiliza distâncias euclidianas e agrupa entidades em
clusters.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List

from ..fingerprint.extractor import Fingerprint


class CorrelationEngine:
    """Agrupa fingerprints em clusters baseados em similaridade.

    Esta implementação usa um limiar simples para determinar se duas
    entidades pertencem ao mesmo cluster. O algoritmo não é otimizado
    para escala; seu objetivo principal é servir como exemplo auditável.
    """

    def __init__(self, threshold: float = 0.5) -> None:
        self.threshold = threshold

    def _distance(self, first: Fingerprint, second: Fingerprint) -> float:
        """Calcula a distância euclidiana entre duas fingerprints."""
        keys = set(first.features.keys()) | set(second.features.keys())
        diff_squared = 0.0
        for key in keys:
            diff = first.features.get(key, 0.0) - second.features.get(
                key,
                0.0,
            )
            diff_squared += diff * diff
        return math.sqrt(diff_squared)

    def correlate(
        self,
        fingerprints: List[Fingerprint],
    ) -> List[Dict[str, Any]]:
        """Agrupa fingerprints em clusters simples."""
        clusters: List[Dict[str, Any]] = []
        assigned = set()
        for fingerprint in fingerprints:
            if fingerprint.entity in assigned:
                continue
            cluster_members = [fingerprint.entity]
            assigned.add(fingerprint.entity)
            for other in fingerprints:
                if other.entity in assigned:
                    continue
                if self._distance(fingerprint, other) <= self.threshold:
                    cluster_members.append(other.entity)
                    assigned.add(other.entity)
            clusters.append(
                {
                    "center": fingerprint.entity,
                    "members": cluster_members,
                }
            )
        return clusters
