from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set


@dataclass
class Normalizer:
    """Normaliza campos de eventos observacionais.

    Esta classe limpa e padroniza o texto das mensagens, remove
    caracteres não alfanuméricos, converte para minúsculas,
    extrai tokens e determina flags de risco simples com base em
    repetição e palavras‑chave suspeitas.
    """

    suspicious_keywords: List[str] = field(
        default_factory=lambda: [
            "bonus", "bônus", "promocao", "promoção", "casino",
            "cassino", "gratis", "grátis", "oferta", "clique", "agora",
        ]
    )
    repetition_threshold: float = 0.4

    def normalize(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna uma cópia normalizada do evento."""
        normalized = dict(event)
        text = normalized.get("message_text", "")
        # limpar caracteres especiais e normalizar espaços
        text_clean = re.sub(r"[^\w\s]", " ", text.lower())
        text_clean = re.sub(r"\s+", " ", text_clean).strip()
        normalized["message_text"] = text_clean
        tokens = re.findall(r"\b\w+\b", text_clean)
        normalized["normalized_tokens"] = tokens

        flags: Set[str] = set(normalized.get("risk_flags", []))
        if tokens:
            counts = Counter(tokens)
            _, most_common_count = counts.most_common(1)[0]
            if (most_common_count / len(tokens)) >= self.repetition_threshold:
                flags.add("repetitivo")
        for kw in self.suspicious_keywords:
            if kw.lower() in tokens:
                flags.add("keyword-suspeita")
                break

        # normalizar domínio e detectar domínios suspeitos
        domain = normalized.get("domain_hint")
        if isinstance(domain, str) and domain:
            domain_lower = domain.lower().strip()
            parts = domain_lower.split(".")
            domain_norm = ".".join(parts[-2:]) if len(parts) > 2 else domain_lower
            normalized["domain_hint"] = domain_norm
            for suspicious in ["bonus", "promo", "casino", "cassino", "xyz"]:
                if suspicious in domain_lower:
                    flags.add("dominio-suspeito")
                    break

        markers = normalized.get("campaign_markers")
        if isinstance(markers, list):
            normalized["campaign_markers"] = [str(m).strip().lower() for m in markers]

        dest = normalized.get("destination_hint")
        if isinstance(dest, str):
            normalized["destination_hint"] = dest.strip().lower()

        normalized["risk_flags"] = sorted(flags)
        return normalized
