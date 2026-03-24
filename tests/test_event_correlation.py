from src.correlation.event_correlation import EventCorrelationEngine
from src.fingerprint.event import EventFingerprintExtractor
from src.normalization.normalizer import Normalizer


def test_event_correlation_clusters_similar_events() -> None:
    events = [
        {
            "event_id": "e1",
            "source_type": "sms",
            "observed_at": "2025-01-01T00:00:00Z",
            "message_text": "Bônus incrível! Visite bonus.com para resgatar.",
            "sender_handle": "a",
            "sender_hash": "a" * 64,
            "domain_hint": "bonus.com",
            "campaign_markers": ["bonus"],
        },
        {
            "event_id": "e2",
            "source_type": "sms",
            "observed_at": "2025-01-01T00:05:00Z",
            "message_text": "bônus incrível! visite bonus.com para resgatar.",
            "sender_handle": "b",
            "sender_hash": "b" * 64,
            "domain_hint": "bonus.com",
            "campaign_markers": ["bonus"],
        },
        {
            "event_id": "e3",
            "source_type": "sms",
            "observed_at": "2025-01-02T00:00:00Z",
            "message_text": "Mensagem diferente em outro domínio.",
            "sender_handle": "c",
            "sender_hash": "c" * 64,
            "domain_hint": "outro.com",
            "campaign_markers": [],
        },
    ]
    norm = Normalizer()
    fps = EventFingerprintExtractor(norm.suspicious_keywords).extract_batch([norm.normalize(e) for e in events])
    clusters = EventCorrelationEngine(threshold=0.5).correlate(fps)
    assert sorted(len(c["members"]) for c in clusters) == [1, 2]
