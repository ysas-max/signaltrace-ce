"""Testes para o módulo de sanitização."""

from src.sanitization.sanitizer import sanitize_message


def test_sanitize_message_masks_phone_and_email() -> None:
    msg = {
        "content": "Contato: 123-456-7890 e email: user@example.org",
        "sender": "user_test",
    }
    sanitized = sanitize_message(msg)
    assert "<PHONE>" in sanitized["content"]
    assert "<EMAIL>" in sanitized["content"]
