"""Módulo de contratos e schemas.

Responsável por carregar e fornecer acesso aos schemas públicos
versionados definidos em `schemas/`. Facilita a validação de dados de
entrada e saída.
"""

from .schema import load_schema

__all__ = ["load_schema"]
