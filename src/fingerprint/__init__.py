"""Módulo de fingerprint comportamental.

Contém classes responsáveis por extrair características de mensagens
para criar representações quantitativas e comparáveis.
"""

from .extractor import Fingerprint, FingerprintExtractor

__all__ = ["FingerprintExtractor", "Fingerprint"]
