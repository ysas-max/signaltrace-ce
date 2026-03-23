# Roteiro de Desenvolvimento (Roadmap)

Este roadmap esboça a direção planejada para o **signaltrace‑ce**.  Os itens listados são aspiracionais; a comunidade é bem-vinda a sugerir, discutir e contribuir.

## Curto Prazo (0–6 meses)

* 🧪 **Aprimorar exemplos sintéticos**: adicionar casos que representam diferentes padrões comportamentais para treinar e testar o motor.
* 🛠 **Adicionar normalização de campos**: introduzir funções para normalizar formatos de data, números e URLs.
* 🧰 **Ferramentas de explicabilidade**: incorporar camadas que expliquem como cada feature contribui para o score final.
* ✅ **Cobertura de testes**: aumentar cobertura para acima de 80%, incluindo testes de integração entre módulos.

## Médio Prazo (6–12 meses)

* 📦 **Suporte a múltiplos formatos de dados**: permitir ingestão de CSV, Parquet ou outros formatos populares além de JSON.
* 🧮 **Modelos de scoring configuráveis**: permitir ajuste de pesos e parâmetros via arquivos de configuração.
* 🔄 **Versão 2 dos schemas**: evoluir os schemas públicos com base no feedback dos usuários.
* 🧑‍💻 **Integração com visualizadores**: criar exemplos de integração com dashboards ou notebooks para visualização dos resultados.

## Longo Prazo (12+ meses)

* 🧠 **Incorporação de aprendizado de máquina**: explorar modelos que auxiliem na geração de fingerprints comportamentais, mantendo explicabilidade.
* 🌐 **Internacionalização (i18n)**: traduzir documentação e mensagens para múltiplos idiomas.
* 🔐 **Módulos de privacidade diferencial**: avaliar integrações que permitam executar computação sobre dados sensíveis de forma segura, sem revelá-los.

Esta lista não é exaustiva.  Sugestões e PRs são sempre bem‑vindos!  Consulte [`GOVERNANCE.md`](GOVERNANCE.md) para entender como decisões são tomadas.