from src.normalization.normalizer import Normalizer


def test_normalize_generates_flags_and_tokens() -> None:
    normalizer = Normalizer()
    event = {
        "event_id": "e1",
        "source_type": "sms",
        "observed_at": "2025-01-01T00:00:00Z",
        "message_text": "PROMOÇÃO! PROMOÇÃO! promoção!",
        "sender_handle": "sender",
        "sender_hash": "c" * 64,
        "domain_hint": "promo.exemplo.com",
        "campaign_markers": ["Promoção"],
    }
    normalized = normalizer.normalize(event)
    assert normalized["message_text"].islower()
    assert "promoção" in normalized["normalized_tokens"]
    assert "repetitivo" in normalized["risk_flags"]
    assert "keyword-suspeita" in normalized["risk_flags"]
    assert "dominio-suspeito" in normalized["risk_flags"]
