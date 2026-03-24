# Contratos de Saída – SignalTrace CE

Os contratos a seguir definem a estrutura das saídas produzidas pela
API, CLI e funções de geração de relatórios.  Todas as versões são
prefixadas por um identificador (`_v1`) para permitir evolução
compatível no futuro.  Os esquemas são informais e refletem a
estrutura de objetos Python serializados em JSON.

## `analysis_result_v1`

Objeto retornado por `/analyze` e pelas funções de geração de
relatórios.  Campos:

| Campo          | Tipo                              | Descrição                                  |
|---------------|------------------------------------|---------------------------------------------|
| `clusters`     | lista de `cluster_result_v1`       | Clusters analisados com scores e explicações |
| `summary`      | `report_summary_v1`                | Estatísticas agregadas do dataset            |
| `schema_version` | string                         | Versão do contrato (`analysis_result_v1`)    |

## `cluster_result_v1`

Representa um cluster de eventos correlacionados.  Campos:

| Campo      | Tipo                       | Descrição                                        |
|-----------|---------------------------|--------------------------------------------------|
| `cluster_id` | string                  | Identificador do cluster (ID do evento central)   |
| `members`    | lista de strings        | IDs de eventos pertencentes ao cluster            |
| `fingerprints` | lista de objetos      | Fingerprints de cada evento no cluster            |
| `score`      | número (0–1)            | Score de risco calculado para o cluster           |
| `level`      | string                  | Nível qualitativo de risco (`baixo`, `moderado`, `alto`, `crítico`) |
| `explanation`| string                 | Texto explicando os principais fatores do score   |

Cada objeto em `fingerprints` possui:

| Campo           | Tipo             | Descrição                                      |
|----------------|-----------------|-------------------------------------------------|
| `event_id`      | string          | Identificador do evento original               |
| `features`      | objeto          | Métricas numéricas extraídas do evento         |
| `tokens`        | lista de strings| Tokens normalizados presentes no texto         |
| `domain`        | string/null     | Domínio normalizado associado ao evento        |
| `markers`       | lista de strings| Marcadores de campanha normalizados            |
| `observed_time` | string          | Timestamp ISO 8601 da observação               |
| `risk_flags`    | lista de strings| Flags de risco atribuídas durante a normalização |

## `report_summary_v1`

Estatísticas agregadas do relatório.  Campos:

| Campo             | Tipo                | Descrição                                       |
|------------------|--------------------|--------------------------------------------------|
| `total_events`    | inteiro            | Número total de eventos analisados               |
| `total_clusters`  | inteiro            | Número de clusters formados                      |
| `risk_levels`     | objeto             | Contagem de clusters por nível de risco          |
| `top_markers`     | lista de strings   | Marcadores de campanha mais frequentes           |
| `top_risk_flags`  | lista de strings   | Sinais de risco mais frequentes                  |
| `warning`         | string             | Aviso explícito de que correlação não é prova    |

## Considerações

Os contratos acima são informais e descritos em texto livre.  Uma
definição formal em JSON Schema poderá ser adicionada em futuras
versões.  Ao consumir estes contratos, sempre verifique a chave
`schema_version` para garantir compatibilidade e evite assumir
propriedades não documentadas.
