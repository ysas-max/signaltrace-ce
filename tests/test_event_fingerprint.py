from src.fingerprint.event import EventFingerprintExtractor
from src.normalization.normalizer import Normalizer


def test_event_fingerprint_extraction() -> None:
    normalizer = Normalizer()
    event = {
        "event_id": "e2",
        "source_type": "sms",
        "observed_at": "2025-01-01T00:00:00Z",
        "message_text": "Olá mundo!",
        "sender_handle": "sender",
        "sender_hash": "d" * 64,
    }
    normalized = normalizer.normalize(event)
    fp = EventFingerprintExtractor(normalizer.suspicious_keywords).extract(normalized)
    assert fp.event_id == "e2"
    assert fp.features["text_length"] > 0
    assert isinstance(fp.tokens, set)
