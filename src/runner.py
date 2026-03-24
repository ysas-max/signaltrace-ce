from __future__ import annotations

import argparse
from typing import Any, Dict, List

from .correlation.event_correlation import EventCorrelationEngine
from .fingerprint.event import EventFingerprintExtractor
from .io.event_reader import load_events
from .normalization.normalizer import Normalizer
from .scoring.risk import RiskScorer


def run_pipeline(path: str) -> List[Dict[str, Any]]:
    events = load_events(path)
    normalizer = Normalizer()
    normalized_events = [normalizer.normalize(evt) for evt in events]
    extractor = EventFingerprintExtractor(suspicious_keywords=normalizer.suspicious_keywords)
    fingerprints = extractor.extract_batch(normalized_events)
    clusters = EventCorrelationEngine().correlate(fingerprints)
    return RiskScorer().score(clusters)


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa o motor SignalTrace CE em um dataset sintético de eventos.")
    parser.add_argument("--input", type=str, default="examples/synthetic/events_dataset_v1.json")
    args = parser.parse_args()
    clusters = run_pipeline(args.input)
    print(f"Foram encontrados {len(clusters)} cluster(s).")
    for idx, cluster in enumerate(clusters, start=1):
        print(f"\nCluster {idx}")
        print(f"  Eventos: {', '.join(cluster.get('members', []))}")
        print(f"  Score: {cluster.get('score', 0.0):.2f} ({cluster.get('level', 'desconhecido')})")
        print(f"  Explicação: {cluster.get('explanation', '')}")


if __name__ == "__main__":
    main()
