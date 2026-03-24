# Changelog


## [0.2.0] - 2026-03-23

### Adicionado

- Schema de evento observacional `schemas/event_schema_v1.json`.
- Pipeline de normalização em `src/normalization/normalizer.py`.
- Fingerprint comportamental em `src/fingerprint/event.py`.
- Correlação básica em `src/correlation/event_correlation.py`.
- Scoring configurável em `src/scoring/risk.py`.
- Dataset sintético `examples/synthetic/events_dataset_v1.json`.
- Runner CLI `src/runner.py`.
- Testes unitários para schema, normalização, fingerprint, correlação, scoring e runner.
- Documentação adicional em `docs/schema_event.md`, `docs/scoring.md` e `docs/engine_flow.md`.

### Alterado

- Atualizado `README.md`.
- Atualizado `PATCH_README.md`.

## [0.3.0] - 2026-03-24

### Adicionado

- API local em `src/api/server.py` com endpoints para healthcheck,
  obtenção de schema, normalização de eventos, extração de fingerprints,
  correlação, scoring e análise completa (`/health`, `/schema/event`,
  `/normalize`, `/fingerprint`, `/correlate`, `/score` e `/analyze`).
- CLI pública em `src/cli/main.py` com subcomandos `validate`, `run`,
  `report-json`, `report-md` e `summary` para validar datasets,
  executar o pipeline completo, gerar relatórios e imprimir resumos.
- Módulo de geração de relatórios em `src/report/generator.py` com
  funções para produzir o contrato `analysis_result_v1` e converter
  resultados em Markdown.
- Contrato de saída documentado em `docs/contracts.md` incluindo
  `analysis_result_v1`, `cluster_result_v1` e `report_summary_v1`.
- Documentação da API (`docs/api.md`), CLI (`docs/cli.md`) e demo
  reproduzível (`docs/demo.md`).
- Demo sintética reproduzível descrita em `docs/demo.md` que mostra
  como iniciar a API, validar dados, executar o pipeline e gerar
  relatórios.
- Testes unitários cobrindo os novos endpoints da API, comandos da
  CLI, geração de relatórios e contratos de saída.

### Alterado

- Atualizado `README.md` com descrição das novas interfaces e links
  para a documentação.
- Atualizado `PATCH_README.md` para registrar a nova versão.

### Mantido

- O motor interno de normalização, fingerprint, correlação e scoring
  permanece inalterado em termos de lógica básica, garantindo
  retrocompatibilidade com datasets sintéticos e testes existentes.

## [0.3.1] - 2026-03-24

### Corrigido

- Corrigido erro de permissão que ocorria em ambientes Windows ao
  executar a suíte de testes.  A configuração de testes (`tests/conftest.py`)
  agora cria um diretório temporário dentro do repositório e define
  as variáveis de ambiente `TMPDIR`, `TEMP` e `TMP` para apontar para
  esse local, evitando que o Pytest utilize pastas protegidas (como
  `AppData\Local\Temp`) e evitando erros `PermissionError: [WinError 5]`.
