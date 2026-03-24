from src.fingerprint.event import EventFingerprintExtractor
from src.normalization.normalizer import Normalizer
from src.scoring.risk import RiskScorer


def test_risk_scoring_assigns_level() -> None:
    events = [
        {
            "event_id": "e1",
            "source_type": "sms",
            "observed_at": "2025-01-01T00:00:00Z",
            "message_text": "promoção especial, clique aqui",
            "sender_handle": "a",
            "sender_hash": "a" * 64,
            "domain_hint": "promo.com",
            "campaign_markers": ["promo"],
        },
        {
            "event_id": "e2",
            "source_type": "sms",
            "observed_at": "2025-01-01T00:10:00Z",
            "message_text": "Promoção especial, clique aqui agora",
            "sender_handle": "b",
            "sender_hash": "b" * 64,
            "domain_hint": "promo.com",
            "campaign_markers": ["promo"],
        },
    ]
    norm = Normalizer()
    fps = EventFingerprintExtractor(norm.suspicious_keywords).extract_batch([norm.normalize(e) for e in events])
    cluster = {"center": fps[0].event_id, "members": [fp.event_id for fp in fps], "fingerprints": fps}
    scored = RiskScorer().score([cluster])[0]
    assert 0.0 <= scored["score"] <= 1.0
    assert scored["level"] in {"baixo", "moderado", "alto", "crítico"}
    assert scored["explanation"]
