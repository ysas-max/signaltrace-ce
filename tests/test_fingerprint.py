"""Testes para o módulo de fingerprint."""

from src.fingerprint.extractor import FingerprintExtractor


def test_fingerprint_extractor_creates_features() -> None:
    extractor = FingerprintExtractor()
    messages = [
        {"sender": "user_alpha", "content": "Olá mundo"},
        {"sender": "user_alpha", "content": "Teste de mensagem"},
    ]
    fingerprints = extractor.extract_batch(messages)
    assert len(fingerprints) == 1
    fingerprint = fingerprints[0]
    assert fingerprint.entity == "user_alpha"
    assert "avg_message_length" in fingerprint.features
    assert fingerprint.features["avg_message_length"] > 0
