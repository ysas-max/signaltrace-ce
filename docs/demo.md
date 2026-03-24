# Demo Reproduzível – SignalTrace CE

Esta demo demonstra como executar a API localmente, processar um
dataset sintético e gerar relatórios por meio da CLI.  Todo o fluxo
utiliza apenas dados artificiais disponíveis no repositório.

## Pré‑requisitos

* Python 3.10 ou superior
* Dependências instaladas via `pip install -r requirements-dev.txt`

## Passo a passo

1. **Iniciar a API local**

   Abra um terminal na raiz do repositório e execute:

   ```bash
   python -m src.api.server
   ```

   A API ficará escutando em `http://localhost:5000`.  Em outro
   terminal você pode testar o healthcheck com:

   ```bash
   curl http://localhost:5000/health
   ```

2. **Validar o dataset sintético**

   Utilize a CLI para validar o conjunto de eventos artificial:

   ```bash
   python -m src.cli.main validate --input examples/synthetic/events_dataset_v1.json
   ```

   A mensagem `Dataset válido.` indica que todos os eventos seguem o
   schema público.

3. **Executar o pipeline completo**

   Para analisar o dataset e visualizar um resumo:

   ```bash
   python -m src.cli.main run --input examples/synthetic/events_dataset_v1.json
   ```

4. **Gerar relatórios**

   *JSON*: crie um relatório estruturado em JSON:

   ```bash
   python -m src.cli.main report-json --input examples/synthetic/events_dataset_v1.json --output demo_report.json
   ```

   *Markdown*: crie um relatório legível em Markdown:

   ```bash
   python -m src.cli.main report-md --input examples/synthetic/events_dataset_v1.json --output demo_report.md
   ```

5. **Analisar clusters pela API**

   Com a API em execução, você pode enviar os eventos diretamente:

   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d @examples/synthetic/events_dataset_v1.json \
        http://localhost:5000/analyze
   ```

   A resposta incluirá os clusters com scores e o resumo agregado.

## Observações

* A demo não requer qualquer dado externo ou real.
* O fluxo completo funciona off‑line e não realiza chamadas de rede
  além do loopback local.
* Os scores e correlações são indicativos; consulte o campo
  `warning` no resumo para entender as limitações.
