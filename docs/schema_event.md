# Schema de Evento Observacional

O schema público versionado para eventos observados está em `schemas/event_schema_v1.json`.

## Obrigatórios

- `event_id`
- `source_type`
- `observed_at`
- `message_text`
- `sender_handle`
- `sender_hash`

## Opcionais

- `destination_hint`
- `domain_hint`
- `campaign_markers`
- `language_hint`
- `risk_flags`
- `metadata`

## Rationale

Os campos foram escolhidos para permitir correlação e scoring sem depender de dados reais, mantendo explicabilidade e auditabilidade.
