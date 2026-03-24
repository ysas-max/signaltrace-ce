# SignalTrace Community Edition (signaltrace‑ce)

SignalTrace CE é a versão de **código aberto** da plataforma SignalTrace, focada em análise defensiva e observacional de campanhas suspeitas.  Esta edição comunitária fornece um motor auditável, exemplos sintéticos e documentação completa para permitir contribuições externas sem expor dados sensíveis ou capacidades ofensivas.

## Visão Geral

Esta fase implementa o núcleo funcional mínimo do motor público e expõe interfaces de uso.  O sistema processa eventos observados, aplica normalização segura, extrai fingerprints comportamentais, correlaciona eventos semelhantes e calcula um score de risco configurável.  Os resultados incluem justificativas textuais e são baseados unicamente em dados sintéticos.

Além do motor interno, a versão 0.3 adiciona uma **API local** simples, uma **CLI pública** com múltiplos comandos, geração de relatórios explicáveis em JSON e Markdown e um fluxo de demonstração reproduzível.  Todos os novos componentes seguem as regras rígidas descritas no arquivo `PATCH_README.md` e são totalmente compatíveis com dados sintéticos.

### Missão Defensiva

O objetivo do SignalTrace CE é apoiar pesquisadores e defensores na análise de campanhas de fraude e spam de forma ética, transparente e explicável.  A plataforma **não** faz atribuição categórica de autores ou intenções e **não** oferece funcionalidades ofensivas ou de coleta agressiva.  Correlação e score são apenas indicadores; não devem ser interpretados como provas.

### Componentes Principais

| Componente | Descrição |
| --- | --- |
| **Schemas Públicos** | Descrevem o formato dos eventos observacionais (`schemas/event_schema_v1.json`) e os contratos de saída documentados em [`docs/contracts.md`](docs/contracts.md). |
| **Motor de Normalização** | Padroniza texto, marcadores e domínios de forma segura (`src/normalization/normalizer.py`). |
| **Fingerprint Comportamental** | Resume características não reversíveis de cada evento (`src/fingerprint/event.py`). |
| **Correlação Básica** | Agrupa eventos semelhantes por domínios, tokens, marcadores e tempo (`src/correlation/event_correlation.py`). |
| **Scoring Explicável** | Calcula scores de risco por cluster e gera uma justificativa textual (`src/scoring/risk.py`). |
| **API Local** | Servidor HTTP embutido sem autenticação que expõe endpoints para healthcheck, obtenção de schema e processamento de lotes de eventos (`src/api/server.py`). |
| **CLI Pública** | Executável com subcomandos para validar datasets, executar o pipeline, gerar relatórios JSON/Markdown e imprimir resumos (`src/cli/main.py`). |
| **Geração de Relatórios** | Funções para produzir relatórios explicáveis em JSON e Markdown, incluindo indicadores de limitação e risco de falso positivo (`src/report/generator.py`). |
| **Exemplos Sintéticos** | Campanhas simuladas e scripts de demonstração em `examples/synthetic/`. |

### O que Este Projeto Não Faz

- Não inclui dados reais, credenciais, tokens, telemetria sensível ou evidências operacionais.
- Não contém scraping agressivo, automação ofensiva ou enumeração ativa de serviços externos.
- Não depende de serviços externos obrigatórios; todo processamento ocorre localmente.
- Não apresenta scores como provas; são apenas indicadores para orientar investigações.
- Não faz atribuição de autoria, culpa ou intenção.

### Instalação e Execução

```bash
git clone <repo_url>
cd signaltrace-ce
python -m venv .venv
source .venv/bin/activate  # no Windows use `.venv\Scripts\Activate.ps1`
pip install -r requirements.txt
pip install -r requirements-dev.txt  # opcional para desenvolvimento e testes
pytest -q  # executa a suíte de testes

# Rodar o pipeline via CLI
python -m src.cli.main run --input examples/synthetic/events_dataset_v1.json

# Iniciar a API local (por padrão na porta 5000)
python -m src.api.server
```

## Documentação

- [`docs/schema_event.md`](docs/schema_event.md): detalhes do schema de eventos observacionais.
- [`docs/scoring.md`](docs/scoring.md): explicação sobre o sistema de scoring e seus fatores.
- [`docs/engine_flow.md`](docs/engine_flow.md): fluxo interno do motor.
- [`docs/api.md`](docs/api.md): especificação dos endpoints da API pública local.
- [`docs/cli.md`](docs/cli.md): referência de comandos da CLI.
- [`docs/contracts.md`](docs/contracts.md): contrato de saída dos relatórios versionados.
- [`docs/demo.md`](docs/demo.md): guia para executar a demonstração sintética.

## Mudanças Recentes

Consulte o `CHANGELOG.md` para uma lista detalhada de versões e alterações.
