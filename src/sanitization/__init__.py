"""Módulo de sanitização pública.

Fornece funções para remover ou mascarar dados potencialmente sensíveis
antes do processamento analítico.
"""

from .sanitizer import sanitize_message

__all__ = ["sanitize_message"]
