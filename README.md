# SignalTrace Community Edition (signaltrace-ce)

SignalTrace CE é a versão de **código aberto** da plataforma SignalTrace, focada em análise defensiva e observacional de campanhas suspeitas. Esta edição comunitária fornece um motor auditável, exemplos sintéticos e documentação completa para permitir contribuições externas sem expor dados sensíveis ou capacidades ofensivas.

## Visão Geral

Esta fase implementa o núcleo funcional mínimo do motor público. O sistema processa eventos observados, aplica normalização segura, extrai fingerprints comportamentais, correlaciona eventos semelhantes e calcula um score de risco configurável. Os resultados incluem justificativas textuais e são baseados unicamente em dados sintéticos.

### Missão Defensiva

O objetivo do SignalTrace CE é apoiar pesquisadores e defensores na análise de campanhas de fraude e spam de forma ética, transparente e explicável. A plataforma **não** faz atribuição categórica de autores ou intenções e **não** oferece funcionalidades ofensivas ou de coleta agressiva. Correlação e score são apenas indicadores; não devem ser interpretados como provas.

### Escopo do Repositório

O repositório público contém:

- Schemas públicos versionados para descrever eventos observacionais.
- Pipeline de normalização que padroniza texto, marcações e domínios de forma segura.
- Fingerprint comportamental que resume características de cada evento de maneira não reversível.
- Correlação básica para agrupar eventos com base em semelhança de domínio, estrutura e marcadores.
- Scoring explicável com pesos configuráveis para indicar níveis de risco.
- Dataset sintético em `examples/synthetic/` com campanhas simuladas, falsos positivos e variações de templates.
- Runner CLI simples que processa o dataset sintético, aplica o pipeline e imprime resultados legíveis.
- Testes unitários cobrindo schema, normalização, fingerprint, correlação, scoring, leitura de dados e runner.

### O que Este Projeto Não Faz

- Não inclui dados reais, credenciais, tokens, telemetria sensível ou evidências operacionais.
- Não contém scraping agressivo ou automação ofensiva.
- Não depende de serviços externos; todo processamento ocorre localmente.
- Não apresenta scores como provas; são apenas indicadores para orientar investigações.

### Separação entre `signaltrace-ce` e `signaltrace-data`

O **signaltrace-ce** contém apenas lógica e dados sintéticos. Dados ou integrações sensíveis pertencem ao repositório privado **signaltrace-data** e não são necessários para utilizar a edição comunitária.

## Instalação e Execução

```bash
git clone <repo_url>
cd signaltrace-ce
python -m venv .venv
source .venv/bin/activate  # no Windows use `.venv\Scripts\Activate.ps1`
pip install -r requirements-dev.txt
pytest -q
python -m src.runner --input examples/synthetic/events_dataset_v1.json
```

## Documentação

- `docs/schema_event.md`
- `docs/scoring.md`
- `docs/engine_flow.md`

## Mudanças Recentes

Consulte o `CHANGELOG.md`.
