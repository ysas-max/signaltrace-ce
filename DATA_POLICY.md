# Política de Dados

O **signaltrace‑ce** é um repositório público e auditável.  Para proteger a privacidade e garantir conformidade com leis de proteção de dados, estabelecemos as seguintes regras para qualquer dado incluído neste projeto.

## Proibições

1. **Nenhum dado real deve ser commitado.** Nunca envie logs, mensagens, números de telefone, identificadores pessoais, tokens de acesso ou qualquer informação que possa identificar indivíduos ou operações reais.
2. **Nada de credenciais ou segredos.** Senhas, chaves de API, certificados ou tokens de serviço são estritamente proibidos.
3. **Sem evidências operacionais.** Este repositório não é um repositório de investigação; não aceite arquivos que contenham observações ou indicadores de ameaças do mundo real.

## O que é permitido

* **Amostras sintéticas:** Arquivos gerados artificialmente que imitam a estrutura de dados reais, mas com conteúdo inventado que não corresponde a pessoas ou organizações verdadeiras.
* **Dados públicos seguros:** Informações que já são de domínio público e cujo uso não infringe direitos autorais nem privacidade (ex.: domínios fictícios, nomes de empresas genéricas).

## Boas Práticas

* Mascare dados sensíveis sempre que estiver criando exemplos (ex.: usar "1234567890" como número fictício).
* Indique claramente nos comentários ou nomes de arquivos quando um exemplo for totalmente sintético.
* Execute revisão manual de pull requests para garantir conformidade com esta política.
* Se houver dúvidas sobre a adequação de um dado, **não o inclua**.

## Fiscalização

Issues e pull requests que violem esta política serão encerrados imediatamente.  Colaboradores reincidentes podem perder privilégios de contribuição.  Para mais detalhes sobre as responsabilidades dos contribuidores, veja [`CONTRIBUTING.md`](CONTRIBUTING.md) e [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).