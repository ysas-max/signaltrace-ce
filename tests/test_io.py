"""Testes para o módulo de IO."""

import json
import os
import tempfile

import pytest

from src.io.reader import load_messages


def test_load_messages_validates_schema() -> None:
    messages = [
        {
            "id": "m1",
            "timestamp": "2025-01-01T00:00:00Z",
            "sender": "user_alpha",
            "receiver": "user_beta",
            "content": "Teste",
        }
    ]
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp_file:
        json.dump(messages, tmp_file)
        tmp_path = tmp_file.name
    try:
        loaded = load_messages(tmp_path)
        assert len(loaded) == 1
    finally:
        os.unlink(tmp_path)


def test_load_messages_raises_on_invalid() -> None:
    invalid_messages = [
        {
            "id": "m2",
            "timestamp": "2025-01-01T00:00:00Z",
            "receiver": "user_beta",
            "content": "Teste",
        }
    ]
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp_file:
        json.dump(invalid_messages, tmp_file)
        tmp_path = tmp_file.name
    try:
        with pytest.raises(Exception):
            load_messages(tmp_path)
    finally:
        os.unlink(tmp_path)
