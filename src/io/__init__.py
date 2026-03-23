"""Módulo de entrada e saída para o SignalTrace CE.

Define funções para carregar e salvar dados em formatos suportados,
como JSON.
"""

from .reader import load_messages

__all__ = ["load_messages"]
