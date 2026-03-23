"""Classe principal para orquestrar o pipeline do SignalTrace.

O objetivo desta classe é fornecer um ponto de entrada simples para
carregar dados, sanitizar, extrair fingerprints, correlacionar
entidades e produzir scores explicáveis. A implementação atual é mínima
e serve como base para extensões futuras.
"""

from __future__ import annotations

from typing import Any, Dict, List

from ..correlation.engine import CorrelationEngine
from ..fingerprint.extractor import FingerprintExtractor
from ..io.reader import load_messages
from ..sanitization.sanitizer import sanitize_message
from ..scoring.score import ScoreEngine


class SignalTraceEngine:
    """Pipeline principal da edição comunitária do SignalTrace.

    Args:
        fingerprint_extractor: Instância que extrai features.
        correlation_engine: Instância que correlaciona entidades.
        score_engine: Instância que calcula pontuações.

    The engine is designed to be stateless and reentrant; each run
    processes supplied messages independently.
    """

    def __init__(
        self,
        fingerprint_extractor: FingerprintExtractor | None = None,
        correlation_engine: CorrelationEngine | None = None,
        score_engine: ScoreEngine | None = None,
    ) -> None:
        self.fingerprint_extractor = (
            fingerprint_extractor or FingerprintExtractor()
        )
        self.correlation_engine = correlation_engine or CorrelationEngine()
        self.score_engine = score_engine or ScoreEngine()

    def process(self, path: str) -> List[Dict[str, Any]]:
        """Executa o pipeline completo em um arquivo JSON.

        Args:
            path: Caminho para o arquivo com mensagens sintéticas.

        Returns:
            Lista de resultados com correlação e score por entidade.
        """
        messages = load_messages(path)
        sanitized = [sanitize_message(message) for message in messages]
        fingerprints = self.fingerprint_extractor.extract_batch(sanitized)
        correlations = self.correlation_engine.correlate(fingerprints)
        return self.score_engine.score(correlations)
