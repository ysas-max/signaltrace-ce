from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Set


@dataclass
class EventFingerprint:
    """Representa um fingerprint comportamental extraído de um evento."""

    event_id: str
    features: Dict[str, float]
    tokens: Set[str]
    domain: Optional[str]
    markers: Set[str]
    observed_time: datetime
    risk_flags: Set[str]


class EventFingerprintExtractor:
    """Extrai fingerprints comportamentais de eventos normalizados."""

    def __init__(self, suspicious_keywords: Optional[List[str]] = None) -> None:
        self.suspicious_keywords = [kw.lower() for kw in suspicious_keywords] if suspicious_keywords else []

    def _parse_time(self, ts: str) -> datetime:
        try:
            if ts.endswith("Z"):
                ts = ts[:-1] + "+00:00"
            return datetime.fromisoformat(ts)
        except Exception:
            return datetime(1970, 1, 1)

    def extract(self, event: Dict[str, Any]) -> EventFingerprint:
        tokens = set(event.get("normalized_tokens", []))
        risk_flags = set(event.get("risk_flags", []))
        markers = set(event.get("campaign_markers", [])) if event.get("campaign_markers") else set()
        suspicious_count = sum(1.0 for t in tokens if t in self.suspicious_keywords)
        features = {
            "text_length": float(len(event.get("message_text", ""))),
            "unique_token_count": float(len(tokens)),
            "suspicious_keyword_count": suspicious_count,
            "repetitive": 1.0 if "repetitivo" in risk_flags else 0.0,
            "domain_suspicious": 1.0 if "dominio-suspeito" in risk_flags else 0.0,
            "marker_count": float(len(markers)),
        }
        return EventFingerprint(
            event_id=str(event.get("event_id")),
            features=features,
            tokens=tokens,
            domain=event.get("domain_hint"),
            markers=markers,
            observed_time=self._parse_time(str(event.get("observed_at", "1970-01-01T00:00:00Z"))),
            risk_flags=risk_flags,
        )

    def extract_batch(self, events: List[Dict[str, Any]]) -> List[EventFingerprint]:
        return [self.extract(e) for e in events]
