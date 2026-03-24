import json
import os
import tempfile

import pytest

from src.io.event_reader import load_events


def test_load_events_valid() -> None:
    events = [{
        "event_id": "e1",
        "source_type": "sms",
        "observed_at": "2025-01-01T00:00:00Z",
        "message_text": "Teste de evento",
        "sender_handle": "user",
        "sender_hash": "a" * 64,
    }]
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        json.dump(events, tmp)
        tmp_path = tmp.name
    try:
        assert len(load_events(tmp_path)) == 1
    finally:
        os.unlink(tmp_path)


def test_load_events_invalid() -> None:
    events = [{
        "source_type": "sms",
        "observed_at": "2025-01-01T00:00:00Z",
        "message_text": "Teste",
        "sender_handle": "user",
        "sender_hash": "b" * 64,
    }]
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        json.dump(events, tmp)
        tmp_path = tmp.name
    try:
        with pytest.raises(Exception):
            load_events(tmp_path)
    finally:
        os.unlink(tmp_path)
