"""Testes para o módulo de scoring."""

from src.scoring.score import ScoreEngine


def test_score_engine_assigns_score_and_explanation() -> None:
    engine = ScoreEngine()
    clusters = [
        {"center": "user_a", "members": ["user_a", "user_b"]},
        {"center": "user_c", "members": ["user_c"]},
    ]
    scored = engine.score(clusters)
    assert len(scored) == 2
    for cluster in scored:
        assert "score" in cluster
        assert "explanation" in cluster
        assert isinstance(cluster["score"], float)
