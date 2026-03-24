# API Pública – SignalTrace CE

Esta documentação descreve a API local oferecida pela edição
comunitária do SignalTrace.  A API é implementada com um servidor
minimal embutido (sem dependências externas como Flask) e é
executada localmente; não há autenticação nesta fase e todos os
dados processados devem ser sintéticos.  Nenhum dado real deve ser
enviado à API.

## Endpoints

### `GET /health`

Retorna um objeto JSON simples indicando que o serviço está ativo.
Utilize este endpoint para verificações de liveness.

Exemplo:

```json
{
  "status": "ok",
  "timestamp": "2026-03-24T12:00:00Z"
}
```

### `GET /schema/event`

Retorna o schema JSON usado para validar eventos sintéticos.  O
conteúdo é carregado a partir de `schemas/event_schema_v1.json`.

### `POST /normalize`

Normaliza uma lista de eventos.  O corpo da requisição deve conter um
objeto JSON com a chave `events` que referencia um array de eventos.
Os eventos são validados contra o schema; em seguida campos como
`message_text`, `domain_hint` e `campaign_markers` são normalizados.
Retorna um objeto com a chave `normalized` contendo a lista de
eventos normalizados.

### `POST /fingerprint`

Extrai fingerprints a partir de eventos normalizados.  O corpo deve
conter a chave `events` com os objetos de entrada.  A resposta
contém um array `fingerprints` com as características de cada
evento.

### `POST /correlate`

Agrupa fingerprints em clusters com base em similaridade de tokens,
domínio, marcadores e tempo.  O corpo deve conter a chave
`fingerprints` com os fingerprints no mesmo formato retornado por
`/fingerprint`.  A resposta inclui uma chave `clusters` com a lista de
clusters formados.

### `POST /score`

Atribui scores de risco aos clusters.  O corpo deve conter a chave
`clusters` com as estruturas retornadas por `/correlate`.  A resposta
inclui uma chave `scored_clusters` com os clusters anotados com
`score`, `level` e `explanation`.

### `POST /analyze`

Executa todo o pipeline em uma única chamada.  O corpo deve conter a
chave `events` com os eventos originais.  A resposta segue o
contrato `analysis_result` e contém:

* `clusters`: lista de clusters com score e explicação.
* `summary`: estatísticas agregadas (total de eventos, clusters,
  distribuição de risco, marcadores e sinais de risco mais comuns).
* `schema_version`: versão do contrato retornado (`analysis_result_v1`).

## Uso

Para executar a API localmente, instale as dependências (`pip
install -r requirements-dev.txt`) e rode:

```bash
python -m src.api.server
```

 Por padrão o servidor ouvirá na porta 5000.  Utilize ferramentas como
`curl` ou `httpie` para interagir com os endpoints.  Consulte os
testes em `tests/test_api.py` para exemplos práticos de uso.

## Limitações

* A API não possui autenticação ou controle de acesso nesta fase.
* Todos os dados devem ser sintéticos; enviar dados reais viola as
  regras de uso da Community Edition.
* Os scores e correlações são apenas indicadores e não constituem
  prova categórica de fraude ou atividade maliciosa.
