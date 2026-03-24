# Fluxo do Motor

O motor do SignalTrace CE segue um fluxo determinístico e auditável para processar eventos observados.  Este fluxo foi projetado para ser claro, simples e extensível.

1. **Leitura e validação:** Os eventos são carregados de um arquivo JSON e validados contra o schema público (`schemas/event_schema_v1.json`).  Eventos inválidos geram erro e são rejeitados.
2. **Normalização:** Textos, domínios, marcadores e outros campos são normalizados de forma segura (`src/normalization/normalizer.py`).  São aplicadas regras de limpeza, tokenização e detecção de repetições e palavras‑chave suspeitas.
3. **Fingerprint:** Para cada evento é criado um fingerprint comportamental (`src/fingerprint/event.py`) com features numéricas e conjuntos de tokens, domínios e marcadores.  Este fingerprint é não reversível e não armazena texto original.
4. **Correlação:** Os fingerprints são correlacionados em clusters com base em similaridade de domínio, tokens, marcadores e proximidade temporal (`src/correlation/event_correlation.py`).  Um limiar simples determina se eventos devem pertencer ao mesmo cluster.
5. **Scoring:** Cada cluster recebe um score de risco de 0 a 1 calculado a partir de métricas agregadas (repetição de domínios, similaridade textual, presença de marcadores, proximidade temporal e flags de risco) e pesos configuráveis (`src/scoring/risk.py`).  O score é convertido em um nível categórico (`baixo`, `moderado`, `alto`, `crítico`) e uma explicação textual é gerada.
6. **Saída:** O resultado pode ser exposto via API, CLI ou relatórios em JSON/Markdown.  A API retorna objetos `analysis_result`, enquanto a CLI oferece opções de impressão resumida ou geração de arquivos.

Este fluxo foi pensado para priorizar a **auditabilidade** e a **explicabilidade**.  Cada etapa pode ser examinada isoladamente e testada com dados sintéticos.
