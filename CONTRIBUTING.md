# Guia de Contribuição para signaltrace‑ce

Obrigado por considerar contribuir para o **signaltrace‑ce**!  Este projeto depende da comunidade para evoluir e manter sua transparência.  Leia este guia antes de enviar problemas ou pull requests.

## Fluxo de trabalho

1. **Fork** o repositório e crie um branch a partir de `main` para suas alterações.
2. Certifique‑se de que sua alteração está de acordo com as [Regras Rígidas](README.md#regras-rígidas-e-inegociáveis).
3. Escreva testes apropriados em `tests/` e verifique se todos os testes passam.
4. Atualize a documentação relevante (README, CHANGELOG, etc.).
5. Siga o modelo de pull request em `.github/pull_request_template.md` e preencha todas as caixas de verificação.
6. Aguarde revisão.  Responda aos comentários de forma respeitosa e mantenha a discussão focada na melhoria do código.

## Estilo de Código

* Siga a PEP 8 para código Python.  Utilize ferramentas como `flake8` e `black` para garantir consistência.
* Organize importações com `isort`.
* Documente funções e classes com docstrings no estilo [Google](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) ou [reStructuredText].

## Mensagens de Commit

Escreva mensagens de commit claras em português ou inglês.  Comece com um verbo no infinitivo e descreva brevemente a mudança.  Exemplo:

```
Adiciona sanitizador básico e teste
```

Inclua referências a issues quando aplicável usando `Fixes #n` ou `Refs #n`.

## Problemas (Issues)

Antes de abrir um novo issue, verifique se já existe um report semelhante.  Ao abrir um issue, forneça um título descritivo e todos os detalhes necessários para reproduzir o problema ou justificar a nova funcionalidade.

## Segurança e Dados Sensíveis

Nunca inclua dados reais, credenciais, tokens ou material sensível em commits, issues ou pull requests.  Siga as orientações em [`DATA_POLICY.md`](DATA_POLICY.md) e reporte vulnerabilidades de forma responsável conforme descrito em [`SECURITY.md`](SECURITY.md).

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença AGPL 3.0 que o projeto.