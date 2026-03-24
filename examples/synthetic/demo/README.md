# Demo da SignalTrace CE

Este diretório contém um exemplo reproduzível de execução do motor
SignalTrace Community Edition utilizando apenas dados sintéticos.  Siga
as instruções abaixo para gerar e inspecionar relatórios:

1. **Executar o pipeline via CLI**

   ```bash
   python -m src.cli run --input ../events_dataset_v1.json
   ```

   O comando imprimirá no terminal os clusters identificados, os
   scores atribuídos e a explicação de cada score.

2. **Gerar relatório JSON**

   ```bash
   python -m src.cli report-json --input ../events_dataset_v1.json --output report.json
   ```

   O arquivo `report.json` será criado neste diretório contendo a
   estrutura `analysis_result` com todos os clusters e um resumo
   agregado.

3. **Gerar relatório Markdown**

   ```bash
   python -m src.cli report-md --input ../events_dataset_v1.json --output report.md
   ```

   O arquivo `report.md` será criado neste diretório com uma versão
   legível do relatório, incluindo seções de resumo e detalhes por
   cluster.

4. **Executar a API local**

   ```bash
   python -m src.api
   ```

   Em outra janela de terminal, envie uma requisição para analisar
   eventos do dataset sintético:

   ```bash
   curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d @../events_dataset_v1.json
   ```

   O resultado será exibido no terminal e poderá ser comparado com os
   relatórios gerados via CLI.

## Aviso

Todos os dados utilizados aqui são **sintéticos**.  Os scores e a
correlação fornecem apenas indicações heurísticas, e não devem ser
interpretados como provas de fraude ou spam.
