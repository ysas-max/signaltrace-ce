"""API pública local do SignalTrace CE.

Este módulo define um pequeno servidor HTTP baseado em Flask que expõe
operações para processar um lote de eventos sintéticos.  Ele oferece
endpoints para verificação de saúde (`/health`), informação de versão
do contrato (`/version`) e execução de análise (`/analyze`).

As funções de processamento reutilizam as camadas internas de
normalização, extração de fingerprints, correlação e scoring para
produzir um resultado estruturado conforme `analysis_result`.  Os
resultados incluem avisos explícitos de que correlação e score não
constituem prova categórica.

O servidor é destinado apenas a uso local e não implementa
autenticação nem limitações de taxa nesta fase.  Apenas dados
sintéticos devem ser enviados pelo cliente.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Tuple

# Tenta importar Flask; se não disponível, usa implementação de fallback
try:
    from flask import Flask, jsonify, request
    _USE_FLASK = True
except ImportError:  # pragma: no cover
    # Fornece implementações mínimas de ``jsonify`` e ``request``
    _USE_FLASK = False
    Flask = None  # tipo: ignore
    def jsonify(obj: Any) -> Any:  # type: ignore[misc]
        """Fallback simples que retorna o objeto como está.

        Em ausência do Flask, a API retorna dicionários brutos e o
        cliente de testes encapsula esses valores em objetos que
        expõem ``get_json()``.
        """
        return obj

    class _DummyRequest:
        """Objeto de request mínimo para satisfazer imports.
        Não deve ser usado em ambiente de fallback.
        """
        @staticmethod
        def get_json(force: bool = False) -> Any:
            raise RuntimeError("request context não está disponível no modo de fallback")

    request = _DummyRequest()  # type: ignore

from .correlation.event_correlation import EventCorrelationEngine
from .fingerprint.event import EventFingerprintExtractor
from .normalization.normalizer import Normalizer
from .reporting.report import generate_analysis_result
from .scoring.risk import RiskScorer


# Configura logger básico para a aplicação
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#: Versão da aplicação.  Atualize ao modificar contratos ou interfaces.
APP_VERSION = "0.3.0"

#: Versão do schema de saída retornado pela API.
SCHEMA_VERSION = "analysis_result_v1"

# A instância ``app`` será definida dinamicamente mais abaixo, dependendo da
# disponibilidade do Flask.  Ela deve expor um método ``test_client``
# compatível com os testes.
app: Any  # será inicializada posteriormente

# Configuração das rotas dependendo da disponibilidade do Flask
if _USE_FLASK:
    # Instancia o Flask e registra rotas utilizando os handlers definidos.
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health() -> Any:  # pragma: no cover - simples delegação
        return jsonify(health_handler())

    @app.route("/version", methods=["GET"])
    def version() -> Any:  # pragma: no cover - simples delegação
        return jsonify(version_handler())

    @app.route("/analyze", methods=["POST"])
    def analyze() -> Any:  # pragma: no cover - parsing de request
        try:
            payload = request.get_json(force=True)
        except Exception:
            return jsonify({"error": "Corpo inválido ou não parseável como JSON."}), 400
        if not isinstance(payload, list):
            return jsonify({"error": "Corpo deve ser uma lista de eventos."}), 400
        events: List[Dict[str, Any]] = []
        for idx, obj in enumerate(payload, start=1):
            if not isinstance(obj, dict):
                return jsonify({"error": f"Evento na posição {idx} não é um objeto."}), 400
            events.append(dict(obj))
        try:
            result = analyze_handler(events)
        except Exception:
            logger.exception("Erro interno ao processar eventos")
            return jsonify({"error": "Erro interno ao processar eventos."}), 500
        return jsonify(result)
else:
    # Implementação de fallback minimalista quando Flask não está disponível.
    class _DummyResponse:
        def __init__(self, data: Any, status_code: int = 200) -> None:
            self._data = data
            self.status_code = status_code

        def get_json(self) -> Any:
            return self._data

    class _DummyClient:
        """Cliente de teste minimalista que chama handlers diretamente."""

        def get(self, path: str) -> _DummyResponse:
            if path == "/health":
                return _DummyResponse(health_handler())
            if path == "/version":
                return _DummyResponse(version_handler())
            return _DummyResponse({"error": "Path não suportado"}, 404)

        def post(self, path: str, data: Any = None, content_type: str | None = None) -> _DummyResponse:
            if path != "/analyze":
                return _DummyResponse({"error": "Path não suportado"}, 404)
            # assume que data já é JSON serializado (string/bytes) ou lista de eventos
            try:
                events_raw: Any
                if isinstance(data, (str, bytes)):
                    events_raw = json.loads(data)
                else:
                    events_raw = data
            except Exception:
                return _DummyResponse({"error": "Corpo inválido ou não parseável como JSON."}, 400)
            if not isinstance(events_raw, list):
                return _DummyResponse({"error": "Corpo deve ser uma lista de eventos."}, 400)
            events: List[Dict[str, Any]] = []
            for idx, obj in enumerate(events_raw, start=1):
                if not isinstance(obj, dict):
                    return _DummyResponse({"error": f"Evento na posição {idx} não é um objeto."}, 400)
                events.append(dict(obj))
            try:
                result = analyze_handler(events)
            except Exception:
                logger.exception("Erro interno ao processar eventos (fallback)")
                return _DummyResponse({"error": "Erro interno ao processar eventos."}, 500)
            return _DummyResponse(result)

    class _DummyApp:
        def test_client(self) -> _DummyClient:
            return _DummyClient()

    app = _DummyApp()


def _run_pipeline(events: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """Executa o pipeline completo sobre uma lista de eventos.

    Esta função encapsula a sequência de etapas: normalização,
    extração de fingerprints, correlação e scoring.  Retorna os
    clusters anotados com scores e o número total de eventos processados.
    """
    normalizer = Normalizer()
    normalized = [normalizer.normalize(evt) for evt in events]
    extractor = EventFingerprintExtractor(suspicious_keywords=normalizer.suspicious_keywords)
    fingerprints = extractor.extract_batch(normalized)
    clusters = EventCorrelationEngine().correlate(fingerprints)
    scored_clusters = RiskScorer().score(clusters)
    return scored_clusters, len(events)


def health_handler() -> Dict[str, Any]:
    """Retorna um dicionário indicando que o serviço está saudável."""
    return {"status": "ok"}


def version_handler() -> Dict[str, Any]:
    """Retorna um dicionário com a versão da aplicação e do schema."""
    return {"version": APP_VERSION, "schema_version": SCHEMA_VERSION}


def analyze_handler(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Processa um lote de eventos e retorna o objeto analysis_result.

    Lança exceções em caso de falhas internas.
    """
    clusters, total = _run_pipeline(events)
    return generate_analysis_result(clusters, total)


def main() -> None:
    """Executa o servidor Flask localmente.

    O host padrão é `0.0.0.0` e a porta padrão é 8000. Estes valores
    podem ser substituídos configurando as variáveis de ambiente
    `HOST` e `PORT` ou passando argumentos de linha de comando quando
    necessário.  A função registra logs informativos sobre a
    inicialização.
    """
    import os
    host = os.environ.get("HOST", "0.0.0.0")
    port_str = os.environ.get("PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        port = 8000
    logger.info(f"Iniciando API SignalTrace CE na porta {port} (schema {SCHEMA_VERSION})")
    app.run(host=host, port=port)


if __name__ == "__main__":  # pragma: no cover
    main()