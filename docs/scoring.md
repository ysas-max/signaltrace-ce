# Sistema de Scoring

O sistema de scoring do SignalTrace CE produz um valor numérico entre 0 e 1 para cada cluster e atribui um nível categórico que auxilia na priorização de análises.  O score é calculado a partir de métricas simples e pesos configuráveis, e **não** deve ser interpretado como prova.

## Fatores Considerados

| Fator | Descrição |
| --- | --- |
| **Repetição de domínio** | Proporção de eventos do cluster que compartilham o mesmo domínio normalizado. |
| **Similaridade textual** | Média da interseção de tokens entre pares de eventos. |
| **Presença de marcadores** | Proporção de eventos que possuem marcadores de campanha. |
| **Proximidade temporal** | Quão próximos no tempo estão os eventos (janela de 7 dias). |
| **Risk flags** | Proporção de eventos que possuem flags de risco configuradas durante a normalização. |

Cada métrica é normalizada entre 0 e 1 e multiplicada por um peso.  Os pesos padrão são definidos em `src/scoring/risk.py`, mas podem ser ajustados futuramente.

## Cálculo do Score

O score total é a soma ponderada das métricas.  Em seguida, utiliza‑se uma função degrau para mapear o score numérico para um nível categórico:

- **baixo**: score < 0.25
- **moderado**: 0.25 ≤ score < 0.50
- **alto**: 0.50 ≤ score < 0.75
- **crítico**: score ≥ 0.75

## Justificativa

A justificativa textual indica o valor de cada métrica e o peso aplicado, permitindo que analistas entendam por que um cluster recebeu determinado score.  Exemplo de explicação:

```
domain: 1.00 (peso 0.30); tokens: 0.67 (peso 0.25); markers: 1.00 (peso 0.20); time: 0.90 (peso 0.15); risk_flags: 0.50 (peso 0.10)
```

## Aviso Importante

O score é apenas um **indicador heurístico** e não constitui prova.  Ele deve ser utilizado como um sinal para orientar investigações mais profundas.  Falsos positivos e falsos negativos são possíveis.  Consulte `docs/contracts.md` para ver como o score é representado nos contratos de saída.
