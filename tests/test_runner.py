import os

from src.runner import run_pipeline


def test_run_pipeline_on_synthetic_dataset() -> None:
    path = os.path.join(os.path.dirname(__file__), "..", "examples", "synthetic", "events_dataset_v1.json")
    clusters = run_pipeline(path)
    assert isinstance(clusters, list)
    assert clusters
    for cluster in clusters:
        assert "score" in cluster
        assert "level" in cluster
        assert "members" in cluster
