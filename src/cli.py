"""Interface de linha de comando (CLI) do SignalTrace CE.

Este módulo define subcomandos para interagir com o motor de análise
utilizando apenas dados sintéticos.  Ele oferece utilitários para
validar datasets, executar o pipeline completo e gerar relatórios em
diversos formatos.  A CLI facilita a auditoria e inspeção local do
comportamento do sistema sem dependências externas.

Subcomandos disponíveis:

- ``validate``: valida um arquivo JSON de eventos contra o schema público.
- ``run``: executa o pipeline e imprime no terminal um resumo de cada cluster.
- ``report-json``: executa o pipeline e grava o resultado estruturado em um arquivo JSON.
- ``report-md``: executa o pipeline e grava um relatório em Markdown legível por humanos.
- ``summary``: executa o pipeline e imprime apenas estatísticas agregadas no terminal.

Todos os comandos respeitam as regras rígidas da comunidade: não há
coleta agressiva de dados, apenas dados sintéticos podem ser
processados e os resultados são interpretados como indicadores, não
provas categóricas.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, List

from .io.event_reader import load_events
from .reporting.report import (
    generate_json_report,
    generate_markdown_report,
    print_summary,
)
from .runner import run_pipeline


def _validate_dataset(path: str) -> List[Any]:
    """Carrega e valida eventos a partir de um arquivo JSON.

    Lança exceções se o arquivo não existir ou se algum evento violar
    o schema.  Retorna a lista de eventos carregados em caso de
    sucesso.
    """
    return load_events(path)


def cmd_validate(args: argparse.Namespace) -> int:
    """Executa o subcomando ``validate``.

    Imprime o número de eventos se a validação for bem‑sucedida.
    """
    try:
        events = _validate_dataset(args.input)
    except FileNotFoundError as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Falha na validação: {e}", file=sys.stderr)
        return 1
    print(f"Arquivo válido. {len(events)} evento(s) carregado(s).")
    return 0


def _run_and_get_clusters(path: str) -> tuple[list[dict[str, Any]], int]:
    """Executa o pipeline completo e retorna clusters e contagem de eventos.

    Para obter a contagem de eventos, carrega o arquivo de eventos
    diretamente.  Em seguida, utiliza ``run_pipeline`` para processar
    o arquivo e obter os clusters anotados com scores.
    """
    events = _validate_dataset(path)
    clusters = run_pipeline(path)
    return clusters, len(events)


def cmd_run(args: argparse.Namespace) -> int:
    """Executa o pipeline completo e imprime os clusters no terminal."""
    try:
        clusters, _ = _run_and_get_clusters(args.input)
    except Exception as e:
        print(f"Erro ao executar pipeline: {e}", file=sys.stderr)
        return 1
    if not clusters:
        print("Nenhum cluster encontrado.")
        return 0
    for idx, cluster in enumerate(clusters, start=1):
        print(f"\nCluster {idx}")
        print(f"  Membros: {', '.join(cluster.get('members', []))}")
        score = cluster.get('score', 0.0)
        level = cluster.get('level', 'desconhecido')
        print(f"  Score: {score:.2f} ({level})")
        print(f"  Explicação: {cluster.get('explanation', '')}")
    return 0


def cmd_report_json(args: argparse.Namespace) -> int:
    """Gera um relatório completo em JSON e grava em ``args.output``."""
    try:
        clusters, events_count = _run_and_get_clusters(args.input)
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}", file=sys.stderr)
        return 1
    output = Path(args.output)
    try:
        generate_json_report(clusters, events_count, str(output))
    except Exception as e:
        print(f"Falha ao escrever relatório JSON: {e}", file=sys.stderr)
        return 1
    print(f"Relatório JSON gerado em {output}")
    return 0


def cmd_report_md(args: argparse.Namespace) -> int:
    """Gera um relatório em Markdown e grava em ``args.output``."""
    try:
        clusters, events_count = _run_and_get_clusters(args.input)
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}", file=sys.stderr)
        return 1
    output = Path(args.output)
    try:
        generate_markdown_report(clusters, events_count, str(output))
    except Exception as e:
        print(f"Falha ao escrever relatório Markdown: {e}", file=sys.stderr)
        return 1
    print(f"Relatório Markdown gerado em {output}")
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    """Imprime apenas o resumo agregado no terminal."""
    try:
        clusters, events_count = _run_and_get_clusters(args.input)
    except Exception as e:
        print(f"Erro ao gerar resumo: {e}", file=sys.stderr)
        return 1
    print_summary(clusters, events_count)
    return 0


def main(argv: List[str] | None = None) -> None:
    """Ponto de entrada para a CLI.

    Este método configura o parser de argumentos, registra os
    subcomandos e delega a execução para a função apropriada.
    """
    parser = argparse.ArgumentParser(
        description="Interface de linha de comando para o SignalTrace CE",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando validate
    p_validate = subparsers.add_parser(
        "validate",
        help="Valida um arquivo JSON de eventos sintéticos",
    )
    p_validate.add_argument("--input", required=True, help="Caminho para o arquivo JSON de eventos")
    p_validate.set_defaults(func=cmd_validate)

    # Subcomando run
    p_run = subparsers.add_parser(
        "run",
        help="Executa o pipeline completo e imprime resumo por cluster",
    )
    p_run.add_argument("--input", required=True, help="Caminho para o arquivo JSON de eventos")
    p_run.set_defaults(func=cmd_run)

    # Subcomando report-json
    p_json = subparsers.add_parser(
        "report-json",
        help="Gera um relatório JSON estruturado",
    )
    p_json.add_argument("--input", required=True, help="Caminho para o arquivo JSON de eventos")
    p_json.add_argument("--output", required=True, help="Arquivo de saída para o relatório JSON")
    p_json.set_defaults(func=cmd_report_json)

    # Subcomando report-md
    p_md = subparsers.add_parser(
        "report-md",
        help="Gera um relatório em Markdown",
    )
    p_md.add_argument("--input", required=True, help="Caminho para o arquivo JSON de eventos")
    p_md.add_argument("--output", required=True, help="Arquivo de saída para o relatório em Markdown")
    p_md.set_defaults(func=cmd_report_md)

    # Subcomando summary
    p_summary = subparsers.add_parser(
        "summary",
        help="Imprime apenas o resumo agregado",
    )
    p_summary.add_argument("--input", required=True, help="Caminho para o arquivo JSON de eventos")
    p_summary.set_defaults(func=cmd_summary)

    args = parser.parse_args(argv)
    # Chama a função associada ao subcomando
    exit_code = args.func(args)
    sys.exit(exit_code)


if __name__ == "__main__":  # pragma: no cover
    main()