"""CLI entry point for SignalTrace CE.

This module defines the ``main`` function which can be invoked either
directly via ``python -m src.cli.main`` or through an installed
console script entry point.  The CLI uses :mod:`argparse` to expose
subcommands that correspond to common tasks such as validating
datasets, running the analysis pipeline and generating reports.

Throughout the CLI we emphasise that the data must be synthetic and
that correlations are not proofs.  Exiting with a non‑zero status
code on failure allows integration into CI pipelines.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from ..contracts.schema import load_schema
from ..io.event_reader import load_events
from ..report.generator import generate_analysis_result, generate_markdown_report


def _load_events(path: str) -> List[Dict[str, Any]]:
    """Helper to load events from a file path.

    Wraps :func:`load_events` and converts common exceptions into
    user friendly messages.
    """
    try:
        return load_events(path)
    except Exception as exc:
        raise SystemExit(f"Erro ao carregar eventos: {exc}")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Interface de linha de comando para o SignalTrace CE"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # validate command
    p_validate = sub.add_parser(
        "validate", help="Valida um dataset sintético contra o schema de evento"
    )
    p_validate.add_argument(
        "--input", required=True, help="Caminho para o arquivo JSON de eventos"
    )

    # run command
    p_run = sub.add_parser(
        "run", help="Executa o pipeline completo e imprime resumo"
    )
    p_run.add_argument(
        "--input", required=True, help="Caminho para o arquivo JSON de eventos"
    )

    # report-json command
    p_rjson = sub.add_parser(
        "report-json", help="Gera relatório em JSON e salva em arquivo"
    )
    p_rjson.add_argument("--input", required=True, help="Caminho para o arquivo de eventos")
    p_rjson.add_argument(
        "--output", required=True, help="Arquivo de saída para o relatório JSON"
    )

    # report-md command
    p_rmd = sub.add_parser(
        "report-md", help="Gera relatório em Markdown e salva em arquivo"
    )
    p_rmd.add_argument("--input", required=True, help="Caminho para o arquivo de eventos")
    p_rmd.add_argument(
        "--output", required=True, help="Arquivo de saída para o relatório Markdown"
    )

    # summary command
    p_sum = sub.add_parser(
        "summary", help="Imprime apenas o resumo do relatório no terminal"
    )
    p_sum.add_argument("--input", required=True, help="Caminho para o arquivo de eventos")
    return parser


def _print_summary(summary: Dict[str, Any]) -> None:
    """Imprime um resumo amigável no terminal.

    Este helper formata a saída de forma consistente com os testes.  Ele
    começa sempre com ``Total de eventos`` e ``Total de clusters`` para
    facilitar a verificação automatizada e a leitura humana.  Campos
    adicionais como distribuição de níveis, marcadores e flags
    aparecem apenas se presentes.
    """
    # Linhas iniciais esperadas pelos testes
    print(f"Total de eventos: {summary.get('total_events', 0)}")
    print(f"Total de clusters: {summary.get('total_clusters', 0)}")
    risk_levels = summary.get("risk_levels", {})
    if risk_levels:
        print("Distribuição de níveis de risco:")
        for level, count in risk_levels.items():
            print(f"  - {level}: {count}")
    top_markers = summary.get("top_markers", [])
    if top_markers:
        print("Marcadores mais frequentes: " + ", ".join(top_markers))
    top_flags = summary.get("top_risk_flags", [])
    if top_flags:
        print("Sinais de risco mais frequentes: " + ", ".join(top_flags))
    print(f"Aviso: {summary.get('warning')}")


def main(argv: List[str] | None = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)
    if args.command == "validate":
        # Simply attempt to load events. load_events will validate.
        _ = _load_events(args.input)
        print("Dataset válido.")
    elif args.command == "run":
        events = _load_events(args.input)
        result = generate_analysis_result(events)
        _print_summary(result.get("summary", {}))
    elif args.command == "report-json":
        events = _load_events(args.input)
        result = generate_analysis_result(events)
        output_path = Path(args.output)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Relatório JSON salvo em {output_path}")
    elif args.command == "report-md":
        events = _load_events(args.input)
        result = generate_analysis_result(events)
        md = generate_markdown_report(result)
        output_path = Path(args.output)
        with output_path.open("w", encoding="utf-8") as f:
            f.write(md)
        print(f"Relatório Markdown salvo em {output_path}")
    elif args.command == "summary":
        events = _load_events(args.input)
        result = generate_analysis_result(events)
        _print_summary(result.get("summary", {}))
    else:
        parser.error(f"Comando desconhecido: {args.command}")


if __name__ == "__main__":
    main(sys.argv[1:])
