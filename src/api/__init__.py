"""API package for the SignalTrace Community Edition.

This package expõe um aplicativo HTTP mínimo (sem dependências externas)
com um conjunto de endpoints que permitem a consumidores externos
executar o núcleo do pipeline SignalTrace CE.  A API é
intencionalmente simples e não requer autenticação nesta fase.  Todas
as entradas devem ser dados sintéticos em conformidade com os schemas
públicos fornecidos no diretório ``schemas/``.

Endpoints provided:

* ``GET /health`` – basic health check returning status information.
* ``GET /schema/event`` – returns the JSON schema used to validate
  incoming events.
* ``POST /normalize`` – accepts a JSON object with an ``events``
  array and returns normalized events.
* ``POST /fingerprint`` – accepts normalized events and returns
  fingerprints for each event.
* ``POST /correlate`` – accepts event fingerprints and returns
  correlated clusters.
* ``POST /score`` – accepts clusters and returns risk‑scored clusters
  with explanatory text.
* ``POST /analyze`` – convenience endpoint that accepts raw events
  and returns an analysis result containing scored clusters and a
  report summary.

See ``docs/api.md`` for detailed documentation on each endpoint.
"""

from .server import create_app  # noqa: F401
