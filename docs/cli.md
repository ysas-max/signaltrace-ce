# CLI Pública – SignalTrace CE

A interface de linha de comando (CLI) fornece uma maneira simples de
interagir com o núcleo do SignalTrace CE a partir do terminal.  Os
comandos são agrupados em subcomandos, cada um com uma finalidade
específica.  Para usar a CLI execute `python -m src.cli.main <comando>`
ou instale o pacote e utilize o script `signaltrace-ce` se
disponibilizado.

## Comandos

### `validate`

Valida um dataset de eventos sintéticos contra o schema de evento.

**Uso:**

```bash
python -m src.cli.main validate --input examples/synthetic/events_dataset_v1.json
```

Se o arquivo contiver eventos válidos, a CLI imprimirá `Dataset
válido.`; caso contrário, uma mensagem de erro será exibida.

### `run`

Executa o pipeline completo (normalização, fingerprint, correlação,
scoring) e imprime um resumo no terminal.

**Uso:**

```bash
python -m src.cli.main run --input examples/synthetic/events_dataset_v1.json
```

O resumo inclui o total de eventos analisados, número de clusters,
distribuição de níveis de risco, marcadores e sinais de risco mais
frequentes e um aviso sobre as limitações do score.

### `report-json`

Gera um relatório estruturado em JSON e o salva em um arquivo.

**Uso:**

```bash
python -m src.cli.main report-json --input examples/synthetic/events_dataset_v1.json --output relatorio.json
```

O arquivo `relatorio.json` conterá os clusters anotados, resumo e
versão do contrato (`analysis_result_v1`).

### `report-md`

Gera um relatório em formato Markdown, adequado para leitura humana.

**Uso:**

```bash
python -m src.cli.main report-md --input examples/synthetic/events_dataset_v1.json --output relatorio.md
```

O arquivo Markdown incluirá um resumo e uma seção para cada cluster.

### `summary`

Imprime apenas o resumo do relatório no terminal, sem executar
qualquer saída de arquivo.

**Uso:**

```bash
python -m src.cli.main summary --input examples/synthetic/events_dataset_v1.json
```

## Avisos Importantes

* Apenas datasets sintéticos devem ser usados.  Não execute a CLI em
  dados reais.
* A correlação e o score de risco são indicativos, não provas.
