# Schema de Evento Observacional – SignalTrace CE

Este documento descreve o formato dos eventos observacionais aceitos
pelo SignalTrace CE.  O schema formal em JSON encontra‑se em
`schemas/event_schema_v1.json` e segue o padrão JSON Schema Draft 7.

Cada evento representa uma observação isolada de uma mensagem de
possível campanha de spam, fraude ou phishing.  Os campos foram
projetados para suportar dados sintéticos e garantir que nenhum dado
pessoal identificável seja necessário.

## Campos Obrigatórios

| Campo | Tipo | Descrição |
|------|------|-----------|
| `event_id` | string | Identificador único do evento. Deve ser uma string não vazia. |
| `source_type` | string | Tipo de canal de origem da mensagem (`sms`, `whatsapp`, `email`, `social` ou `other`). |
| `observed_at` | string | Timestamp ISO 8601 de quando o evento foi observado (ex.: `2025-01-01T00:00:00Z`). |
| `message_text` | string | Conteúdo textual da mensagem observada. |
| `sender_handle` | string | Nome ou identificador público do remetente. |
| `sender_hash` | string | Hash hexadecimal (64 caracteres) que representa o remetente de forma não reversível. |

## Campos Opcionais

| Campo | Tipo | Descrição |
|------|------|-----------|
| `destination_hint` | string | Pista de destino (telefone ou usuário) codificada de maneira irreversível. |
| `domain_hint` | string | Domínio ou subdomínio relevante extraído da mensagem; somente caracteres alfanuméricos, hífens e pontos são permitidos. |
| `campaign_markers` | array de strings | Marcadores ou rótulos de campanha associados ao evento. |
| `language_hint` | string | Indica o idioma provável da mensagem. |
| `risk_flags` | array de strings | Conjunto de flags de risco identificadas durante a normalização. |
| `metadata` | objeto | Informações adicionais opcionais (valores podem ser string, número, booleano ou nulo). |

## Considerações

* Todos os campos podem conter apenas dados sintéticos; nunca use
  dados pessoais reais.
* O schema restringe tamanho, formatos e padrões para dificultar o
  vazamento acidental de dados sensíveis.
* Campos adicionais não listados no schema são proibidos.

Para detalhes completos, consulte o arquivo JSON Schema em
`schemas/event_schema_v1.json`.