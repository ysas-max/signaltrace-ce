"""Extração de fingerprints comportamentais.

Este módulo define a classe `FingerprintExtractor`, responsável por
gerar representações simplificadas de comportamento com base em
mensagens sanitizadas. As fingerprints são utilizadas em seguida pelos
módulos de correlação e scoring.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Fingerprint:
    """Representação de uma fingerprint comportamental.

    Attributes:
        entity: Identificador sintético do remetente ou grupo analisado.
        features: Mapa de características numéricas extraídas.
    """

    entity: str
    features: Dict[str, float]


class FingerprintExtractor:
    """Extrai fingerprints de mensagens sanitizadas.

    A implementação atual utiliza métricas simples como comprimento
    médio das mensagens, contagem de palavras e um placeholder para o
    tempo médio entre mensagens.
    """

    def extract_batch(
        self,
        messages: List[Dict[str, Any]],
    ) -> List[Fingerprint]:
        """Extrai fingerprints para cada remetente nas mensagens."""
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for message in messages:
            sender = message.get("sender")
            grouped.setdefault(sender, []).append(message)

        fingerprints: List[Fingerprint] = []
        for sender, sender_messages in grouped.items():
            total_length = sum(
                len(message.get("content", ""))
                for message in sender_messages
            )
            avg_length = (
                total_length / len(sender_messages)
                if sender_messages
                else 0.0
            )
            unique_words = len(
                {
                    word.lower()
                    for message in sender_messages
                    for word in message.get("content", "").split()
                }
            )
            features = {
                "avg_message_length": avg_length,
                "unique_words": float(unique_words),
                "time_between_messages": 0.0,
            }
            fingerprints.append(Fingerprint(entity=sender, features=features))

        return fingerprints
