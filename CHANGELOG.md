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
