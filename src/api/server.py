"""Simple in‑process API for SignalTrace CE.

This module defines a minimal, dependency‑free HTTP‑like API.  It
registers endpoints and exposes a ``test_client`` for programmatic
access.  The API does not implement a real HTTP server; instead, it
focuses on a minimal contract suitable for unit testing and local
integration without external dependencies like Flask.  You may extend
this module in the future to wrap a real web server if desired.

Endpoints provided:

* ``GET /health`` – returns status and timestamp.
* ``GET /schema/event`` – returns the event schema.
* ``POST /normalize`` – normalizes events.
* ``POST /fingerprint`` – extracts fingerprints.
* ``POST /correlate`` – correlates fingerprints into clusters.
* ``POST /score`` – scores clusters.
* ``POST /analyze`` – runs the full pipeline and returns the
  ``analysis_result`` contract.
"""

from __future__ import annotations

import datetime
import json
import os
from typing import Any, Callable, Dict, List, Optional, Tuple

from ..contracts.schema import load_schema
from ..fingerprint.event import EventFingerprint, EventFingerprintExtractor
from ..normalization.normalizer import Normalizer
from ..correlation.event_correlation import EventCorrelationEngine
from ..scoring.risk import RiskScorer


class SimpleResponse:
    """Simple response object mimicking Flask's test response."""

    def __init__(self, status_code: int, data: Any) -> None:
        self.status_code = status_code
        self._data = data

    def get_json(self) -> Any:
        return self._data


class SimpleClient:
    """Client for invoking handlers on a SimpleApp."""

    def __init__(self, app: "SimpleApp") -> None:
        self.app = app

    def get(self, path: str) -> SimpleResponse:
        handler, methods = self.app._routes.get(path, (None, None))
        if handler is None or "GET" not in methods:
            return SimpleResponse(404, {"error": "not found"})
        data, status = handler()
        return SimpleResponse(status, data)

    def post(self, path: str, data: Optional[str] = None, content_type: Optional[str] = None) -> SimpleResponse:
        handler, methods = self.app._routes.get(path, (None, None))
        if handler is None or "POST" not in methods:
            return SimpleResponse(404, {"error": "not found"})
        try:
            body = json.loads(data or "{}")
        except Exception:
            return SimpleResponse(400, {"error": "invalid json"})
        data, status = handler(body)
        return SimpleResponse(status, data)


class SimpleApp:
    """Minimal application that registers route handlers."""

    def __init__(self) -> None:
        # _routes maps path to (handler, methods)
        self._routes: Dict[str, Tuple[Callable[..., Tuple[Any, int]], List[str]]] = {}

    def route(self, path: str, methods: Optional[List[str]] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        methods = methods or ["GET"]

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._routes[path] = (func, methods)
            return func

        return decorator

    def test_client(self) -> SimpleClient:
        return SimpleClient(self)


def _fingerprint_to_dict(fp: EventFingerprint) -> Dict[str, Any]:
    return {
        "event_id": fp.event_id,
        "features": fp.features,
        "tokens": sorted(list(fp.tokens)),
        "domain": fp.domain,
        "markers": sorted(list(fp.markers)),
        "observed_time": fp.observed_time.isoformat(),
        "risk_flags": sorted(list(fp.risk_flags)),
    }


def _cluster_to_dict(cluster: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "cluster_id": cluster.get("center"),
        "members": cluster.get("members", []),
        "fingerprints": [
            _fingerprint_to_dict(fp) for fp in cluster.get("fingerprints", [])
        ],
    }


def _compute_summary(scored_clusters: List[Dict[str, Any]], total_events: int) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "total_events": total_events,
        "total_clusters": len(scored_clusters),
        "risk_levels": {},
        "top_markers": [],
        "top_risk_flags": [],
        "warning": "A correlação não constitui prova categórica."
    }
    levels: Dict[str, int] = {}
    marker_counts: Dict[str, int] = {}
    flag_counts: Dict[str, int] = {}
    for cluster in scored_clusters:
        level = cluster.get("level", "desconhecido")
        levels[level] = levels.get(level, 0) + 1
        for fp in cluster.get("fingerprints", []):
            if isinstance(fp, EventFingerprint):
                markers = fp.markers
                flags = fp.risk_flags
            else:
                markers = set(fp.get("markers", []))
                flags = set(fp.get("risk_flags", []))
            for m in markers:
                marker_counts[m] = marker_counts.get(m, 0) + 1
            for f in flags:
                flag_counts[f] = flag_counts.get(f, 0) + 1
    summary["risk_levels"] = levels
    top_markers = sorted(marker_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    summary["top_markers"] = [m for m, _ in top_markers]
    top_flags = sorted(flag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    summary["top_risk_flags"] = [f for f, _ in top_flags]
    return summary


def create_app() -> SimpleApp:
    """Create and configure the minimal application."""
    app = SimpleApp()
    normalizer = Normalizer()
    extractor = EventFingerprintExtractor(suspicious_keywords=normalizer.suspicious_keywords)
    correlator = EventCorrelationEngine()
    scorer = RiskScorer()

    @app.route("/health", methods=["GET"])
    def health() -> Tuple[Any, int]:
        return {
            "status": "ok",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }, 200

    @app.route("/schema/event", methods=["GET"])
    def event_schema() -> Tuple[Any, int]:
        schema = load_schema("event_schema_v1.json")
        return schema, 200

    @app.route("/normalize", methods=["POST"])
    def normalize(body: Dict[str, Any]) -> Tuple[Any, int]:
        events = body.get("events", []) if isinstance(body, dict) else []
        if not isinstance(events, list):
            return {"error": "events must be a list"}, 400
        normalized = [normalizer.normalize(evt) for evt in events]
        return {"normalized": normalized}, 200

    @app.route("/fingerprint", methods=["POST"])
    def fingerprint(body: Dict[str, Any]) -> Tuple[Any, int]:
        events = body.get("events", []) if isinstance(body, dict) else []
        if not isinstance(events, list):
            return {"error": "events must be a list"}, 400
        fps = extractor.extract_batch(events)
        return {"fingerprints": [_fingerprint_to_dict(fp) for fp in fps]}, 200

    @app.route("/correlate", methods=["POST"])
    def correlate(body: Dict[str, Any]) -> Tuple[Any, int]:
        fps_data = body.get("fingerprints", []) if isinstance(body, dict) else []
        if not isinstance(fps_data, list):
            return {"error": "fingerprints must be a list"}, 400
        fps: List[EventFingerprint] = []
        for item in fps_data:
            try:
                fp = EventFingerprint(
                    event_id=str(item["event_id"]),
                    features=item.get("features", {}),
                    tokens=set(item.get("tokens", [])),
                    domain=item.get("domain"),
                    markers=set(item.get("markers", [])),
                    observed_time=datetime.datetime.fromisoformat(
                        str(item.get("observed_time", "1970-01-01T00:00:00"))
                    ),
                    risk_flags=set(item.get("risk_flags", [])),
                )
                fps.append(fp)
            except Exception:
                return {"error": "invalid fingerprint format"}, 400
        clusters = correlator.correlate(fps)
        return {"clusters": [_cluster_to_dict(c) for c in clusters]}, 200

    @app.route("/score", methods=["POST"])
    def score(body: Dict[str, Any]) -> Tuple[Any, int]:
        clusters_data = body.get("clusters", []) if isinstance(body, dict) else []
        if not isinstance(clusters_data, list):
            return {"error": "clusters must be a list"}, 400
        clusters_internal: List[Dict[str, Any]] = []
        for c in clusters_data:
            fps_list = []
            for fp_dict in c.get("fingerprints", []):
                fp = EventFingerprint(
                    event_id=str(fp_dict["event_id"]),
                    features=fp_dict.get("features", {}),
                    tokens=set(fp_dict.get("tokens", [])),
                    domain=fp_dict.get("domain"),
                    markers=set(fp_dict.get("markers", [])),
                    observed_time=datetime.datetime.fromisoformat(
                        str(fp_dict.get("observed_time", "1970-01-01T00:00:00"))
                    ),
                    risk_flags=set(fp_dict.get("risk_flags", [])),
                )
                fps_list.append(fp)
            clusters_internal.append(
                {
                    "center": c.get("cluster_id"),
                    "members": c.get("members", []),
                    "fingerprints": fps_list,
                }
            )
        scored = scorer.score(clusters_internal)
        result: List[Dict[str, Any]] = []
        for sc in scored:
            cd = _cluster_to_dict(sc)
            cd["score"] = sc.get("score")
            cd["level"] = sc.get("level")
            cd["explanation"] = sc.get("explanation")
            result.append(cd)
        return {"scored_clusters": result}, 200

    @app.route("/analyze", methods=["POST"])
    def analyze(body: Dict[str, Any]) -> Tuple[Any, int]:
        events = body.get("events", []) if isinstance(body, dict) else []
        if not isinstance(events, list):
            return {"error": "events must be a list"}, 400
        normalized = [normalizer.normalize(evt) for evt in events]
        fps = extractor.extract_batch(normalized)
        clusters = correlator.correlate(fps)
        scored = scorer.score(clusters)
        clusters_serialised: List[Dict[str, Any]] = []
        for sc in scored:
            cs = _cluster_to_dict(sc)
            cs["score"] = sc.get("score")
            cs["level"] = sc.get("level")
            cs["explanation"] = sc.get("explanation")
            clusters_serialised.append(cs)
        summary = _compute_summary(scored, total_events=len(events))
        result = {
            "clusters": clusters_serialised,
            "summary": summary,
            "schema_version": "analysis_result_v1",
        }
        return result, 200

    return app


if __name__ == "__main__":
    # Provide a minimal HTTP server using http.server for demonstration.
    import http.server
    import socketserver

    PORT = int(os.environ.get("SIGNALTRACE_API_PORT", 5000))

    app = create_app()

    class Handler(http.server.BaseHTTPRequestHandler):
        def _set_headers(self, code: int) -> None:
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

        def do_GET(self) -> None:
            handler, methods = app._routes.get(self.path, (None, None))
            if handler is None or "GET" not in methods:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "not found"}).encode())
                return
            body, status = handler()
            self._set_headers(status)
            self.wfile.write(json.dumps(body).encode())

        def do_POST(self) -> None:
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length).decode() if length else "{}"
            handler, methods = app._routes.get(self.path, (None, None))
            if handler is None or "POST" not in methods:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "not found"}).encode())
                return
            try:
                body = json.loads(data or "{}")
            except Exception:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "invalid json"}).encode())
                return
            body, status = handler(body)
            self._set_headers(status)
            self.wfile.write(json.dumps(body).encode())

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"SignalTrace CE API rodando em http://localhost:{PORT}")
        httpd.serve_forever()