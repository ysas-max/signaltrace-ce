"""Módulo central do motor SignalTrace.

Esta subpasta contém classes e utilitários fundamentais para
orquestrar as etapas de carregamento de dados, extração de
fingerprints, correlação e scoring.
"""

from .engine import SignalTraceEngine

__all__ = ["SignalTraceEngine"]
