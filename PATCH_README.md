# Registro de Patches

## 0.3.0 - 2026-03-24

- Adicionada camada pública utilizável composta por uma **API local** e uma **CLI pública**.  A API expõe endpoints para healthcheck, obtenção de schema, normalização de eventos, extração de fingerprints, correlação, scoring e análise completa.  A CLI oferece subcomandos `validate`, `run`, `report-json`, `report-md` e `summary`.
- Implementada geração de relatórios explicáveis em JSON e Markdown via `src/report/generator.py`.
- Criados contratos de saída versionados documentados em `docs/contracts.md` e adicionadas validações correspondentes nos testes automatizados.
- Desenvolvida demonstração reproduzível em `examples/synthetic/demo/` mostrando como iniciar a API, rodar a CLI e gerar relatórios usando um dataset sintético.
- Adicionada documentação detalhada em `docs/api.md`, `docs/cli.md`, `docs/demo.md` e atualizada a `README.md` com instruções de uso e limitações.
- Incluídos testes adicionais cobrindo a API, a CLI, geração de relatórios e conformidade dos contratos.

## 0.2.0 - 2026-03-23

- Implementada a primeira fase funcional do motor público com schema observacional, normalização segura, fingerprint comportamental, correlação, scoring, dataset sintético, runner CLI e testes.
- Atualizada documentação em `README.md`, `CHANGELOG.md` e `docs/`.

## 0.3.1 - 2026-03-24

- Corrigida falha nos testes em ambientes Windows relacionada à criação de
  diretórios temporários (`PermissionError: [WinError 5]`).  A
  configuração de testes agora cria um diretório temporário dentro do
  repositório (`tests/tmp`) e exporta as variáveis de ambiente `TMPDIR`,
  `TEMP` e `TMP` para esse local.

