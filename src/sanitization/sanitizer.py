"""Funções de sanitização de mensagens.

Este módulo define utilitários para proteger informações
potencialmente sensíveis, como números de telefone e e-mails,
substituindo-os por máscaras. A sanitização é aplicada antes de
qualquer análise.
"""

from __future__ import annotations

import re
from typing import Any, Dict


PHONE_REGEX = re.compile(r"\b\d{3}[-\.\s]\d{3}[-\.\s]\d{4}\b")
EMAIL_REGEX = re.compile(r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}")


def sanitize_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """Retorna uma cópia sanitizada de uma mensagem."""
    sanitized = dict(message)
    content = sanitized.get("content", "")
    content = PHONE_REGEX.sub("<PHONE>", content)
    content = EMAIL_REGEX.sub("<EMAIL>", content)
    sanitized["content"] = content
    return sanitized
