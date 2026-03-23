"""Testes para o módulo de correlação."""

from src.correlation.engine import CorrelationEngine
from src.fingerprint.extractor import Fingerprint


def test_correlation_engine_clusters_by_threshold() -> None:
    first = Fingerprint(entity="user_a", features={"x": 0.0})
    second = Fingerprint(entity="user_b", features={"x": 0.1})
    third = Fingerprint(entity="user_c", features={"x": 1.0})
    engine = CorrelationEngine(threshold=0.2)
    clusters = engine.correlate([first, second, third])
    members_sets = [set(cluster["members"]) for cluster in clusters]
    assert len(clusters) == 2
    assert {"user_a", "user_b"} in members_sets
    assert {"user_c"} in members_sets
